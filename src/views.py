from flask import Blueprint, request, jsonify

from .app import db, redis_connection
from .models import Notes
from .schema import NotesSchema, RedisNotesSchema

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/", methods=["GET"])
def get_notes():
    # Get all items from DB directly
    notes = Notes.query.all()
    schema = NotesSchema(many=True)
    return jsonify(schema.dump(notes))


@notes_bp.route("/<int:note_id>", methods=["GET"])
def get_note_by_id(note_id):
    schema = NotesSchema()
    redis_schema = RedisNotesSchema()

    # First check if the note is in Redis
    note = redis_connection.get(f"note:{note_id}")

    if note is not None and note != b'{}':
        note = redis_schema.loads(note)

        return jsonify(note)

    # If not, get it from the DB and cache it
    note = Notes.query.filter(Notes.id == note_id).first()

    # Set the note in Redis
    redis_connection.set(f"note:{note_id}", schema.dumps(note))

    return jsonify(schema.dump(note))


@notes_bp.route("/", methods=["POST"])
def create_note():
    schema = NotesSchema()
    note = schema.load(request.json)

    note = Notes(**note)

    db.session.add(note)
    db.session.commit()

    return jsonify(schema.dump(note))


@notes_bp.route("/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    schema = NotesSchema()

    # Get the note from the DB only
    note = Notes.query.get(note_id)

    if not note:
        return jsonify({"message": "Note not found"}), 404

    note_data = schema.load(request.json)
    
    # Upsert data
    for key, value in note_data.items():
        setattr(note, key, value)

    db.session.commit()

    # Update the note in Redis if it exists
    redis_connection.set(f"note:{note_id}", schema.dumps(note), xx=True)

    return jsonify(schema.dump(note))


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = Notes.query.get(note_id)

    if not note:
        return jsonify({"message": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    # Delete the note from Redis if it exists
    redis_connection.delete(f"note:{note_id}")

    return jsonify({"message": "Note deleted"})
