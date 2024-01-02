import PySimpleGUI as sg
import requests
import json
import time
from pathlib import Path


def create_layout(address: str, port: str) -> list[list]:
    """
    Create the layout for the PySimpleGUI window.

    :param address: The default IP address to display.
    :param port: The default port to display.
    :return: A list of lists representing the layout for the GUI.
    """
    layout = [
        [sg.Text("Timestamp Helper", font=("Helvetica", 16))],
        [
            sg.Text("IP Address: http://"),
            sg.InputText(default_text=address, pad=0, size=20, key="-IP-"),
            sg.Text("Port:"),
            sg.InputText(default_text=port, pad=0, size=5, key="-PORT-"),
        ],
        [
            sg.Text("Number of Scenes:"),
            sg.Text(text="", key="-NUMBER_OF_SCENES-"),
            [sg.Text("Current Timestamp:"), sg.Text(text="", key="-TIMESTAMP-")],
            [sg.Button("Get Scenes")],
            [sg.Button("Process Timestamp")],
            [sg.Image(key="ImagePlaceholder")],  # Placeholder for image
        ],
    ]
    return layout


def get_scene_count(url: str, config: dict, debug: bool = False) -> int:
    """
    Get the number of scenes from the specified URL using the provided configuration.

    :param url: The URL to fetch data from.
    :param config: Configuration dictionary for the request.
    :param debug: Flag to enable debug output.
    :return: The number of scenes.
    """
    response = requests.post(url, json=config)
    if response.status_code == 200:
        result = response.json()
        response_file = Path("../scratch/response.json")
        with response_file.open("w") as file:
            json.dump(result, file, indent=4)
        result_count = result["results"]
        if debug:
            print(f"{result_count=}")
        return result_count
    else:
        return 0


def load_settings() -> dict[str, str]:
    """
    Load settings from a JSON file.

    :return: A dictionary with settings. Defaults are provided if the file does not exist.
    """
    settings_file = Path("settings.json")
    default_settings = {"server_url": "localhost", "port": "9999"}

    settings = None
    if settings_file.is_file():
        with settings_file.open("r") as file:
            settings = json.load(file)
    if settings is not None:
        if settings["server_url"] is None:
            settings["server_url"] = default_settings["server_url"]
        if settings["port"] is None:
            settings["port"] = default_settings["port"]
    else:
        settings = default_settings

    return settings


def process_timestamps(scene_list_api, request_config):
    response = requests.post(scene_list_api, json=request_config)
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
        # while request_config["offset"] < results:
        while request_config["offset"] < results and request_config["offset"] < 10:
            response = request_s.post(scene_list_api, json=request_config)
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


def save_settings(settings: dict[str, str]) -> None:
    """
    Save settings to a JSON file.

    :param settings: A dictionary containing the settings to save.
    """
    settings_file = Path("settings.json")
    with settings_file.open("w") as file:
        json.dump(settings, file, indent=4)


def submit_web(s):
    s.post("https://timestamp.trade/submit-xbvr2", json=s)


def submit_timestamp(url, config):
    response = requests.post(url, json=config)
    if response.status_code == 200:
        #    print(response.json())
        result = response.json()
        results = result["results"]
        config["limit"] = 100
        config["offset"] = 0
        submit_s = requests.Session()
        request_s = requests.Session()
        while config["offset"] < results:
            response = request_s.post(url, json=config)
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
                # submit_web(s)
            config["offset"] = config["offset"] + config["limit"]
            print("--" + str(config["offset"]))
            submit_s.close()
            time.sleep(10)


def main():
    """
    Main function to execute the application.
    """
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
    settings = load_settings()
    url = settings["server_url"]
    port = settings["port"]
    scene_list_api = f"http://{url}:{port}/api/scene/list"

    layout = create_layout(address=url, port=port)
    window = sg.Window(title="Timestamp Helper", layout=layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            window.refresh()
            settings = {
                "server_url": window["-IP-"].get(),
                "port": window["-PORT-"].get(),
            }
            save_settings(settings)
            break
        elif event == "Process Timestamp":
            # Implement logic for "Get Timestamp" event
            process_timestamps(
                scene_list_api=scene_list_api, request_config=request_config
            )
        elif event == "Get Scenes":
            number_of_scenes = get_scene_count(
                url=scene_list_api, config=settings, debug=True
            )
            window["-NUMBER_OF_SCENES-"].update(number_of_scenes)

    window.close()


if __name__ == "__main__":
    main()
