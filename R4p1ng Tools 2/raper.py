import requests
import json
from pymongo import MongoClient

def main():
    with open("/home/robigan/Documents/Source/EclipsisMatchScraper/R4p1ng Tools 2/secret.hidden.json") as json_file:
        config = json.load(json_file)
        json_file.close()

    client = MongoClient(config["conn_url"], serverSelectionTimeoutMS=5000)
    db = client['eclipsis-database']
    col = db["matches"]

    r = requests.get(config["url"], params=config["getOptions"], headers=config["headers"])


if __name__ == "__main__":
    main()