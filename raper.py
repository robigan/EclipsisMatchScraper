import requests
import json
from pymongo import MongoClient
import regex


def main():
    with open("/home/robigan/Documents/Source/EclipsisMatchScraper/secret.hidden.json") as json_file:
        config = json.load(json_file)
        json_file.close()

    #client = MongoClient(config["conn_url"], serverSelectionTimeoutMS=5000)
    #db = client['eclipsis-database']
    #col = db["matches"]

    r = requests.get(config["url"], params=config["getOptions"], headers=config["headers"])
    data = r.json()

    limit = config["getOptions"]["limit"]
    success = 0

    Usernames = []
    Durations = []
    Ratings = []

    for Match in data:
        UsernamesInMatch = regex.findall("(?<=:arrow_down: |:arrow_down_small: |:trophy::arrow_up_small: |:trophy::arrow_up: |#:arrow_double_down: |:trophy::arrow_double_up: ).*?(?= [[])", str(Match))
        DurationInMatch = regex.findall("(?<=\w [[]).*?(?=[]])", str(Match))
        RatingInMatch = regex.findall("(?<=]: ).*?(?= [-+])", str(Match))
        if (len(UsernamesInMatch) == len(DurationInMatch) == len(RatingInMatch)):
            success += 1
            print(len(UsernamesInMatch), len(DurationInMatch), len(RatingInMatch), " Matched")
        else:
            print(len(UsernamesInMatch), len(DurationInMatch), len(RatingInMatch))

    print("Parsing success rate stats: " + str((success / limit) * 100) + str("%"))
    # Usernames = regex.findall("(?<=:arrow_down: |:arrow_down_small: |:trophy::arrow_up_small: |:trophy::arrow_up: |#:arrow_double_down: |:trophy::arrow_double_up: ).*?(?= [[])", r.text)
    #Durations = regex.findall("(?<=\w [[]).*?(?=[]])", r.text)
    #Ratings = regex.findall("(?<=]: ).*?(?= [-+])", r.text)

    #massWrite = []

    # for message in data:
    # formatted = {
    # "_id": message["id"]
    # }
    # massWrite.append()


if __name__ == "__main__":
    main()
