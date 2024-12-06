from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, exc
from src.config import Config

# Create an instance of SQLAlchemy
db = SQLAlchemy()

class DatabaseService:
    _instance = None

    def __new__(cls, app=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if app is not None:
                cls._instance.init_app(app)
        return cls._instance

    def init_app(self, app):
        """Initialize the app with the database configuration."""
        app.config.from_object(Config)
        db.init_app(app)
        self._app = app
        self._check_connection()

    def _check_connection(self):
        """Check if the database connection is successful."""
        try:
            # Create an engine to test the connection
            engine = create_engine(self._app.config["SQLALCHEMY_DATABASE_URI"])
            connection = engine.connect()
            connection.close()
            print("Database connected successfully!")
        except exc.SQLAlchemyError as e:
            print(f"Database connection failed: {e}")
            raise e  # Reraise the exception to halt the app startup if connection fails
