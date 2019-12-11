from urllib.request import urlopen
from urllib.parse import quote_plus as urlencode
from datetime import datetime
import json
from exceptions import * # Include custom exceptions.
import numpy as np

def filter_handle(handle: str) -> str:
    return "".join(filter(lambda c: c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-", handle))

def get_information(handle: str) -> dict:
    handle = filter_handle(handle)
    if len(handle) > 24 or len(handle) < 3:
        raise InvalidLengthException()
    url = "https://codeforces.com/api/user.info?handles=" + handle
    with urlopen(url) as req:
        result = json.load(req)
    if result["status"] == "FAILED":
        raise NoSuchUserException()
    else:
        assert result["status"] == "OK"
        result = result["result"][0]
        if "rating" not in result:
            raise NoRatingException()
        else:
            return {
                "rating": result["rating"],
                "maxRating": result["maxRating"],
                "rank": result["rank"],
                "maxRank": result["maxRank"],
                "registrationTime": result["registrationTimeSeconds"]
            }

def get_rating_data(handle: str, startTime: int) -> str:
    handle = filter_handle(handle)
    if len(handle) > 24 or len(handle) < 3:
        raise InvalidLengthException()
    url = "https://codeforces.com/api/user.rating?handle=" + handle
    with urlopen(url) as req:
        result = json.load(req)
    if result["status"] == "FAILED":
        raise NoSuchUserException()
    else:
        assert result["status"] == "OK"
        result = result["result"]
        result = [(datetime.fromtimestamp(startTime), 1500)] \
            + [(datetime.fromtimestamp(entry["ratingUpdateTimeSeconds"]), entry["newRating"]) for entry in result]
        return np.transpose(result)

def get_color(rank: str) -> str:
    if "grandmaster" in rank: return "red"
    elif "candidate master" == rank: return "violet"
    elif "master" in rank: return "orange"
    elif "expert" == rank: return "blue"
    elif "specialist" == rank: return "cyan"
    elif "pupil" == rank: return "green"
    else: return "gray"