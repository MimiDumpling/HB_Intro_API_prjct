from flask import Flask, request, render_template
from random import choice, randint
from urllib2 import urlopen
from json import load
import api_sample_code_webapp 


# "__name__" is a special Python variable for the name of the current module
# Flask wants to know this to know what any imported things are relative to.
app = Flask(__name__)

@app.route('/')
def index():
    """Home page."""
    return render_template("home.html")
    #return render_template("cat_game.html")


@app.route('/fur-name')
def get_fur_name():
    
    player = request.args.get("Fur-Name")
    greeting = "Hello " + player + "!"
    return render_template("cat_game.html", 
                           furr_name=player, 
                           show_greeting=greeting)

@app.route('/art')
def find_art():
    zipcode_input = request.args.get("zipcode")
    five_shortest = api_sample_code_webapp.parse_five_shortest(zipcode_input)
    print five_shortest
    print type(five_shortest)

    if len(five_shortest) == 0:
        return "<html> There was no civic art pieces within the zipcode... Try again </html>"

    else:    
        return render_template("art_results.html", five_shortest = five_shortest)

@app.route('/game-type')
def choose_game_type():
    user_input = request.args.get("game-name")
    
    if user_input == "Game" or user_input == "game" or user_input == "g":
        return render_template("cat_game.html")
    else:
        return render_template("art.html")    

if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads"
    # our web app if we change the code.
    app.run(debug=True)
