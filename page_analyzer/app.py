from flask import Flask

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route('/')
def home_page():
    return 'Welcome to Flask!'


# if __name__ == '__main__':
#     app.run()
