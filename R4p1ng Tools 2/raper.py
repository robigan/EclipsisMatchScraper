import requests
import json

def main():
    with open("secret.hidden.json") as json_file:
        data = json.load(json_file)
        json_file.close()

    r = requests.get(data.url, params=data.getOptions, headers=data.headers)

    print(r.url)
    print(r.text)

if __name__ == "__main__":
    main()