from flask import Flask

asteroid_app = Flask(__name__)


def main():
    from views_pkg.asteriods_calls import asteroids_bp
    asteroid_app.register_blueprint(asteroids_bp)


def run():
    asteroid_app.run(host='0.0.0.0', port=8444)


if __name__ == '__main__':
    main()
    run()
