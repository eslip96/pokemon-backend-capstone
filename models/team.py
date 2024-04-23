import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from .teampokemonxref import team_pokemon_association_table

from db import db


class Team(db.Model):
    __tablename__ = "Team"

    team_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_name = db.Column(db.String(), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=True)
    # description = db.Column(db.String())

    pokemons = db.relationship("Pokemon", secondary=team_pokemon_association_table, back_populates='teams')

    def __init__(self, team_name):
        self.team_name = team_name
        # self.description = description

    def new_team_obj():
        return Team("")


class TeamSchema(ma.Schema):
    class Meta:
        fields = ['team_id', 'team_name']

    pokemons = ma.fields.Nested("PokemonSchema", many=True, exclude=['teams'])


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
