import sys
from gunicorn.app.base import BaseApplication
from flask import Flask
from api.main import register_routes
from db import ping_database
from migrations.migrate import migrate_database_tables
from settings import settings

app = Flask(__name__)

register_routes(app)

# class FlaskGunicornApplication(BaseApplication):
#     def __init__(self, app, options=None):
#         self.options = options or {}
#         self.application = app
#         super().__init__()

#     def load_config(self):
#         for key, value in self.options.items():
#             if key in self.cfg.settings and value is not None:
#                 self.cfg.set(key.lower(), value)

#     def load(self):
#         return self.application

if __name__ == "__main__":
    if len(sys.argv) == 2:
        match sys.argv[1]:
            case "api":
                ping_database() # ping database before server start, exit when failed

                gunicorn_options = {
                    "bind": f"0.0.0.0:{settings.PORT}",
                }

                # Run Gunicorn with the Flask application
                # FlaskGunicornApplication(app, gunicorn_options).run()
                app.run(host="0.0.0.0", port=settings.PORT,debug=True)

            case "migrate":
                migrate_database_tables()
