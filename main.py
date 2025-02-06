from app import create_app
app = create_app()


@app.route('/')
def hello():
    return "Hello, World!"

# La ligne suivante n'est pas nécessaire avec Gunicorn
# if __name__ == '__main__':
#     app.run(debug=True)
