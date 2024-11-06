from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is running!"  # This will display the message

if __name__ == '__main__':
    print("Starting Flask app...")  # Debug print
    app.run(debug=True)