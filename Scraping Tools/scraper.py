from datetime import datetime   # Used to convert the scraped time into a datetime object
from tabulate import tabulate   # Used to create pretty tables
import json
import re
import time
import hashlib

iso_timestamp = 0
results_table = []              # Stores the pretty table
match_number = 0                # Counts the number of matches in the .json file
team = True
rated = False
mode = ""
export = []

def prettyTime(iso_timestamp):
    timestamp = datetime.strptime(iso_timestamp, '%Y-%m-%dT%H:%M:%S.%f+00:00')      # Convert the scraped timestamp into a datetime object
    timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S')                                     # Output the datatime object into something more a e s t h e t i c
    return timestamp

def scrape(source):
    username_pattern_start = re.compile(":arrow_down:|:arrow_down_small:|:trophy::arrow_up_small:|:trophy::arrow_up:|:arrow_double_down:|:trophy::arrow_double_up:")
    username_pattern_end = re.compile("[[]\w")
    time_pattern_end = re.compile("\w]:")
    rating_pattern_end = re.compile("\s[+-]\d")

    # The following gets the character positions for the statements above
    username_starts = [m.end() for m in username_pattern_start.finditer(str(source))]
    username_ends = [m.start() for m in username_pattern_end.finditer(str(source))]
    time_ends = [m.start() for m in time_pattern_end.finditer(str(source))]
    rating_ends = [m.start() for m in rating_pattern_end.finditer(str(source))]

    # Repeat for every user found in the match
    for i in range (len(username_starts)):
        # Use character positions to isolate the content
        username = source[username_starts[i] +1 : username_ends[i] -1]
        time = source[username_ends[i] +1 : time_ends[i] +1]
        rating = source[time_ends[i] +4 : rating_ends[i]]
        outcome = source[rating_ends[i] +1 : rating_ends[i] +2]
        rating_gain = source[rating_ends[i] +1 : rating_ends[i] + 4]

        rating_gain = int(re.sub("[^0-9|+-]", "", rating_gain))

        outcome = True if outcome == "+" else False

        try:                                                # Trial and error be like
            time = datetime.strptime(time,"%Mm %Ss")
        except:
            try:
                time = datetime.strptime(time,"%Hh %Mm %Ss")
            except:
                try:
                    time = datetime.strptime(time,"%Hh %Ss")
                except:
                    try:
                        time = datetime.strptime(time,"%Ss")
                    except:
                        try:
                            time = datetime.strptime(time,"%Mm")
                        except:
                            try:
                                time = datetime.strptime(time,"%Hh")
                            except:
                                time = datetime.strptime(time,"%Hh %Mm %Ss")
        time = time.strftime("%H:%M:%S")
                        

        results_table.append([prettyTime(iso_timestamp), username, outcome, time, rating, rating_gain, rated, mode])

        hash = hashlib.md5()
        hash.update((username+prettyTime(iso_timestamp)).encode('utf-8'))
        id = str(int(hash.hexdigest(), 16))[0:8]
        print(id)

        #export.append({"_id":int(id), "username":username, "rating":rating, "matches":[{"date":iso_timestamp, "time":time, "won":outcome, "rating":rating, "rating_gained":rating_gain, "match_type":{"mode":mode, "rated":rated}}]})
        export.append({"_id":int(id), "date":prettyTime(iso_timestamp),"username":username, "new_rating":int(rating)+int(rating_gain), "won":outcome, "rating_gain":rating_gain, "time":time, "mode":mode, "rated":rated})

if __name__ == "__main__":
    with open('data.json') as json_file:        # Load the .json into memory
        data = json.load(json_file)
    t0 = time.time()
    for message in data:                        # Loop for every match in the .json
        player_count = 0
        match_number += 1                       
        iso_timestamp = message["timestamp"]

        match_type_data = message["embeds"][0]["fields"][len(message["embeds"][0]["fields"])-1]["value"]
        rated = True if "Rated" in match_type_data else False
        mode = "team" if "Team" in match_type_data else "solo"


        scrape(str(message))   
    t1 = time.time()


    #print(tabulate(results_table, headers=["Timestamp", "Username", "Outcome", "Time", "Rating", "Rating Gain", "Rated", "Mode"]))
    print("TIME:", t1-t0)
    t0= time.time()
    #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    print(export)