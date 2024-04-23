from db import db

team_pokemon_association_table = db.Table(
    "TeamPokemonAssociation",
    db.Model.metadata,
    db.Column('team_id', db.ForeignKey('Team.team_id'), primary_key=True),
    db.Column('pokemon_id', db.ForeignKey('Pokemon.pokemon_id'), primary_key=True)

)
