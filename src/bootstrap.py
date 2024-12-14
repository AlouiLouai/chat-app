# bootstrap.py: Ensure monkey-patching is applied first
import eventlet
eventlet.monkey_patch()

from src.server import app