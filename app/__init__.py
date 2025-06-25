from dotenv import load_dotenv
from flask import Flask, request, url_for, redirect, Response,render_template
import os
from . import db
from . import registro 

load_dotenv()

def create_app():
   app = Flask(__name__)
   app.config.from_mapping(
      SECRET_KEY= 'mikey',#para definir las sesiones de la app
      DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
      DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
      DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
      DATABASE = os.environ.get('FLASK_DATABASE')
   )


   db.init_app(app)



   app.register_blueprint(registro.bp)

   @app.route('/')
   def index():
      return ("Hola mundo")


   return (app)