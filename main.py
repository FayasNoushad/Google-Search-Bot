# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import requests
from pyrogram import Client


API = "https://api.abirhasan.wtf/google?query="


Bot = Client(
    "PyPi-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


def google(query):
    query = query.replace(" ", "+")
    r = requests.get(API + query)
    info = r.json()
    informations = info["results"]
    results = []
    for info in informations:
        text = f"**Title:** `{info['title']}`"
        text += f"\n**Description:** `{info['description']}`"
        results.append({"text": text, "link": info['link']})
    return results


Bot.run()
