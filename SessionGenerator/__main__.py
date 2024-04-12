# Copyright (c) 2023 WOODcraft
import asyncio
import importlib

from pyrogram import idle

from SessionGenerator import LOGGER, Opleech
from SessionGenerator.modules import ALL_MODULES


async def Opleech_boot():
    try:
        await Opleech.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("SessionGenerator.modules." + all_module)

    LOGGER.info(f"@{Opleech.username} Started.")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(Opleech_boot())
    LOGGER.info("Stopping String Gen Bot... ! help : t.me/ultroidofficial_chat")
