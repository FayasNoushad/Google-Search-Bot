# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import requests
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import *

API = "https://api.abirhasan.wtf/google?query="


Bot = Client(
    "Google-Search-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


START_TEXT = """Hello {}
I am a google search bot.

> `I can search from google. Use me in inline.`

Made by @FayasNoushad"""

JOIN_BUTTON = [
    InlineKeyboardButton(
        text='⚙ Join Updates Channel ⚙',
        url='https://telegram.me/FayasNoushad'
    )
]


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        reply_markup=InlineKeyboardMarkup([JOIN_BUTTON]),
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_inline_query()
async def inline(bot, update):
    results = google(update.query)
    answers = []
    for result in results:
        answers.append(
            InlineQueryResultArticle(
                title=result["title"],
                description=result["description"],
                input_message_content=InputTextMessageContent(
                    message_text=result["text"],
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="Link", url=result["link"])],
                        JOIN_BUTTON
                    ]
                )
            )
        )
                


def google(query):
    r = requests.get(API + requote_uri(query))
    informations = r.json()["results"]
    results = []
    for info in informations:
        text = f"**Title:** `{info['title']}`"
        text += f"\n**Description:** `{info['description']}`"
        text += f"\n\nMade by @FayasNoushad"
        results.append(
            {
                "title": info['title'],
                "description": info['description'],
                "text": text,
                "link": info['link']
            }
        )
    return results


Bot.run()
