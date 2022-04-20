from flask import Flask, jsonify, render_template, request, redirect
import requests, socket, os

app = Flask(__name__)

# Default URL to get requests from, localhost:4995
BASE = "http://127.0.0.1:4995/"



# Class accepts a json and sets all of the fields
class Track(object):
    def __init__(self, jsonblob):
        self.id = jsonblob["id"]
        self.name = jsonblob["name"]
        self.popularity = jsonblob["popularity"]
        self.duration_ms = jsonblob["duration_ms"]
        self.explicit = jsonblob["explicit"]
        self.artists = jsonblob["artists"]
        self.id_artists = jsonblob["id_artists"]
        self.release_date = jsonblob["release_date"]
        self.danceability = jsonblob["danceability"]
        self.energy = jsonblob["energy"]
        self.key = jsonblob["key"]
        self.loudness = jsonblob["loudness"]
        self.mode = jsonblob["mode"]
        self.speechiness = jsonblob["speechiness"]
        self.acousticness = jsonblob["acousticness"]
        self.instrumentalness = jsonblob["instrumentalness"]
        self.liveness = jsonblob["liveness"]
        self.valence = jsonblob["valence"]
        self.tempo = jsonblob["tempo"]
        self.time_signature = jsonblob["time_signature"]
        
    # Print all data in track
    def printTrack(self):
        print("id = " + self.id)
        print("name = " + self.name)
        print("popularity = " + self.popularity)
        print("duration_ms = " + self.duration_ms)
        print("explicit = " + self.explicit)
        print("artists = " + self.artists)
        print("id_artists = " + self.id_artists)
        print("release_date = " + self.release_date)
        print("danceability = " + self.danceability)
        print("energy = " + self.energy)
        print("key = " + self.key)
        print("loudness = " + self.loudness)
        print("mode = " + self.mode)
        print("speechiness = " + self.speechiness)
        print("acousticness = " + self.acousticness)
        print("instrumentalness = " + self.instrumentalness)
        print("liveness = " + self.liveness)
        print("valence = " + self.valence)
        print("tempo = " + self.tempo)
        print("time_signature = " + self.time_signature)

# contains search data
searchData = []

# loads main menu default
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

# Implement search function logic below
@app.route('/search', methods=['GET', 'POST'])
def search():
    global searchData
    if len(searchData) == 0:
        return redirect('/reset')
    if request.method == 'POST':
        searchCategory = request.form['category']
        searchString = request.form['content']
        result = requests.get(BASE + "api/search?type=" + searchCategory + "&term=" + searchString)
        r_data = result.json()
        compareDB = []
        tempDB = []
        
        for compareElements in r_data:
            compareDB.append(Track(compareElements))
        for compareElements in compareDB: 
            for searchElements in searchData:
                if compareElements.id == searchElements.id:
                    tempDB.append(searchElements)
        searchData = tempDB
        if len(searchData) == 0:
            return render_template('notfound.html')
        try:
            return redirect('/search')
        except:
            return "Error while attempting to search"
    else:
        return render_template('search.html', data=searchData)

@app.route('/reset')
def reset():
    global searchData
    searchData.clear()
    result = requests.get(BASE + "default")
    r_data = result.json()
    for elements in r_data:
        searchData.append(Track(elements))
    return redirect('/search')

@app.route('/database')
def database():
    return render_template('database.html')

@app.route('/export')
def export():
    r = requests.get(BASE + "export")
    return redirect('/database')

if __name__ == "__main__":
    app.run(debug=True)