import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from .teampokemonxref import team_pokemon_association_table

from db import db


class Pokemon(db.Model):
    __tablename__ = "Pokemon"

    pokemon_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pokemon_name = db.Column(db.String(), nullable=False)
    type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Type.type_id'), nullable=False)
    ability_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Ability.ability_id'), nullable=True)
    description = db.Column(db.String())

    type = db.relationship("Type", back_populates="pokemons")
    teams = db.relationship("Team", secondary=team_pokemon_association_table, back_populates="pokemons")

    def __init__(self, pokemon_name, type_id, description):
        self.pokemon_name = pokemon_name
        self.type_id = type_id

        self.description = description

    def new_pokemon_obj():
        return Pokemon("", "", "")


class PokemonSchema(ma.Schema):
    class Meta:
        fields = ['pokemon_id', 'pokemon_name', 'type_id', 'description']

    type = ma.fields.Nested("TypeSchema", only=['type_id', 'name'])
    teams = ma.fields.Nested("TeamsSchema", many=True, exclude=['pokemons'])


pokemon_schema = PokemonSchema()
pokemons_schema = PokemonSchema(many=True)
