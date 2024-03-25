from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from .models import Notes


class NotesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notes
        include_relationships = True
        unknown = EXCLUDE

    id = auto_field(dump_only=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
    
class RedisNotesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notes
        unknown = EXCLUDE
