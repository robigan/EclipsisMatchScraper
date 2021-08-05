from pymongo import MongoClient
import os
import json
from tabulate import tabulate
import sys
import termplotlib as tpl

def help():
    print("Usage: program.py {info|match} {username}")

def validateArgs():
    try:
        if not (sys.argv[1] == "info") or (sys.argv[2] == ""):
            print("Please pass a valid option into CLI")
            help()
            exit(1)
    except:
        print("Please pass args into the CLI")
        help()
        exit(1)

    return str(sys.argv[1]), str(sys.argv[2])

def main():
    print("This is a small command line utility for quickly prototyping, note that the scraper can only scrape from 2019-03-07 and onwards")

    with open(os.getcwd() + "/secret.hidden.json") as json_file:  # Get config file
        config = json.load(json_file)
        json_file.close()

    client = MongoClient(config["conn_url"], serverSelectionTimeoutMS=5000)
    db = client['eclipsis-database']
    col = db["matches"]

    type, username = validateArgs()

    if type == "info":
        count = col.count_documents({"teams.players.username": username})
        wins = col.count_documents(
            {"teams": {"$elemMatch": {"players.username": username, "won": True}}})
        loses = col.count_documents(
            {"teams": {"$elemMatch": {"players.username": username, "won": False}}})
        matches = list(col.find({"teams.players.username": username}).sort(
            "teams.players.username", -1).limit(20))

        print()

        if count != 0:
            info = []
            info.append(["Matches in DB: ", str(count)])
            info.append(["Wins: ", str(wins)])
            info.append(["Losses: ", str(loses)])
            info.append(["W/L Ratio: ", str('%.2f' % (wins/loses))])

            print(tabulate(info, headers=["Stats for:", "robigan"], numalign="left", stralign="right"))

            amounts = []
            change = []

            for Match in matches:
                Found = False
                for Team in Match["teams"]:
                    if Found:
                        break
                    for Player in Team["players"]:
                        if Player["username"] == username:
                            Found = True
                            amounts.append(Player["new_rating"])
                            change.append("Rating:" + str(Player["rating_change"]))
                            break

            """graphY = [[str(highest)], [str(lowest + step*9)], [str(lowest + step*8)], [str(lowest + step*7)], [str(lowest + step*6)], [str(lowest + step*5)], [str(lowest + step*4)], [str(lowest + step*3)], [str(lowest + step*2)], [str(lowest + step)], [str(lowest)]]

            print(tabulate(graphY, tablefmt="plain"))"""
            fig = tpl.figure()
            fig.barh(amounts, change, force_ascii=True)
            fig.show()

        else:
            print("No data on user " + username)


if __name__ == "__main__":
    main()
