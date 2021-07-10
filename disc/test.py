import re


url_regex = re.compile(r"http[s]*://(open.)*spotify.com/track/[\w?=]*")

message = """
Look at this cool song: https://open.spotify.com/track/6RKGBcDtgzXx21zUjpeu6F?si=9afdb7358d0141a5 it's really good
"""

message = """
Look at this cool song: https://open.spotify.com/track/6RKGBcDtgzXx21zUjpeu6F?si=9afdb7358d0141a5. it's really good
"""

re.search()