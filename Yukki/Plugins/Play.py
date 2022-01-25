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
            "𝖡𝗎 𝖲𝗈𝗁𝖻𝖾𝗍 𝗀𝗋𝗎𝖻𝗎𝗇𝖽𝖺 __𝖠𝗇𝗈𝗇𝗂𝗆 𝖸𝗈𝗇𝖾𝗍𝗂𝖼𝗂__𝗌𝗂𝗇𝗂𝗓!\n𝖸𝗈𝗇𝖾𝗍𝗂𝖼𝗂 𝗁𝖺𝗄𝗅𝖺𝗋𝗂𝗇𝖽𝖺𝗇 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝗁𝖾𝗌𝖺𝖻𝗂𝗇𝖺 𝗀𝖾𝗋𝗂 𝖽𝗈𝗇𝗎𝗇."
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
            "📥 𝖲𝖾𝗌 𝗂𝗌𝗅𝖾𝗇𝗂𝗒𝗈𝗋... 𝖫𝗎𝗍𝖿𝖾𝗇 𝖡𝖾𝗄𝗅𝖾𝗒𝗂𝗇!"
        )
        try:
            read = db_mem[message.chat.id]["live_check"]
            if read:
                return await mystic.edit(
                    "𝖢𝖺𝗇𝗅𝗂 𝖺𝗄𝗂𝗌 𝗈𝗒𝗇𝖺𝗍𝗂𝗅𝗂𝗒𝗈𝗋...𝖬𝗎𝗓𝗂𝗄 𝖽𝗂𝗇𝗅𝖾𝗆𝖾𝗄 𝗂𝖼𝗂𝗇 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗇"
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
                f"**𝖲𝗎𝗋𝖾 𝖲𝗂𝗇𝗂𝗋𝗂 𝖠𝗌𝗂𝗅𝖽𝗂**\n\n**𝖨𝗓𝗂𝗇 𝖵𝖾𝗋𝗂𝗅𝖾𝗇 𝖲𝗎𝗋𝖾: **{DURATION_LIMIT_MIN} 𝖣𝖺𝗄𝗂𝗄𝖺(s)\n**𝖠𝗅𝗂𝗇𝖺𝗇 𝖲𝗎𝗋𝖾:** {duration_min} 𝖣𝖺𝗄𝗂𝗄𝖺(s)"
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
            "𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝗎𝗓𝖾𝗋𝗂𝗇𝖽𝖾𝗇 𝗌𝖾𝗌 𝗏𝖾𝗋𝗂𝗅𝖽𝗂",
            duration_min,
            duration_sec,
            mystic,
        )
    elif video:
        limit = await get_video_limit(141414)
        if not limit:
            return await message.reply_text(
                "**Görüntülü Görüşmeler için Sınır Tanımlanmadı**\n\ntarafından Bot'ta izin verilen Maksimum Görüntülü Arama Sayısı için bir Sınır Belirleyin /set_video_limit [𝖸𝖺𝗅𝗇𝗂𝗓𝖼𝖺 𝖲𝗎𝖽𝗈 𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋𝗂]"
            )
        count = len(await get_active_video_chats())
        if int(count) == int(limit):
            if await is_active_video_chat(message.chat.id):
                pass
            else:
                return await message.reply_text(
                    "Üzgünüm! Bot, CPU aşırı yükleme sorunları nedeniyle yalnızca sınırlı sayıda görüntülü görüşmeye izin verir. Diğer birçok sohbet şu anda görüntülü aramayı kullanıyor. Sese geçmeyi deneyin veya daha sonra tekrar deneyin"
                )
        mystic = await message.reply_text(
            "📥 𝖵𝗂𝖽𝖾𝗈 𝗂𝗌𝗅𝖾𝗇𝗂𝗒𝗈𝗋...𝖫𝗎𝗍𝖿𝖾𝗇 𝖡𝖾𝗄𝗅𝖾𝗒𝗂𝗇!"
        )
        try:
            read = db_mem[message.chat.id]["live_check"]
            if read:
                return await mystic.edit(
                    "𝖢𝖺𝗇𝗅𝗂 𝖺𝗄𝗂𝗌 𝗈𝗒𝗇𝖺𝗍𝗂𝗅𝗂𝗒𝗈𝗋...𝖬𝗎𝗓𝗂𝗄 𝖽𝗂𝗇𝗅𝖾𝗆𝖾𝗄 𝗂𝖼𝗂𝗇 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗇"
                )
            else:
                pass
        except:
            pass
        file = await telegram_download(message, mystic)
        return await start_stream_video(
            message,
            file,
            "𝖳𝖾𝗅𝖾𝖿𝗈𝗇 𝗒𝗈𝗅𝗎𝗒𝗅𝖺 𝗏𝖾𝗋𝗂𝗅𝖾𝗇 𝗏𝗂𝖽𝖾𝗈",
            mystic,
        )
    elif url:
        mystic = await message.reply_text("📥 𝖴𝖱𝖫 𝗂𝗌𝗅𝖾𝗇𝗂𝗒𝗈𝗋...𝖫𝗎𝗍𝖿𝖾𝗇 𝖡𝖾𝗄𝗅𝖾𝗒𝗂𝗇!")
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
            caption=f"📋𝖡𝖺𝗌𝗅𝗂𝗄: **{title}\n\n⌚𝖲𝗎𝗋𝖾:** {duration_min} 𝖣𝖺𝗄𝗂𝗄𝖺\n\n__[Video Hakkında Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
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
                    "**𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝗆:** /oynat [𝖬𝗎𝗓𝗂𝗄 𝖺𝖽𝗂 𝗏𝖾𝗒𝖺 𝖲𝖾𝗌 𝖣𝗈𝗌𝗒𝖺𝗌𝗂 𝖸𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇]\n\nÖ𝗋𝗇𝖾𝗄 => /oynat 𝖧𝖺𝗇𝗀𝗂 𝖺𝗅𝗄𝗈𝗅 𝗎𝗇𝗎𝗍𝗍𝗎𝗋𝗎𝗋..."
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        mystic = await message.reply_text("🙈 **𝖠𝗋𝖺𝗇𝗂𝗒𝗈𝗋**...")
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
            caption=f"📋𝖡𝖺𝗌𝗅𝗂𝗄: **{title}\n\n⌚𝖲𝗎𝗋𝖾:** {duration_min} 𝖣𝖺𝗄𝗂𝗄𝖺\n\n__[𝖵𝗂𝖽𝖾𝗈 𝖧𝖺𝗄𝗄𝗂𝗇𝖽𝖺 𝖤𝗄 𝖡𝗂𝗅𝗀𝗂 𝗂𝖼𝗂𝗇](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
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
                "𝖢𝖺𝗇𝗅𝗂 𝖺𝗄𝗂𝗌 𝗈𝗒𝗇𝖺𝗍𝗂𝗅𝗂𝗒𝗈𝗋...𝖬𝗎𝗓𝗂𝗄 𝖽𝗂𝗇𝗅𝖾𝗆𝖾𝗄 𝗂𝖼𝗂𝗇 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗇",
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
            "**𝖢𝖺𝗇𝗅𝗂 𝖺𝗄𝗂𝗌 𝖺𝗅𝗀𝗂𝗅𝖺𝗇𝖽𝗂**\n\n𝖢𝖺𝗇𝗅𝗂 𝖺𝗄𝗂𝗌 𝗈𝗒𝗇𝖺𝗍𝗆𝖺𝗄 𝗂𝗌𝗍𝖾𝗋 𝗆𝗂𝗌𝗂𝗇? (varsa), 𝖢𝖺𝗅𝗆𝖺𝗄𝗍𝖺 𝗈𝗅𝖺𝗇 𝗆𝗎𝗓𝗂𝗄 𝖽𝗎𝗋𝖺𝖼𝖺𝗄,𝖢𝖺𝗇𝗅𝗂 𝗏𝗂𝖽𝖾𝗈 𝖺𝗄𝗂𝗌𝗂𝗇𝖺 𝗀𝖾𝖼𝗂𝗅𝖾𝖼𝖾𝗄𝗍𝗂𝗋...",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "𝖡𝗎 𝗌𝖾𝗇𝗂𝗇 𝗂𝖼𝗂𝗇 𝖽𝖾𝗀𝗂𝗅!𝖪𝖾𝗇𝖽𝗂 𝗌𝖺𝗋𝗄𝗂𝗇𝗂 𝖺𝗋𝖺.", show_alert=True
        )
    await CallbackQuery.message.delete()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    if duration_sec > DURATION_LIMIT:
        return await CallbackQuery.message.reply_text(
            f"**𝖲𝗎𝗋𝖾 𝖲𝗂𝗇𝗂𝗋𝗂 𝖠𝗌𝗂𝗅𝖽𝗂**\n\n**𝖨𝗓𝗂𝗇 𝖵𝖾𝗋𝗂𝗅𝖾𝗇 𝖲𝗎𝗋𝖾: **{DURATION_LIMIT_MIN} 𝖣𝖺𝗄𝗂𝗄𝖺(s)\n**𝖠𝗅𝗂𝗇𝖺𝗇 𝖲𝗎𝗋𝖾:** {duration_min} 𝖣𝖺𝗄𝗂𝗄𝖺(s)"
        )
    await CallbackQuery.answer(f"𝖨𝗌𝗅𝖾𝗇𝗂𝗒𝗈𝗋:- {title[:20]}", show_alert=True)
    mystic = await CallbackQuery.message.reply_text(
        f"**{MUSIC_BOT_NAME} 𝖨𝗇𝖽𝗂𝗋𝗂𝖼𝗂**\n\n**📋𝖡𝖺𝗌𝗅𝗂𝗄:** {title[:50]}\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
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
            "𝖪𝖾𝗇𝖽𝗂 𝗆𝗎𝗓𝗂𝗀𝗂𝗇𝗂𝗓𝗂 𝖺𝗋𝖺𝗒𝗂𝗇...𝖡𝗎 𝖽𝗎𝗀𝗆𝖾𝗒𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗆𝖺𝗒𝖺 𝗁𝖺𝗄𝗄𝗂𝗇 𝗒𝗈𝗄.",
            show_alert=True,
        )
    await CallbackQuery.answer("𝖣𝖺𝗁𝖺 𝖥𝖺𝗓𝗅𝖺 𝖲𝗈𝗇𝗎𝖼")
    results = YoutubeSearch(query, max_results=5).to_dict()
    med = InputMediaPhoto(
        media="Utils/Result.JPEG",
        caption=(
            f"1️⃣<b>{results[0]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[0]['id']})__</u>\n\n2️⃣<b>{results[1]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[1]['id']})__</u>\n\n3️⃣<b>{results[2]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[2]['id']})__</u>\n\n4️⃣<b>{results[3]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[3]['id']})__</u>\n\n5️⃣<b>{results[4]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[4]['id']})__</u>"
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
            "𝖡𝗎 𝗌𝖾𝗇𝗂𝗇 𝗂𝖼𝗂𝗇 𝖽𝖾𝗀𝗂𝗅!𝖪𝖾𝗇𝖽𝗂 𝖬𝗎𝗓𝗂𝗀𝗂𝗇𝗂𝗓𝗂 𝖺𝗋𝖺𝗒𝗂𝗇...", show_alert=True
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
            f"6️⃣<b>{results[5]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[5]['id']})__</u>\n\n7️⃣<b>{results[6]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[6]['id']})__</u>\n\n8️⃣<b>{results[7]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[7]['id']})__</u>\n\n9️⃣<b>{results[8]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[8]['id']})__</u>\n\n🔟<b>{results[9]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[9]['id']})__</u>",
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
            f"1️⃣<b>{results[0]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[0]['id']})__</u>\n\n2️⃣<b>{results[1]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[1]['id']})__</u>\n\n3️⃣<b>{results[2]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[2]['id']})__</u>\n\n4️⃣<b>{results[3]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[3]['id']})__</u>\n\n5️⃣<b>{results[4]['title']}</b>\n  ┗  🔗 <u>__[Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{results[4]['id']})__</u>",
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
            "𝖪𝖾𝗇𝖽𝗂 𝖬𝗎𝗓𝗂𝗀𝗂𝗇𝗂𝗓𝗂 𝖺𝗋𝖺𝗒𝗂𝗇...𝖡𝗎 𝖽𝗎𝗀𝗆𝖾𝗒𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗆𝖺𝗒𝖺 𝗁𝖺𝗄𝗄𝗂𝗇 𝗒𝗈𝗄.",
            show_alert=True,
        )
    what = str(what)
    type = int(type)
    if what == "F":
        if type == 9:
            query_type = 0
        else:
            query_type = int(type + 1)
        await CallbackQuery.answer("𝖲𝗈𝗇𝗋𝖺𝗄𝗂 𝖲𝗈𝗇𝗎𝖼𝗎 𝖠𝗅𝗆𝖺", show_alert=True)
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
            caption=f"📋𝖡𝖺𝗌𝗅𝗂𝗄: **{title}\n\n⌚𝖲𝗎𝗋𝖾:** {duration_min} 𝖣𝖺𝗄𝗂𝗄𝖺\n\n__[𝖵𝗂𝖽𝖾𝗈 𝗁𝖺𝗄𝗄𝗂𝗇𝖽𝖺 𝖾𝗄 𝖻𝗂𝗅𝗀𝗂 𝖺𝗅𝗂𝗇](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if type == 0:
            query_type = 9
        else:
            query_type = int(type - 1)
        await CallbackQuery.answer("Ö𝗇𝖼𝖾𝗄𝗂 𝗌𝗈𝗇𝗎𝖼𝗎 𝖺𝗅𝗆𝖺", show_alert=True)
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
            caption=f"📋𝖡𝖺𝗌𝗅𝗂𝗄: **{title}\n\n⌚𝖲𝗎𝗋𝖾:** {duration_min} 𝖣𝖺𝗄𝗂𝗄𝖺\n\n__[𝖵𝗂𝖽𝖾𝗈 𝗁𝖺𝗄𝗄𝗂𝗇𝖽𝖺 𝖾𝗄 𝖻𝗂𝗅𝗀𝗂 𝖺𝗅𝗂𝗇](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
