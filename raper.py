import requests
import json
from pymongo import MongoClient
import regex

def main():
    with open("/home/robigan/Documents/Source/EclipsisMatchScraper/R4p1ng Tools 2/secret.hidden.json") as json_file:
        config = json.load(json_file)
        json_file.close()

    #client = MongoClient(config["conn_url"], serverSelectionTimeoutMS=5000)
    #db = client['eclipsis-database']
    #col = db["matches"]

    r = requests.get(
        config["url"], params=config["getOptions"], headers=config["headers"])
    #data = json.load(r.json())

    print(regex.findall("(?<=:arrow_down: |:arrow_down_small: |:trophy::arrow_up_small: |:trophy::arrow_up: |:arrow_double_down: |:trophy::arrow_double_up: ).*?(?= [[])", r.text))
    print(regex.findall("(?<=\w [[]).*?(?=[]])", r.text))
    print(regex.findall("(?<=]: ).*?(?= [-+])", r.text))

    #massWrite = []

    # for message in data:
    # formatted = {
    # "_id": message["id"]
    # }
    # massWrite.append()


if __name__ == "__main__":
    main()
