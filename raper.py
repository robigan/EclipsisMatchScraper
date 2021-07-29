import requests
import json
from pymongo import MongoClient


def shave(data):
    newData = []
    for Message in data:
        formatted = {}
        formatted["id"] = Message["id"]
        formatted["embeds"] = Message["embeds"]
        newData.append(formatted)
    return newData


def getData(url, getOptions, headers):
    r = requests.get(
        url, params=getOptions, headers=headers)
    data= r.json()
    data= shave(data)
    return data

def main():
    with open("/home/robigan/Documents/Source/EclipsisMatchScraper/secret.hidden.json") as json_file:
        config= json.load(json_file)
        json_file.close()

    client= MongoClient(config["conn_url"], serverSelectionTimeoutMS=5000)
    db= client['eclipsis-database']
    col= db["matches"]

    latest = list(col.find({"_id": {"$gte": "553182269070901259"}}).sort("_id", -1).limit(1))[0]["_id"]

    getOptions= config["getOptions"]
    getOptions["after"]= latest

    data= getData(config["url"], getOptions, config["headers"])

    print(data)

if __name__ == "__main__":
    main()
