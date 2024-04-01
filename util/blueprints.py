import routes


def register_blueprints(app):
    app.register_blueprint(routes.ability)
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.pokemon)
    app.register_blueprint(routes.team)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.type)
