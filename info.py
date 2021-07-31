from pymongo import MongoClient
import os
import json


def main():
    print("This is a small command line utility for quickly prototyping, note that the scraper can only scrape from 2019-03-07 and onwards")

    with open(os.getcwd() + "/secret.hidden.json") as json_file:  # Get config file
        config = json.load(json_file)
        json_file.close()

    client = MongoClient(config["conn_url"], serverSelectionTimeoutMS=5000)
    db = client['eclipsis-database']
    col = db["matches"]

    while True:
        option = input("Type of operation to execute (Possible types are: W/L, Count, Exit): ")
        option = option.lower()

        print()

        if option == "count":
            print("You have chose Count operation")
            username = input("Roblox Username to run the operation upon: ")
            print("Number of matches for user " + username + " are " + str(col.count_documents({"teams.players.username": username})))

        elif option == "w/l":
            print("You have chose W/L operation")
            username = input("Roblox Username to run the operation upon: ")
            wins = col.count_documents({"teams": {"$elemMatch": { "players.username": username, "won": True }}})
            loses = col.count_documents({"teams": {"$elemMatch": { "players.username": username, "won": False }}})
            print(username + " = " + str(wins/loses) + " W/L")

        elif option == "exit":
            exit(0)
        else:
            print("Option not available...")

        print()

if __name__ == "__main__":
    main()
