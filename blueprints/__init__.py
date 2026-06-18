# blueprints/__init__.py

from .auth import auth

# This defines what gets imported when someone writes "from blueprints import *"
__all__ = ["auth"]