from db import db

team_pokemon_association_table = db.Table(
    "TeamPokemonAssociation",
    db.Column('team_id', db.ForeignKey('Teams.team_id'), primary_key=True),
    db.Column('pokemon_id', db.ForeignKey('Pokemons.pokemon_id'), primary_key=True),
    # db.Column('nickname', db.String()),
    # db.Column('level', db.Integer())
)
