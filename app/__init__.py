# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy

# from flask_googlemaps import GoogleMaps

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
# db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.modul.upload.controllers import mod_upload as upload_module
from app.modul.upload.controllers import mod_uploader as uploader_module
from app.modul.cleaning.controllers import mod_select_column as select_column_module
from app.modul.cleaning.controllers import mod_cleaning as cleaning_module
from app.modul.cluster.controllers import mod_cluster as cluster_module

# Register blueprint(s)
app.register_blueprint(select_column_module)
app.register_blueprint(upload_module)
app.register_blueprint(uploader_module)
app.register_blueprint(cleaning_module)
app.register_blueprint(cluster_module)

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()
