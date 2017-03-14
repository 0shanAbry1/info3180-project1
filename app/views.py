"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
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


@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/profile', methods=['GET','POST'])
def add_profile():
    """Renders the profile form to add a new user"""
    form = ProfileForm() #Instance of the form
    
    if(request.method == 'POST'): #Handles POST requests
        if form.validate_on_submit(): #Form is valid
            # Retrieve form data
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            username = request.form['username']
            age = request.form['age']
            biography = request.form['biography']
            gender = request.form['gender']
            
            imageFolder = app.config["UPLOAD_FOLDER"]
            imageFile = request.files['image']
            
            #Determines the file name of the image
            if(imageFile.filename == ''):
                imageName = "default-profilePicture.jpg"
            else:
                imageName = secure_filename(imageFile.filename)
                imageFile.save(os.path.join(imageFolder, imageName))
            
            while True:
                userid = random.randint(7000000,7999999) #Generates a random id for the user
                userid_data = UserProfile.query.filter_by(userid=userid).first()
                
                if userid_data is None: #Genereated userid is unique
                    break
                
                created_on = timeinfo() #Retrieves today's date
                
                entry = UserProfile(userid, firstname, lastname, username, age, gender, biography, imageName, created_on)
                db.session.add(entry)
                db.session.commit()
                
                flash('New profile for user added successfully :)', 'success')
                
                # return redirect(url_for('view_profile', userid=userid))
                # return redirect('/profile/' + userid)
                return redirect(url_for('list_profiles'))
    
    flash_errors(form)
    
    #Default >> GET Request
    return render_template('add_profile.html', form=form)

@app.route('/profiles', methods=['GET','POST'])
def list_profiles():
    """ Renders an html template (GET) and json (POST) for a list of all user profiles"""
    profiles = db.session.query(UserProfile).all() #Retrieves all the profiles records from the database
    
    if(request.method == 'POST' and request.headers['Content-Type'] == 'application/json'):
        #list_profJson = [] #List of profile jsons
        list_profDict = [] #List of profile dictionaries
        
        for profile in profiles: # Traverse the query result
            #profJson = jsonify(username=profile.username, userid=profile.userid)
            #list_profJson.append(profJson)
            
            profDict = {'username': profile.username, 'userid': profile.userid}
            list_profDict.append(profDict)
        
        #return jsonify(users=list_profJson)
        return jsonify(users=list_profDict)
    else:
        if not profiles:
            flash('No users exist. Please add a new user to create a listing.', 'danger')
            return redirect(url_for('add_profile'))
            
        return render_template('profiles_listing.html', profiles=profiles)


@app.route('/profile/<userid>', methods=['GET','POST'])
def view_profile(userid):
    """ Renders an html template (GET) and json (POST) for an individual user profile"""
    user_profile = UserProfile.query.filter_by(userid=userid).first() 
    
    if(request.method == 'POST' and request.headers['Content-Type'] == 'application/json'):
        if user_profile: #Not empty >> user_profile
            return jsonify(userid=user_profile.userid, username=user_profile.username, image=user_profile.image, gender=user_profile.gender, age=user_profile.age, profile_created_on=user_profile.created_on)
        else: #Empty >> user_profile
            return jsonify(user_profile)
    elif(request.method == 'GET'):
        if not user_profile: #Empty >> user_profile
            flash('User does not exist.','danger')
            return redirect(url_for('list_profiles'))
        else: #Not empty >> user_profile
            return render_template('view_profile.html', user_profile=user_profile)


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
