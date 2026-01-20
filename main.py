from app import create_app 
from waitress import serve

if __name__ == '__main__':
    app = create_app()
    print('Starting the Flask application...')
    if app.config["DEBUG"] is False:
        serve(app, host='0.0.0.0', port=8000)
    else:
        app.run(debug=True, port=8000)
