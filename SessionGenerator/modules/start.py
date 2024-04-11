# Generate Session In Your Telegram premium @Opleech
# Copyright (c) 2023 WOODcraft
from pyrogram import filters
from pyrogram.types import Message

from SessionGenerator import Opleech
from SessionGenerator.utils import add_served_user, keyboard


@Opleech.on_message(filters.command("start") & filters.private & filters.incoming)
async def f_start(_, message: Message):
    await message.reply_text(
        text=f"🦋 Hey {message.from_user.first_name},\n\n⌘ This is {Opleech.mention},\nAn open source string session generator bot, written in python with the help of pyrogram ].",
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    await add_served_user(message.from_user.id)
