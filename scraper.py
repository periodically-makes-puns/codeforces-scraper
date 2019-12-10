from urllib.request import urlopen
from urllib.parse import quote_plus as urlencode
import json
from exceptions import * # Include custom exceptions.


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
                "maxRank": result["maxRank"]
            }

def get_color(rank: str) -> str:
    if "grandmaster" in rank: return "red"
    elif "candidate master" == rank: return "#aoa"
    elif "master" in rank: return "#ff8c00"
    elif "expert" == rank: return "blue"
    elif "specialist" == rank: return "#03a89e"
    elif "pupil" == rank: return "green"
    else: return "gray"