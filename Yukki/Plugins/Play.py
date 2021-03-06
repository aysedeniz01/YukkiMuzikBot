import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)
from youtube_search import YoutubeSearch

import Yukki
from Yukki import (BOT_USERNAME, DURATION_LIMIT, DURATION_LIMIT_MIN,
                   MUSIC_BOT_NAME, app, db_mem)
from Yukki.Core.PyTgCalls.Converter import convert
from Yukki.Core.PyTgCalls.Downloader import download
from Yukki.Core.PyTgCalls.Tgdownloader import telegram_download
from Yukki.Database import (get_active_video_chats, get_video_limit,
                            is_active_video_chat)
from Yukki.Decorators.assistant import AssistantAdd
from Yukki.Decorators.checker import checker
from Yukki.Decorators.logger import logging
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (livestream_markup, playlist_markup, search_markup,
                          search_markup2, url_markup, url_markup2)
from Yukki.Utilities.changers import seconds_to_min, time_to_seconds
from Yukki.Utilities.chat import specialfont_to_normal
from Yukki.Utilities.stream import start_stream, start_stream_audio
from Yukki.Utilities.theme import check_theme
from Yukki.Utilities.thumbnails import gen_thumb
from Yukki.Utilities.url import get_url
from Yukki.Utilities.videostream import start_stream_video
from Yukki.Utilities.youtube import (get_yt_info_id, get_yt_info_query,
                                     get_yt_info_query_slider)

loop = asyncio.get_event_loop()


