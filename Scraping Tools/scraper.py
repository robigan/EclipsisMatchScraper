from datetime import datetime   # Used to convert the scraped time into a datetime object
from tabulate import tabulate   # Used to create pretty tables
import json
import re

results_table = []              # Stores the pretty table
match_number = 0                # Counts the number of matches in the .json file

def prettyTime(iso_timestamp):
    timestamp = datetime.strptime(iso_timestamp, '%Y-%m-%dT%H:%M:%S.%f+00:00')      # Convert the scraped timestamp into a datetime object
    timestamp = timestamp.strftime('%D, %H:%M')                                     # Output the datatime object into something more a e s t h e t i c
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

        outcome = "WON" if outcome == "+" else "LOST"

        results_table.append([prettyTime(iso_timestamp), username, outcome, time, rating, match_number])

if __name__ == "__main__":
    with open('data.json') as json_file:        # Load the .json into memory
        data = json.load(json_file)

    for message in data:                        # Loop for every match in the .json
        match_number += 1                       
        iso_timestamp = message["timestamp"]
        scrape(str(message))   

    results_table.append([0,0,0,0,0,0])         # Fixes formatting on the last piece of data

    print(tabulate(results_table, headers=["Timestamp", "Username", "Outcome", "Time", "Rating", "Match No."]))
    
    
