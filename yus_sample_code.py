from flask import Flask, request, render_template
from urllib2 import urlopen
from json import load

app = Flask(__name__)

@app.route('/')
def index():
    return """
        <!DOCTYPE html>
        <html>
            <body>
                <h1>Are you ready to explore parks in San Francisco?</h1>
                <img src =
                <form action = "/parks">
                    <label>Please put a zipcode to find parks! 
                    <input type="text" name="zipcode"></label>
                    <input type="submit">
                </form>
           
            </body>
            </html>"""


@app.route("/parks")
def find_parks_sf():
    zipcode_input = request.args.get("zipcode")
    apiUrl = "http://data.sfgov.org/resource/94uf-amnx.json"
    response = urlopen(apiUrl)

    json_obj = load(response)
    # zipcode_input = raw_input("Zipcode?")
    park_list=[]
    for park in json_obj:
        if "zipcode" in park:
        # print park["zipcode"]

            if park["zipcode"] == zipcode_input:
                park_list.append(park["parkname"])

    if len(park_list) == 0:
        return "<html> There was no parks within the zipcode... Try again </html>"

    else:    
    # print "<html>"+"<br>".join(park_list)+"</html>" #in order to get raw data to test out
        return "<html>"+"<br>".join(park_list)+"</html>"



if __name__ == "__main__":
    app.run(debug=True)