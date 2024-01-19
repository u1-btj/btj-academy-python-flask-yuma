from .user.views import router as user_router
from .auth.views import router as auth_router
from .base.views import router as base_router
from .note.views import router as note_router

def register_routes(app):
    """
    Register routes with blueprint and namespace
    """
    app.register_blueprint(base_router)
    app.register_blueprint(auth_router) 
    app.register_blueprint(user_router)
    app.register_blueprint(note_router)     