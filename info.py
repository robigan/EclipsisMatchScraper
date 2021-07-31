from pymongo import MongoClient
import os
import json
from tabulate import tabulate


def main():
    print("This is a small command line utility for quickly prototyping, note that the scraper can only scrape from 2019-03-07 and onwards")

    with open(os.getcwd() + "/secret.hidden.json") as json_file:  # Get config file
        config = json.load(json_file)
        json_file.close()

    client = MongoClient(config["conn_url"], serverSelectionTimeoutMS=5000)
    db = client['eclipsis-database']
    col = db["matches"]

    username = input("Roblox Username to search: ")

    count = col.count_documents({"teams.players.username": username})
    wins = col.count_documents({"teams": {"$elemMatch": { "players.username": username, "won": True }}})
    loses = col.count_documents({"teams": {"$elemMatch": { "players.username": username, "won": False }}})

    info = []
    info.append(["Matches in DB: ", str(count)])
    info.append(["Wins: ", str(wins)])
    info.append(["Losses: ", str(loses)])
    info.append(["W/L Ratio: ", str(float(round((wins/loses)*100))/100)])

    print(tabulate(info))

if __name__ == "__main__":
    main()
