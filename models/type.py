import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Type(db.Model):
    __tablename__ = "Type"

    type_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    pokemons = db.relationship("Pokemon", back_populates="type")

    def __init__(self, type_name, description):
        self.type_name = type_name
        self.description = description

    def new_type_obj():
        return Type("", "")


class TypeSchema(ma.Schema):
    class Meta:
        fields = ['type_id', 'type_name', 'description']


type_schema = TypeSchema()
types_schema = TypeSchema(many=True)
