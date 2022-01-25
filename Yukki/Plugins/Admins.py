import asyncio
import os
import random
from asyncio import QueueEmpty

from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, KeyboardButton, Message,
                            ReplyKeyboardMarkup, ReplyKeyboardRemove)

from config import get_queue
from Yukki import BOT_USERNAME, MUSIC_BOT_NAME, app, db_mem
from Yukki.Core.PyTgCalls import Queues
from Yukki.Core.PyTgCalls.Converter import convert
from Yukki.Core.PyTgCalls.Downloader import download
from Yukki.Core.PyTgCalls.Yukki import (pause_stream, resume_stream,
                                        skip_stream, skip_video_stream,
                                        stop_stream)
from Yukki.Database import (is_active_chat, is_music_playing, music_off,
                            music_on, remove_active_chat,
                            remove_active_video_chat)
from Yukki.Decorators.admins import AdminRightsCheck
from Yukki.Decorators.checker import checker, checkerCB
from Yukki.Inline import audio_markup, primary_markup, secondary_markup2
from Yukki.Utilities.changers import time_to_seconds
from Yukki.Utilities.chat import specialfont_to_normal
from Yukki.Utilities.theme import check_theme
from Yukki.Utilities.thumbnails import gen_thumb
from Yukki.Utilities.timer import start_timer
from Yukki.Utilities.youtube import get_m3u8, get_yt_info_id

loop = asyncio.get_event_loop()


__MODULE__ = "𝖪𝗈𝗆𝗎𝗍𝗅𝖺𝗋"
__HELP__ = """


/durdur
- 𝖲𝖾𝗌𝗅𝗂 𝖲𝗈𝗁𝖻𝖾𝗍𝗍𝖾 𝖼𝖺𝗅𝖺𝗇 𝖬𝗎𝗓𝗂𝗀𝗂 𝖽𝗎𝗋𝖽𝗎𝗋.

/devam
- 𝖲𝖾𝗌𝗅𝗂 𝖲𝗈𝗁𝖻𝖾𝗍𝗍𝖾 𝖣𝗎𝗋𝖺𝗄𝗅𝖺𝗍𝗂𝗅𝗆𝗂𝗌 𝖬𝗎𝗓𝗂𝗄 𝖽𝖾𝗏𝖺𝗆 𝖾𝖽𝖾𝗋.

/atla
- 𝖲𝖾𝗌𝗅𝗂 𝖲𝗈𝗁𝖻𝖾𝗍𝗍𝖾 𝖼𝖺𝗅𝗆𝖺𝗄𝗍𝖺 𝗈𝗅𝖺𝗇 𝖬𝗎𝗓𝗂𝗀𝗂 𝖺𝗍𝗅𝖺 .

/end veya /son
- 𝖬𝗎𝗓𝗂𝗀𝗂 𝗌𝗈𝗇𝗅𝖺𝗇𝖽𝗂𝗋 .

/queue
- 𝖲𝖺𝗋𝗄𝗂 𝗅𝗂𝗌𝗍𝖾𝗌𝗂𝗇𝗂 𝗄𝗈𝗇𝗍𝗋𝗈𝗅 𝖾𝗍 .


**Not:**
𝖸𝖺𝗅𝗇𝗂𝗓𝖼𝖺 𝖲𝗎𝖽𝗈 𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋𝗂 𝗂𝖼𝗂𝗇...

/activevc
- 𝖡𝗈𝗍𝗍𝖺 𝖺𝗄𝗍𝗂𝖿 𝗌𝖾𝗌𝗅𝗂 𝗌𝗈𝗁𝖻𝖾𝗍𝗅𝖾𝗋𝗂 𝗄𝗈𝗇𝗍𝗋𝗈𝗅 𝖾𝗍.
/activevideo
- 𝖡𝗈𝗍𝗍𝖺 𝖺𝗄𝗍𝗂𝖿 𝗀𝗈𝗋𝗎𝗇𝗍𝗎𝗅𝗎 𝗌𝗈𝗁𝖻𝖾𝗍𝗅𝖾𝗋𝗂 𝗄𝗈𝗇𝗍𝗋𝗈𝗅 𝖾𝗍.
"""


