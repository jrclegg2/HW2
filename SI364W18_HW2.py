## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################
class AlbumEntryForm(FlaskForm):
    albumName = StringField("Enter the name of an album: ", validators=[Required()])
    likeness = RadioField("How much do you like this album? (1 low, 3 high)", choices = [(1, '1'), (2, '2'), (3, '3')])
    submit = SubmitField('Submit')
####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artistform():
    return render_template('artistform.html')

@app.route('/artistinfo')
def artistInfo():
    requestURL = "https://itunes.apple.com/search"
    artist = request.args.get('artist')
    requestParams = {'term' : artist}
    itunesSearch = json.loads(requests.get(requestURL, params = requestParams).text.encode('utf-8'))
    return render_template('artist_info.html', objects = itunesSearch['results'])

@app.route('/artistlinks')
def artistlinks():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specificSong(artist_name):
    artistName = artist_name
    requestURL = "https://itunes.apple.com/search"
    artist = request.args.get('artist')
    requestParams = {'term' : artistName}
    itunesSearch = json.loads(requests.get(requestURL, params = requestParams).text.encode('utf-8'))
    return render_template('specific_artist.html', results = itunesSearch['results'])

@app.route('/album_entry')
def album_entry():
    simpleForm = AlbumEntryForm()
    return render_template('album_entry.html', form = simpleForm)

@app.route('/album_result', methods = ("GET", "POST"))
def album_result():
    form = AlbumEntryForm(request.form)
    if (request.method == 'POST') and (len(form.albumName.data) > 0) and (form.likeness.data != 'None'):
        albumName = form.albumName.data
        likeness = form.likeness.data
        return render_template('album_data.html', form = form)
    else:
        flash("All fields are required!")
        return redirect(url_for('album_entry'))
if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