@app.on_message(
    filters.command(["oynat", "play", f"oynat@{BOT_USERNAME}"]) & filters.group
)
@checker
@logging
@PermissionCheck
@AssistantAdd
async def play(_, message: Message):
    await message.delete()
    if message.chat.id not in db_mem:
        db_mem[message.chat.id] = {}
    if message.sender_chat:
        return await message.reply_text(
            "π‘π π²πππ»πΎπ ππππ»πππ½πΊ __π πππππ πΈπππΎπππΌπ__πππππ!\nπΈπππΎπππΌπ ππΊπππΊππππ½πΊπ πππππΊπππΌπ ππΎππΊπ»πππΊ ππΎππ π½ππππ."
        )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    if audio:
        mystic = await message.reply_text(
            "π₯ π²πΎπ ππππΎπππππ... π«πππΏπΎπ π‘πΎπππΎπππ!"
        )
        try:
            read = db_mem[message.chat.id]["live_check"]
            if read:
                return await mystic.edit(
                    "π’πΊπππ πΊπππ ππππΊπππππππ...π¬ππππ π½ππππΎππΎπ ππΌππ π½πππ½ππππ"
                )
            else:
                pass
        except:
            pass
        if audio.file_size > 1073741824:
            return await mystic.edit_text(
                "Audio File Size Should Be Less Than 150 mb"
            )
        duration_min = seconds_to_min(audio.duration)
        duration_sec = audio.duration
        if (audio.duration) > DURATION_LIMIT:
            return await mystic.edit_text(
                f"**π²πππΎ π²πππππ π ππππ½π**\n\n**π¨πππ π΅πΎππππΎπ π²πππΎ: **{DURATION_LIMIT_MIN} π£πΊππππΊ(s)\n**π ππππΊπ π²πππΎ:** {duration_min} π£πΊππππΊ(s)"
            )
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
        file_name = path.join(path.realpath("downloads"), file_name)
        file = await convert(
            (await message.reply_to_message.download(file_name))
            if (not path.isfile(file_name))
            else file_name,
        )
        return await start_stream_audio(
            message,
            file,
            "smex1",
            "π³πΎππΎπππΊπ πππΎππππ½πΎπ ππΎπ ππΎππππ½π",
            duration_min,
            duration_sec,
            mystic,
        )
    elif video:
        limit = await get_video_limit(141414)
        if not limit:
            return await message.reply_text(
                "**GΓΆrΓΌntΓΌlΓΌ GΓΆrΓΌΕmeler iΓ§in SΔ±nΔ±r TanΔ±mlanmadΔ±**\n\ntarafΔ±ndan Bot'ta izin verilen Maksimum GΓΆrΓΌntΓΌlΓΌ Arama SayΔ±sΔ± iΓ§in bir SΔ±nΔ±r Belirleyin /set_video_limit [πΈπΊπππππΌπΊ π²ππ½π πͺππππΊπππΌπππΊππ]"
            )
        count = len(await get_active_video_chats())
        if int(count) == int(limit):
            if await is_active_video_chat(message.chat.id):
                pass
            else:
                return await message.reply_text(
                    "ΓzgΓΌnΓΌm! Bot, CPU aΕΔ±rΔ± yΓΌkleme sorunlarΔ± nedeniyle yalnΔ±zca sΔ±nΔ±rlΔ± sayΔ±da gΓΆrΓΌntΓΌlΓΌ gΓΆrΓΌΕmeye izin verir. DiΔer birΓ§ok sohbet Εu anda gΓΆrΓΌntΓΌlΓΌ aramayΔ± kullanΔ±yor. Sese geΓ§meyi deneyin veya daha sonra tekrar deneyin"
                )
        mystic = await message.reply_text(
            "π₯ π΅ππ½πΎπ ππππΎπππππ...π«πππΏπΎπ π‘πΎπππΎπππ!"
        )
        try:
            read = db_mem[message.chat.id]["live_check"]
            if read:
                return await mystic.edit(
                    "π’πΊπππ πΊπππ ππππΊπππππππ...π¬ππππ π½ππππΎππΎπ ππΌππ π½πππ½ππππ"
                )
            else:
                pass
        except:
            pass
        file = await telegram_download(message, mystic)
        return await start_stream_video(
            message,
            file,
            "π³πΎππΎπΏππ πππππππΊ ππΎππππΎπ πππ½πΎπ",
            mystic,
        )
    elif url:
        mystic = await message.reply_text("π₯ π΄π±π« ππππΎπππππ...π«πππΏπΎπ π‘πΎπππΎπππ!")
        if not message.reply_to_message:
            query = message.text.split(None, 1)[1]
        else:
            query = message.reply_to_message.text
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query(query)
        await mystic.delete()
        buttons = url_markup2(videoid, duration_min, message.from_user.id)
        return await message.reply_photo(
            photo=thumb,
            caption=f"ππ‘πΊππππ: **{title}\n\nβπ²πππΎ:** {duration_min} π£πΊππππΊ\n\n__[Video HakkΔ±nda Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            buttons = playlist_markup(
                message.from_user.first_name, message.from_user.id, "abcd"
            )
            await message.reply_photo(
                photo="Utils/Playlist.jpg",
                caption=(
                    "**πͺππππΊπππ:** /oynat [π¬ππππ πΊπ½π ππΎππΊ π²πΎπ π£ππππΊππ πΈπΊπππππΊπππ]\n\nΓπππΎπ => /oynat π§πΊπππ πΊππππ πππππππππ..."
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        mystic = await message.reply_text("π **π ππΊπππππ**...")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query(query)
        await mystic.delete()
        buttons = url_markup(
            videoid, duration_min, message.from_user.id, query, 0
        )
        return await message.reply_photo(
            photo=thumb,
            caption=f"ππ‘πΊππππ: **{title}\n\nβπ²πππΎ:** {duration_min} π£πΊππππΊ\n\n__[π΅ππ½πΎπ π§πΊπππππ½πΊ π€π π‘ππππ ππΌππ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(filters.regex(pattern=r"MusicStream"))
async def Music_Stream(_, CallbackQuery):
    if CallbackQuery.message.chat.id not in db_mem:
        db_mem[CallbackQuery.message.chat.id] = {}
    try:
        read1 = db_mem[CallbackQuery.message.chat.id]["live_check"]
        if read1:
            return await CallbackQuery.answer(
                "π’πΊπππ πΊπππ ππππΊπππππππ...π¬ππππ π½ππππΎππΎπ ππΌππ π½πππ½ππππ",
                show_alert=True,
            )
        else:
            pass
    except:
        pass
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    videoid, duration, user_id = callback_request.split("|")
    if str(duration) == "None":
        buttons = livestream_markup("720", videoid, duration, user_id)
        return await CallbackQuery.edit_message_text(
            "**π’πΊπππ πΊπππ πΊπππππΊππ½π**\n\nπ’πΊπππ πΊπππ ππππΊπππΊπ ππππΎπ πππππ? (varsa), π’πΊπππΊπππΊ πππΊπ πππππ π½πππΊπΌπΊπ,π’πΊπππ πππ½πΎπ πΊππππππΊ ππΎπΌπππΎπΌπΎππππ...",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "π‘π ππΎπππ ππΌππ π½πΎπππ!πͺπΎππ½π ππΊπππππ πΊππΊ.", show_alert=True
        )
    await CallbackQuery.message.delete()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    if duration_sec > DURATION_LIMIT:
        return await CallbackQuery.message.reply_text(
            f"**π²πππΎ π²πππππ π ππππ½π**\n\n**π¨πππ π΅πΎππππΎπ π²πππΎ: **{DURATION_LIMIT_MIN} π£πΊππππΊ(s)\n**π ππππΊπ π²πππΎ:** {duration_min} π£πΊππππΊ(s)"
        )
    await CallbackQuery.answer(f"π¨πππΎπππππ:- {title[:20]}", show_alert=True)
    mystic = await CallbackQuery.message.reply_text(
        f"**{MUSIC_BOT_NAME} π¨ππ½ππππΌπ**\n\n**ππ‘πΊππππ:** {title[:50]}\n\n0% ββββββββββββ 100%"
    )
    downloaded_file = await loop.run_in_executor(
        None, download, videoid, mystic, title
    )
    raw_path = await convert(downloaded_file)
    theme = await check_theme(chat_id)
    chat_title = await specialfont_to_normal(chat_title)
    thumb = await gen_thumb(thumbnail, title, user_id, theme, chat_title)
    if chat_id not in db_mem:
        db_mem[chat_id] = {}
    await start_stream(
        CallbackQuery,
        raw_path,
        videoid,
        thumb,
        title,
        duration_min,
        duration_sec,
        mystic,
    )


@app.on_callback_query(filters.regex(pattern=r"Search"))
async def search_query_more(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "πͺπΎππ½π ππππππππππ πΊππΊπππ...π‘π π½ππππΎππ πππππΊπππΊππΊ ππΊππππ πππ.",
            show_alert=True,
        )
    await CallbackQuery.answer("π£πΊππΊ π₯πΊπππΊ π²ππππΌ")
    results = YoutubeSearch(query, max_results=5).to_dict()
    med = InputMediaPhoto(
        media="Utils/Result.JPEG",
        caption=(
            f"1οΈβ£<b>{results[0]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[0]['id']})__</u>\n\n2οΈβ£<b>{results[1]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[1]['id']})__</u>\n\n3οΈβ£<b>{results[2]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[2]['id']})__</u>\n\n4οΈβ£<b>{results[3]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[3]['id']})__</u>\n\n5οΈβ£<b>{results[4]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[4]['id']})__</u>"
        ),
    )
    buttons = search_markup(
        results[0]["id"],
        results[1]["id"],
        results[2]["id"],
        results[3]["id"],
        results[4]["id"],
        results[0]["duration"],
        results[1]["duration"],
        results[2]["duration"],
        results[3]["duration"],
        results[4]["duration"],
        user_id,
        query,
    )
    return await CallbackQuery.edit_message_media(
        media=med, reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"popat"))
async def popat(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    i, query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "π‘π ππΎπππ ππΌππ π½πΎπππ!πͺπΎππ½π π¬πππππππππ πΊππΊπππ...", show_alert=True
        )
    results = YoutubeSearch(query, max_results=10).to_dict()
    if int(i) == 1:
        buttons = search_markup2(
            results[5]["id"],
            results[6]["id"],
            results[7]["id"],
            results[8]["id"],
            results[9]["id"],
            results[5]["duration"],
            results[6]["duration"],
            results[7]["duration"],
            results[8]["duration"],
            results[9]["duration"],
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"6οΈβ£<b>{results[5]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[5]['id']})__</u>\n\n7οΈβ£<b>{results[6]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[6]['id']})__</u>\n\n8οΈβ£<b>{results[7]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[7]['id']})__</u>\n\n9οΈβ£<b>{results[8]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[8]['id']})__</u>\n\nπ<b>{results[9]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[9]['id']})__</u>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        disable_web_page_preview = True
        return
    if int(i) == 2:
        buttons = search_markup(
            results[0]["id"],
            results[1]["id"],
            results[2]["id"],
            results[3]["id"],
            results[4]["id"],
            results[0]["duration"],
            results[1]["duration"],
            results[2]["duration"],
            results[3]["duration"],
            results[4]["duration"],
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"1οΈβ£<b>{results[0]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[0]['id']})__</u>\n\n2οΈβ£<b>{results[1]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[1]['id']})__</u>\n\n3οΈβ£<b>{results[2]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[2]['id']})__</u>\n\n4οΈβ£<b>{results[3]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[3]['id']})__</u>\n\n5οΈβ£<b>{results[4]['title']}</b>\n  β  π <u>__[Ek Bilgi AlΔ±n](https://t.me/{BOT_USERNAME}?start=info_{results[4]['id']})__</u>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        disable_web_page_preview = True
        return


@app.on_callback_query(filters.regex(pattern=r"slider"))
async def slider_query_results(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, type, query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "πͺπΎππ½π π¬πππππππππ πΊππΊπππ...π‘π π½ππππΎππ πππππΊπππΊππΊ ππΊππππ πππ.",
            show_alert=True,
        )
    what = str(what)
    type = int(type)
    if what == "F":
        if type == 9:
            query_type = 0
        else:
            query_type = int(type + 1)
        await CallbackQuery.answer("π²ππππΊππ π²ππππΌπ π πππΊ", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query_slider(query, query_type)
        buttons = url_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"ππ‘πΊππππ: **{title}\n\nβπ²πππΎ:** {duration_min} π£πΊππππΊ\n\n__[π΅ππ½πΎπ ππΊπππππ½πΊ πΎπ π»ππππ πΊπππ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if type == 0:
            query_type = 9
        else:
            query_type = int(type - 1)
        await CallbackQuery.answer("ΓππΌπΎππ πππππΌπ πΊπππΊ", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query_slider(query, query_type)
        buttons = url_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"ππ‘πΊππππ: **{title}\n\nβπ²πππΎ:** {duration_min} π£πΊππππΊ\n\n__[π΅ππ½πΎπ ππΊπππππ½πΊ πΎπ π»ππππ πΊπππ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
