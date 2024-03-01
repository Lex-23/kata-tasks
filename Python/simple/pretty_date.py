"""
Overview
Write a helper function that accepts an argument (Ruby: a Time object / Others: number of seconds) 
and converts it to a more human-readable format. You need only go up to '_ weeks ago'.

to_pretty(0) => "just now"

to_pretty(40000) => "11 hours ago"
Specifics
The output will be an amount of time, t, included in one of the following phrases: 
"just now", "[t] seconds ago", "[t] minutes ago", "[t] hours ago", "[t] days ago", "[t] weeks ago".
You will have to handle the singular cases. That is, when t = 1, the phrasing will be one of "a second ago", 
"a minute ago", "an hour ago", "a day ago", "a week ago".
The amount of time is always rounded down to the nearest integer. 
For example, if the amount of time is actually 11.73 hours ago, the return value will be "11 hours ago".
Only times in the past will be given, with the range "just now" to "52 weeks ago"
"""

import math

def to_pretty(seconds: int):
    minute = 60
    hour = 3600
    day = 86400
    week = 604800
    
    TIME_CONVERSION_MAP = {
        lambda x: x < minute: ("second", (lambda x: x)),
        lambda x: minute <= x < hour: ("minute", (lambda x: math.floor(x / 60))),
        lambda x: hour <= x < day: ("hour", (lambda x: math.floor(x / 3600))),
        lambda x: day <= x < week: ("day", (lambda x: math.floor(x / (3600 * 24)))),
        lambda x: x >= week: ("week", (lambda x: math.floor(x / (3600 * 24 * 7)))),
    }

    def convert_time(time_int: int, time_word: str):
        if time_int == 1:
            return f"an {time_word} ago" if time_word == "hour" else f"a {time_word} ago"
        return f"{time_int} {time_word}s ago"
    

    if seconds == 0:
        return "just now"
    
    for time_check, (word, time_conversion) in TIME_CONVERSION_MAP.items():
        if time_check(seconds):
            return convert_time(time_conversion(seconds), word)

# print(to_pretty(23543534636))
        