#create a README file and walk thru process of getting tokens

from urllib2 import urlopen
#from  API import secret_token
#from mapbox import Static #use later to create map
from geopy.geocoders import Nominatim #used to convert zipcode to lat&long
from geopy.distance import vincenty #measures distance between two points
import json
import ast

api_url = "http://data.sfgov.org/resource/bm46-8iwk.json?" #url where all the data lives
response = urlopen(api_url) #downloads the data into the program
full_list_of_art = json.load(response) #parses thru data string and converts it to json to be easier to manipulate
number_of_art_pieces = len(full_list_of_art)

def menu_choice():
	#print title_image

	print '\n    0 - Main Menu'
	print '    1 - Find nearest public art'
	print '    2 - Exits the program\n'

	choice = int(raw_input('Hello! Please choose from the menu options: '))

	return choice


def get_all_art():
	api_url = "http://data.sfgov.org/resource/bm46-8iwk.json?" #url where all the data lives
	response = urlopen(api_url) #downloads the data into the program
	full_list_of_art = json.load(response) #parses thru data string and converts it to json to be easier to manipulate
	number_of_art_pieces = len(full_list_of_art)

	return full_list_of_art


def find_users_long_lat(user_zip):
	#user_zip = raw_input ("There's free San Francisco public art and it's walking distance from where you are! What's your current address and/or SF zipcode? ")

	geolocator = Nominatim()
	location = geolocator.geocode(user_zip) #passes zipcode thru and converts to lat&long
	users_long_lat = (location.latitude, location.longitude)	

	return users_long_lat


def find_art_location(users_long_lat):
	list_of_art_distance = []
	all_art = get_all_art()
	number_of_art_pieces = len(all_art)

	for art_work in range(number_of_art_pieces):
		list_of_art_distance.append({
			"Geo location: ": all_art[art_work]["geometry"]
			})
	
	return list_of_art_distance	


def find_distance_between_art_and_user(user_location):
	list_of_art_distance = []

	for art_work in range(number_of_art_pieces):
		
		art_location = full_list_of_art[art_work]["geometry"]
		if art_location != "geometry":

			art_dict = ast.literal_eval(art_location)
			art_location2 = art_dict["coordinates"]
			art_tuple = (art_location2[1], art_location2[0])


			distance = vincenty(user_location, art_tuple).miles #takes 2 tuples and measures dist between them, returns dist in miles

			list_of_art_distance.append({
				"ID": art_work,
				"distance": distance
				})

	return list_of_art_distance			
			

def sort_art_distances(list_of_art_distance):

	sorted_list = sorted(list_of_art_distance, key=lambda art_distance: art_distance["distance"])

	return sorted_list


def parse_art_data(art_pieces):
	list = []
	default = "N/A"

	for art_piece in art_pieces:
		art_piece_id = art_piece["ID"]
		full_art = full_list_of_art[art_piece_id]

		list.append({
			"Artist: ": full_art.get("artist", default),
			"Title: ": full_art.get("title", default),
			"Material used: ": full_art.get("medium", default),
			"Location: ": full_art.get("location_description", default),
			"Distance from you: ": "%.2f" % art_piece.get("distance") + " miles"
		})

	return list


def parse_five_shortest(user_zip):
	user_location = find_users_long_lat(user_zip)
	dist_from_art_to_user = find_distance_between_art_and_user(user_location)
	sorted_distances = sort_art_distances(dist_from_art_to_user)
	top_five_shortest_distances = sorted_distances[0:5]	
	art_data = parse_art_data(top_five_shortest_distances)
	return art_data


def print_top_five_results():
	result = []
	default = "N/A"
	
	top_five = parse_five_shortest()

	for art in top_five:
		#add print "Here are you results:"
		print "=========="
		for key, value in art.items():
			print key + value
		print "=========\n"



def main():
	while True:
		choice = menu_choice()

		if choice == 0:
			continue 

		elif choice == 1:
			print_top_five_results()

		elif choice == 2: 		
			break

if __name__ == '__main__':
	main()	