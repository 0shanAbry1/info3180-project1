"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, json, jsonify
from forms import ProfileForm
from app.models import UserProfile
from werkzeug.utils import secure_filename

import time
import os
import random

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render the website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/profile/', methods=['GET','POST'])
def add_profile():
    """Renders the new user profile form"""
    form = ProfileForm() #Instance of the form
    
    if request.method == "POST": #Handles POST requests
        if form.validate_on_submit(): #Form validation
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            username = request.form['username']
            age = request.form['age']
            biography = request.form['biography']
            gender = request.form['gender']
             
            imageFolder = app.config["UPLOAD_FOLDER"]
            image = request.files['image']
            
            if(image.filename == ''):
                imageName = "default-profilePicture.jpg"
            else:
                imageName = secure_filename(image.filename)
                image.save(os.path.join(imageFolder, imageName))
                
            #I am here!!!!!!!!!!!!!!! Remember to create folder

@app.route('/profiles/', methods=['GET','POST'])

###
# The functions below should be applicable to all Flask apps.
###

def timeinfo():
    """ Returns the current datetime """
    return time.strftime("%d %b %Y")


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
