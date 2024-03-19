import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Type(db.Model):
    __tablename__ = "Types"

    type_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    pokemons = db.relationship("Pokemon", backref="type")

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    @classmethod
    def new_type_obj(cls):
        return cls("")


class TypeSchema(ma.Schema):
    class Meta:
        fields = ['type_id', 'name', 'description']


type_schema = TypeSchema()
types_schema = TypeSchema(many=True)
