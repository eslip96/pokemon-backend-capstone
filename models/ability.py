import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Ability(db.Model):
    __tablename__ = "Ability"

    ability_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ability_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    def __init__(self, ability_name, description):
        self.ability_name = ability_name
        self.description = description

    def new_ability_obj():
        return Ability("", "")


class AbilitySchema(ma.Schema):
    class Meta:
        fields = ['ability_id', 'ability_name', 'description']


ability_schema = AbilitySchema()
abilities_schema = AbilitySchema(many=True)
