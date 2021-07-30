import requests
import json
from pymongo import MongoClient
import time
from scraper_v3 import Scraper

def shave(data):  # Trims returned data
    newData = []
    for Message in data:
        formatted = {}
        formatted["id"] = Message["id"]
        formatted["timestamp"] = Message["timestamp"]
        formatted["embeds"] = Message["embeds"]
        newData.append(formatted)
    return newData


def getData(url, getOptions, headers):  # Gets a trimmed down version of the data
    data = {}
    while True:
        r = requests.get(
            url, params=getOptions, headers=headers)
        if str(headers["authorization"]).startswith("Bot "): 
            time.sleep(0.5)
        else:
            time.sleep(2.5)
        decoded = r.json()
        if r.status_code == 429:
            print("Getting ratelimited, ratelimit retry_after is " + str(decoded.retry_after))
            time.sleep(decoded.retry_after + 5)
        else:
            data = shave(decoded)
            break
    return data


def main():  # Main loop
    scraped_msg_count = 0
    with open("/root/EclipsisMatchScraper/secret.hidden.json") as json_file:  # Get config file
        config = json.load(json_file)
        json_file.close()

    # Gets the target collection of the db
    client = MongoClient(config["conn_url"], serverSelectionTimeoutMS=5000)
    db = client['eclipsis-database']
    col = db["matches"]

    latest = list(col.find({"_id": {"$gte": "553182269070901259"}}).sort(
        "_id", -1).limit(1))  # Gets the after offset
    if len(latest) == 0:
        latest = "553180587528290316"
    else:
        latest = latest[0]["_id"]

    getOptions = config["getOptions"]
    getOptions["after"] = latest

    s = Scraper()

    while True:  # While loop to keep recursively updating the db
        print("Fetching and Scraping...")
        data = getData(config["url"], getOptions, config["headers"])
        scraped_msg_count += len(data)
        # If the db contains the returned data, then exit
        if col.find_one({"_id": data[0]["id"]}) != None:
            print("❌ Database contains newly scraped data, exiting...")
            exit()
        else:
            # Scrape here the data, and then dump
            data = s.scrape(data)
            print(f"⚠️ Inserting {str(len(data))} matches... [{scraped_msg_count} in total]")
            col.insert_many(data, ordered=False)
            getOptions["after"] = data[0]["_id"]
        print("\n")

if __name__ == "__main__":
    main()
