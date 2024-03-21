import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Ability(db.Model):
    __tablename__ = "Abilities"

    ability_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    @classmethod
    def new_ability_obj(cls):
        return cls("")


class AbilitySchema(ma.Schema):
    class Meta:
        fields = ['ability_id', 'name', 'description']


ability_schema = AbilitySchema()
abilities_schema = AbilitySchema(many=True)
