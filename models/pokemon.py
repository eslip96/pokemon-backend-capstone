import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Pokemon(db.Model):
    __tablename__ = "Pokemons"

    pokemon_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pokemon_name = db.Column(db.String(), nullable=False)
    type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Types.type_id'), nullable=False)
    ability_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Abilities.ability_id'), nullable=False)
    description = db.Column(db.String())
    base_stats = db.Column(db.String())

    type = db.relationship("Type", backref="pokemon_instances")

    def __init__(self, name, type_id=None, ability_id=None, description=None, base_stats=None):
        self.name = name
        self.type_id = type_id
        self.ability_id = ability_id
        self.description = description
        self.base_stats = base_stats

    @classmethod
    def new_pokemon_obj(cls):
        return cls("")


class PokemonSchema(ma.Schema):
    class Meta:
        fields = ['pokemon_id', 'name', 'type_id', 'ability_id', 'description', 'base_stats']

    type = ma.fields.Nested("TypeSchema", only=['type_id', 'name'])


pokemon_schema = PokemonSchema()
pokemons_schema = PokemonSchema(many=True)
