# Generate Session In Your Telegram premium @Opleech
# Copyright (c) 2023 WOODcraft
import asyncio

from pyrogram import Client, filters
from oldpyro import Client as Client1
from oldpyro.errors import ApiIdInvalid as ApiIdInvalid1
from oldpyro.errors import PasswordHashInvalid as PasswordHashInvalid1
from oldpyro.errors import PhoneCodeExpired as PhoneCodeExpired1
from oldpyro.errors import PhoneCodeInvalid as PhoneCodeInvalid1
from oldpyro.errors import PhoneNumberInvalid as PhoneNumberInvalid1
from oldpyro.errors import SessionPasswordNeeded as SessionPasswordNeeded1
from pyrogram.errors import (
    ApiIdInvalid,
    FloodWait,
    PasswordHashInvalid,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    SessionPasswordNeeded,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from pyromod.listen.listen import ListenerTimeout

from config import SUPPORT_CHAT
from SessionGenerator import Opleech
from SessionGenerator.utils import retry_key


async def gen_session(
    message, user_id: int, telethon: bool = False, old_pyro: bool = False
):
    if telethon:
        ty = f"Telethon"
    elif old_pyro:
        ty = f"Pyrogramm V1"
    else:
        ty = f"Pyrogram V2"

    await message.reply_text(f"Trying to start {ty} Session generator...")

    try:
        api_id = await Opleech.ask(
            identifier=(message.chat.id, user_id, None),
            text="❖ Please enterr your API_ID to proceed:",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Opleech.send_message(
            user_id,
            "Time limits reached of 5 minutes\n\n❖ Please start generating session again.",
            reply_markup=retry_key,
        )

    if await cancelled(api_id):
        return

    try:
        api_id = int(api_id.text)
    except ValueError:
        return await Opleech.send_message(
            user_id,
            "The API_ID you sent is invalid.\n\n❖ Please start generating session again.",
            reply_markup=retry_key,
        )

    try:
        api_hash = await Opleech.ask(
            identifier=(message.chat.id, user_id, None),
            text="❖ Now enter your API_HASH to proceed √",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Opleech.send_message(
            user_id,
            "Time limits reached of 5 minutes.\n\n❖ Please start generating session again.",
            reply_markup=retry_key,
        )

    if await cancelled(api_hash):
        return

    api_hash = api_hash.text

    if len(api_hash) < 30:
        return await Opleech.send_message(
            user_id,
            "he API_HASH you sent is invalid.\n\n❖ Please start generating session again.",
            reply_markup=retry_key,
        )

    try:
        phone_number = await Opleech.ask(
            identifier=(message.chat.id, user_id, None),
            text="❖ Please send your phone number in international format like +9113138737832 :",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Opleech.send_message(
            user_id,
            "Time limits reached of 5 minutes.\n\n❖ Please start generating session again..",
            reply_markup=retry_key,
        )

    if await cancelled(phone_number):
        return
    phone_number = phone_number.text

    await Opleech.send_message(user_id, "❖ Trying to send OTP at the given number...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="Opleech", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()

    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
        await asyncio.sleep(1)

    except FloodWait as f:
        return await Opleech.send_message(
            user_id,
            f"Failed to send code for login.\n\n❖ Plese wait for {f.value or f.x} seconds and try again",
            reply_markup=retry_key,
        )
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        return await Opleech.send_message(
            user_id,
            "API_ID or API_HASH is invalid.\n\n❖ Please start generating your session again..",
            reply_markup=retry_key,
        )
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        return await Opleech.send_message(
            user_id,
            "Phone number is invalid.\n\n❖ Please start generating your session again...",
            reply_markup=retry_key,
        )

    try:
        otp = await Opleech.ask(
            identifier=(message.chat.id, user_id, None),
            text=f"❖ Please enter the OTP sent to {phone_number}.\n\n❖ If OTP is <code>12345</code>, Please sent it as <code>1 2 3 4 5.</code>",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(otp):
            return
    except ListenerTimeout:
        return await Opleech.send_message(
            user_id,
            "Time limits reached of 10 minutes\n\n❖ Please start generating your session again..",
            reply_markup=retry_key,
        )

    otp = otp.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, otp, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, otp)
    except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
        return await Opleech.send_message(
            user_id,
            "The OTP you've sent is  <b>wrong.</b>\n\n❖ Please start generating your session again...",
            reply_markup=retry_key,
        )
    except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
        return await Opleech.send_message(
            user_id,
            "The OTP you've sent is  <b>expired.</b>\n\n❖ Please start generating your session again..",
            reply_markup=retry_key,
        )
    except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
        try:
            pwd = await Opleech.ask(
                identifier=(message.chat.id, user_id, None),
                text="❖ Please enter the 2 step verificaton password to continue √",
                filters=filters.text,
                timeout=300,
            )
        except ListenerTimeout:
            return Opleech.send_message(
                user_id,
                "Time limits reached of 5 minutes.\n\n❖ Please start generating your session again...",
                reply_markup=retry_key,
            )

        if await cancelled(pwd):
            return
        pwd = pwd.text

        try:
            if telethon:
                await client.sign_in(password=pwd)
            else:
                await client.check_password(password=pwd)
        except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
            return await Opleech.send_message(
                user_id,
                "The Password you've sent is wrong!!.\n\n❖ Please start generating your session again..",
                reply_markup=retry_key,
            )

    except Exception as ex:
        return await Opleech.send_message(user_id, f"ᴇʀʀᴏʀ : <code>{str(ex)}</code>")

    try:
        txt = "⎙ Here is your {0} String Session\n\n<code>{1}</code>\n\n🦋 A String Session Bot by <a href={2}>❖ 𝐖𝐃 𝐙𝐎𝐍𝐄 ❖ ™</a>\n☠ <b>Note :</b> Dont't share your string Your girlfriend 😂 others"
        if telethon:
            string_session = client.session.save()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_CHAT),
                link_preview=False,
                parse_mode="html",
            )
            await client(JoinChannelRequest("@Op_Topic_Group"))
        else:
            string_session = await client.export_session_string()
            await client.send_message(
                "me",
                txt.format(ty, string_session, SUPPORT_CHAT),
                disable_web_page_preview=True,
            )
            await client.join_chat("Op_Topic_Group")
    except KeyError:
        pass
    try:
        await client.disconnect()
        await Opleech.send_message(
            chat_id=user_id,
            text=f"⎙ Successfully generated your {ty} String Session √\n\n❖ Please check your saved message for getting it.\n\n❖ A String Generator bot by <a href={SUPPORT_CHAT}>❖ 𝐖𝐃 𝐙𝐎𝐍𝐄 ❖ ™</a>.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🅢︎🅐︎🅥︎🅔︎🅓︎✉️ᵐᵉˢˢᵃᵍᵉ√",
                            url=f"tg://openmessage?user_id={user_id}",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
    except:
        pass


async def cancelled(message):
    if "/cancel" in message.text:
        await message.reply_text(
            "Cancelled the ongoing string generation process..", reply_markup=retry_key
        )
        return True
    elif "/restart" in message.text:
        await message.reply_text(
            "Sucessfully restarted this bot.", reply_markup=retry_key
        )
        return True
    elif message.text.startswith("/"):
        await message.reply_text(
            "Cancelled the ongoing string generation process..", reply_markup=retry_key
        )
        return True
    else:
        return False
