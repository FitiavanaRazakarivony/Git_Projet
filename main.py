from app import create_app
from waitress import serve

app = create_app()


@app.route('/')
def hello():
    return "Hello, World!"


if __name__ == '__main__':
    #app.run(debug=True)
    serve(app, host='0.0.0.0', port=8000)
