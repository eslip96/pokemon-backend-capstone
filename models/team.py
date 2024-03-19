import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Team(db.Model):
    __tablename__ = "Teams"

    team_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_name = db.Column(db.String(), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)

    pokemons = db.relationship("Pokemon", secondary="Team_Pokemon", back_populates="teams")

    def __init__(self, team_name, user_id):
        self.team_name = team_name
        self.user_id = user_id

    @classmethod
    def new_team_obj(cls):
        return cls("")


class TeamSchema(ma.Schema):
    class Meta:
        fields = ['team_id', 'team_name', 'user_id', 'pokemons']

    pokemons = ma.fields.Nested("PokemonSchema", many=True, exclude=['teams'])


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
