from flask import Flask
from src.database import DatabaseService

app = Flask(__name__)

# Initialize the Singleton DatabaseService
db_service = DatabaseService(app)

@app.route("/")
def hello():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)