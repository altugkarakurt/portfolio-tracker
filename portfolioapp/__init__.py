import json
import os


if(not os.path.exists("./config.json")):
    raise FileNotFoundError("The configuration file doesn't exist")

with open("./config.json") as configfile:
    portfolioapp_config = json.load(configfile)
