import requests
import time
import json

""" This program is by Tweeticoats and is used to submit timestamps"""

url = "http://localhost:9999/api/scene/list"

request_config = {
    "dlState": "any",
    "cardSize": "1",
    "lists": [],
    "isAvailable": None,
    "isAccessible": None,
    "isWatched": None,
    "releaseMonth": "",
    "cast": [],
    "sites": [],
    "tags": [],
    "cuepoint": [],
    "volume": 0,
    "sort": "release_desc",
    "offset": 0,
    "limit": 1,
}


def submit_web(s):
    s.post("https://timestamp.trade/submit-xbvr2", json=s)


def submit_timestamp():
    response = requests.post(url, json=request_config)
    if response.status_code == 200:
        #    print(response.json())
        result = response.json()
        results = result["results"]
        request_config["limit"] = 100
        request_config["offset"] = 0
        submit_s = requests.Session()
        request_s = requests.Session()
        while request_config["offset"] < results:
            response = request_s.post(url, json=request_config)
            for s in response.json()["scenes"]:
                for k in [
                    "id",
                    "file",
                    "_score",
                    "history",
                    "favourite",
                    "is_watched",
                    "has_preview",
                    "is_scripted",
                    "last_opened",
                    "star_rating",
                    "is_available",
                    "is_multipart",
                    "needs_update",
                    "edits_applied",
                    "is_accessible",
                    "total_file_size",
                    "total_watch_time",
                    "created_at",
                    "watchlist",
                    "is_subscribed",
                    "is_hidden",
                ]:
                    s.pop(k)
                s["tags"] = [{"name": x["name"]} for x in s["tags"]]
                s["cast"] = [{"name": x["name"]} for x in s["cast"]]

                print(s)
                submit_web(s)
            request_config["offset"] = (
                request_config["offset"] + request_config["limit"]
            )
            print("--" + str(request_config["offset"]))
            submit_s.close()
            time.sleep(10)


def main():
    response = requests.post(url, json=request_config)
    if response.status_code == 200:
        #    print(response.json())
        result = response.json()
        with open("../scratch/response.json", "w") as file:
            json.dump(result, file, indent=4)
        results = result["results"]
        request_config["limit"] = 100
        request_config["offset"] = 0
        submit_s = requests.Session()
        request_s = requests.Session()
        while request_config["offset"] < results:
            response = request_s.post(url, json=request_config)
            for s in response.json()["scenes"]:
                for k in [
                    "id",
                    "file",
                    "_score",
                    "history",
                    "favourite",
                    "is_watched",
                    "has_preview",
                    "is_scripted",
                    "last_opened",
                    "star_rating",
                    "is_available",
                    "is_multipart",
                    "needs_update",
                    "edits_applied",
                    "is_accessible",
                    "total_file_size",
                    "total_watch_time",
                    "created_at",
                    "watchlist",
                    "is_subscribed",
                    "is_hidden",
                ]:
                    s.pop(k)
                s["tags"] = [{"name": x["name"]} for x in s["tags"]]
                s["cast"] = [{"name": x["name"]} for x in s["cast"]]

                print(s)
            #      submit_web(s)
            request_config["offset"] = (
                request_config["offset"] + request_config["limit"]
            )
            print("--" + str(request_config["offset"]))
            submit_s.close()
            time.sleep(10)


if __name__ == "__main__":
    main()
