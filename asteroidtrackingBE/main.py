from flask import Flask

asteroid_app = Flask(__name__)


def main():
    """
    Register all the (asteroid) blueprint over here
    """
    from views_pkg.asteriods_calls import asteroids_bp
    from views_pkg.health_info import health_bp
    asteroid_app.register_blueprint(asteroids_bp)
    asteroid_app.register_blueprint(health_bp)


def run():
    """
    Initiation of the front end service takes place at this point.
    """
    asteroid_app.run(host='0.0.0.0', port=8444)


if __name__ == '__main__':
    main()
    run()
