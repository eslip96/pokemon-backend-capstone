import routes


def register_bluprints(app):
    app.register(routes.ability)
    app.register(routes.auth)
    app.register(routes.pokemon)
    app.register(routes.team)
    app.register(routes.users)
    app.register(routes.types)
