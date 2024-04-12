# YT : @ultroidofficial
# Copyright (c) 2023 WOODcraft
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHAT


keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="❈ 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 ❈", callback_data="gensession")],
        [
            InlineKeyboardButton(text="❈ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ❈", url="https://t.me/SUPPORT_CHAT"),
            InlineKeyboardButton(
                text="❈ Channel ❈", url="https://t.me/Ultroid_official"
            ),
        ],
    ]
)

gen_key = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="❣️ 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐯1 ❣️", callback_data="pyrogram1"),
            InlineKeyboardButton(text="🦋 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐯2 🦋", callback_data="pyrogram"),
        ],
        [InlineKeyboardButton(text="🌼 𝐓𝐞𝐥𝐞𝐭𝐡𝐨𝐧 🌼", callback_data="telethon")],
    ]
)

retry_key = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="⚡️ 𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧 ⚡️", callback_data="gensession")]]
)