@app.on_message(
    filters.command(["durdur", "atla", "devam", "son", "end"])
    & filters.group
)
@AdminRightsCheck
@checker
async def admins(_, message: Message):
    global get_queue
    if not len(message.command) == 1:
        return await message.reply_text("𝖧𝖺𝗍𝖺! 𝖪𝗈𝗆𝗎𝗍𝗎𝗇 𝗒𝖺𝗇𝗅𝗂𝗌 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝗆𝗂...")
    if not await is_active_chat(message.chat.id):
        return await message.reply_text("𝖲𝖾𝗌𝗅𝗂 𝗌𝗈𝗁𝖻𝖾𝗍𝗍𝖾 𝗁𝗂𝖼𝖻𝗂𝗋𝗌𝖾𝗒 𝖼𝖺𝗅𝗆𝗂𝗒𝗈𝗋...")
    chat_id = message.chat.id
    if message.command[0][1] == "u":
        if not await is_music_playing(message.chat.id):
            return await message.reply_text("𝖬𝗎𝗓𝗂𝗄 𝗓𝖺𝗍𝖾𝗇 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗅𝖽𝗎...")
        await music_off(chat_id)
        await pause_stream(chat_id)
        await message.reply_text(
            f"🎙️ 𝖲𝖾𝗌𝗅𝗂 𝖲𝗈𝗁𝖻𝖾𝗍 𝖣𝗎𝗋𝖽𝗎𝗋𝗎𝗅𝖽𝗎 {message.from_user.mention}!"
        )
    if message.command[0][1] == "e":
        if await is_music_playing(message.chat.id):
            return await message.reply_text("𝖬𝗎𝗓𝗂𝗄 𝗓𝖺𝗍𝖾𝗇 𝖼𝖺𝗅𝗂𝗒𝗈𝗋...")
        await music_on(chat_id)
        await resume_stream(chat_id)
        await message.reply_text(
            f"🎙️ 𝖲𝖾𝗌𝗅𝗂 𝖲𝗈𝗁𝖻𝖾𝗍 𝖲𝗎𝗋𝖽𝗎𝗋𝗎𝗅𝖽𝗎 {message.from_user.mention}!"
        )
    if message.command[0][1] == "o" or message.command[0][1] == "n":
        if message.chat.id not in db_mem:
            db_mem[message.chat.id] = {}
        wtfbro = db_mem[message.chat.id]
        wtfbro["live_check"] = False
        try:
            Queues.clear(message.chat.id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await remove_active_video_chat(chat_id)
        await stop_stream(chat_id)
        await message.reply_text(
            f"🎙️ 𝖲𝖾𝗌𝗅𝗂 𝖲𝗈𝗁𝖻𝖾𝗍 𝖲𝗈𝗇𝗅𝖺𝗇𝖽𝗂𝗋𝗂𝗅𝖽𝗂 {message.from_user.mention}!"
        )
    if message.command[0][1] == "t":
        if message.chat.id not in db_mem:
            db_mem[message.chat.id] = {}
        wtfbro = db_mem[message.chat.id]
        wtfbro["live_check"] = False
        Queues.task_done(chat_id)
        if Queues.is_empty(chat_id):
            await remove_active_chat(chat_id)
            await remove_active_video_chat(chat_id)
            await message.reply_text(
                "__𝖲𝗂𝗋𝖺__𝖽𝖺 𝖺𝗋𝗍𝗂𝗄 𝗆𝗎𝗓𝗂𝗄 𝗒𝗈𝗄...\n\n𝖲𝖾𝗌𝗅𝗂 𝖲𝗈𝗁𝖻𝖾𝗍𝗍𝖾𝗇 𝖠𝗒𝗋𝗂𝗅𝗂𝗒𝗈𝗋𝗎𝗆"
            )
            await stop_stream(chat_id)
            return
        else:
            videoid = Queues.get(chat_id)["file"]
            got_queue = get_queue.get(chat_id)
            if got_queue:
                got_queue.pop(0)
            finxx = f"{videoid[0]}{videoid[1]}{videoid[2]}"
            aud = 0
            if str(finxx) == "raw":
                await skip_stream(chat_id, videoid)
                afk = videoid
                title = db_mem[videoid]["title"]
                duration_min = db_mem[videoid]["duration"]
                duration_sec = int(time_to_seconds(duration_min))
                mention = db_mem[videoid]["username"]
                videoid = db_mem[videoid]["videoid"]
                if str(videoid) == "smex1":
                    buttons = buttons = audio_markup(
                        videoid,
                        message.from_user.id,
                        duration_min,
                        duration_min,
                    )
                    thumb = "Utils/Telegram.JPEG"
                    aud = 1
                else:
                    _path_ = _path_ = (
                        (str(afk))
                        .replace("_", "", 1)
                        .replace("/", "", 1)
                        .replace(".", "", 1)
                    )
                    thumb = f"cache/{_path_}final.png"
                    buttons = primary_markup(
                        videoid,
                        message.from_user.id,
                        duration_min,
                        duration_min,
                    )
                final_output = await message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"<b>__𝖠𝗍𝗅𝖺𝗇𝖺𝗇 𝖲𝖾𝗌𝗅𝗂 𝖲𝗈𝗁𝖻𝖾𝗍__</b>\n\n🎥<b>__𝖮𝗒𝗇𝖺𝗆𝖺𝗒𝖺 𝖡𝖺𝗌𝗅𝖺𝖽𝗂:__</b> {title} \n⏳<b>__𝖲𝗎𝗋𝖾:__</b> {duration_min} \n👤<b>__𝖳𝖺𝗅𝖾𝗉:__ </b> {mention}",
                )
                await start_timer(
                    videoid,
                    duration_min,
                    duration_sec,
                    final_output,
                    message.chat.id,
                    message.from_user.id,
                    aud,
                )
            elif str(finxx) == "s1s":
                mystic = await message.reply_text(
                    "𝖠𝗍𝗅𝖺𝗇𝖽𝗂...𝖲𝗈𝗇𝗋𝖺𝗄𝗂 𝖵𝗂𝖽𝖾𝗈 𝖠𝗄𝗂𝗌𝗂𝗇𝖺 𝖦𝖾𝖼𝗂𝗅𝗂𝗒𝗈𝗋..."
                )
                afk = videoid
                read = (str(videoid)).replace("s1s_", "", 1)
                s = read.split("_+_")
                quality = s[0]
                videoid = s[1]
                if int(quality) == 1080:
                    try:
                        await skip_video_stream(chat_id, videoid, 720, mystic)
                    except Exception as e:
                        return await mystic.edit(
                            f"Video akışı değiştirilirken hata oluştu.\n\nMakul sebep:- {e}"
                        )
                    buttons = secondary_markup2("Smex1", message.from_user.id)
                    mention = db_mem[afk]["username"]
                    await mystic.delete()
                    final_output = await message.reply_photo(
                        photo="Utils/Telegram.JPEG",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=(
                            f"<b>__𝖦𝗈𝗋𝗎𝗇𝗍𝗎𝗅𝗎 𝖲𝗈𝗁𝖻𝖾𝗍 𝖠𝗍𝗅𝖺𝗇𝖽𝗂__</b>\n\n👤**__𝖳𝖺𝗅𝖾𝗉:__** {mention}"
                        ),
                    )
                    await mystic.delete()
                else:
                    (
                        title,
                        duration_min,
                        duration_sec,
                        thumbnail,
                    ) = get_yt_info_id(videoid)
                    nrs, ytlink = await get_m3u8(videoid)
                    if nrs == 0:
                        return await mystic.edit(
                            "𝖵𝗂𝖽𝖾𝗈 𝖡𝗂𝖼𝗂𝗆𝗅𝖾𝗋𝗂 𝖠𝗅𝗂𝗇𝖺𝗆𝖺𝖽𝗂.",
                        )
                    try:
                        await skip_video_stream(
                            chat_id, ytlink, quality, mystic
                        )
                    except Exception as e:
                        return await mystic.edit(
                            f"Video akışı değiştirilirken hata oluştu.\n\nMakul sebep:- {e}"
                        )
                    theme = await check_theme(chat_id)
                    c_title = message.chat.title
                    user_id = db_mem[afk]["user_id"]
                    chat_title = await specialfont_to_normal(c_title)
                    thumb = await gen_thumb(
                        thumbnail, title, user_id, theme, chat_title
                    )
                    buttons = primary_markup(
                        videoid, user_id, duration_min, duration_min
                    )
                    mention = db_mem[afk]["username"]
                    await mystic.delete()
                    final_output = await message.reply_photo(
                        photo=thumb,
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=(
                            f"<b>__𝖦𝗈𝗋𝗎𝗇𝗍𝗎𝗅𝗎 𝖲𝗈𝗁𝖻𝖾𝗍 𝖠𝗍𝗅𝖺𝗇𝖽𝗂__</b>\n\n🎥<b>__𝖵𝗂𝖽𝖾𝗈 𝖮𝗒𝗇𝖺𝗍𝗆𝖺𝗒𝖺 𝖡𝖺𝗌𝗅𝖺𝖽𝗂:__ </b> [{title[:25]}](https://www.youtube.com/watch?v={videoid}) \n👤**__𝖳𝖺𝗅𝖾𝗉:__** {mention}"
                        ),
                    )
                    await mystic.delete()
                    os.remove(thumb)
                    await start_timer(
                        videoid,
                        duration_min,
                        duration_sec,
                        final_output,
                        message.chat.id,
                        message.from_user.id,
                        aud,
                    )
            else:
                mystic = await message.reply_text(
                    f"**{MUSIC_BOT_NAME} 𝖢𝖺𝗅𝗆𝖺 𝖫𝗂𝗌𝗍𝖾𝗌𝗂 𝗂𝗌𝗅𝖾𝗏𝗂**\n\n__𝖢𝖺𝗅𝗆𝖺 𝗅𝗂𝗌𝗍𝖾𝗌𝗂𝗇𝖽𝖾𝗇 𝗌𝗈𝗇𝗋𝖺𝗄𝗂 𝗆𝗎𝗓𝗂𝗀𝗂 𝗂𝗇𝖽𝗂𝗋𝗆𝖾....__"
                )
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                ) = get_yt_info_id(videoid)
                await mystic.edit(
                    f"**{MUSIC_BOT_NAME} 𝗂𝗇𝖽𝗂𝗋𝗂𝖼𝗂**\n\n**𝖡𝖺𝗌𝗅𝗂𝗄:** {title[:50]}\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
                )
                downloaded_file = await loop.run_in_executor(
                    None, download, videoid, mystic, title
                )
                raw_path = await convert(downloaded_file)
                await skip_stream(chat_id, raw_path)
                theme = await check_theme(chat_id)
                chat_title = await specialfont_to_normal(message.chat.title)
                thumb = await gen_thumb(
                    thumbnail, title, message.from_user.id, theme, chat_title
                )
                buttons = primary_markup(
                    videoid, message.from_user.id, duration_min, duration_min
                )
                await mystic.delete()
                mention = db_mem[videoid]["username"]
                final_output = await message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=(
                        f"<b>__𝖠𝗍𝗅𝖺𝗇𝖺𝗇 𝖲𝖾𝗌𝗅𝗂 𝖲𝗈𝗁𝖻𝖾𝗍__</b>\n\n🎥<b>__𝖮𝗒𝗇𝖺𝗍𝗆𝖺 𝖡𝖺𝗌𝗅𝖺𝖽𝗂:__ </b>[{title[:25]}](https://www.youtube.com/watch?v={videoid}) \n⏳<b>__𝖲𝗎𝗋𝖾:__</b> {duration_min} 𝖣𝖺𝗄𝗂𝗄𝖺\n👤**__𝖳𝖺𝗅𝖾𝗉:__** {mention}"
                    ),
                )
                os.remove(thumb)
                await start_timer(
                    videoid,
                    duration_min,
                    duration_sec,
                    final_output,
                    message.chat.id,
                    message.from_user.id,
                    aud,
                )
