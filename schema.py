from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .models import Notes

class NotesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notes
        include_relationships = True
        unknown = EXCLUDE