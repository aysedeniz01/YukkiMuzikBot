from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import SUDOERS, app
from Yukki.Database import blacklist_chat, blacklisted_chats, whitelist_chat

__MODULE__ = "𝖪𝖺𝗋𝖺 𝖫𝗂𝗌𝗍𝖾"
__HELP__ = """


/blacklistedchat 
- 𝖪𝖺𝗋𝖺 𝗅𝗂𝗌𝗍𝖾𝗒𝖾 𝖺𝗅𝗂𝗇𝗆𝗂𝗌 𝗌𝗈𝗁𝖻𝖾𝗍𝗅𝖾𝗋𝗂 𝗄𝗈𝗇𝗍𝗋𝗈𝗅 𝖾𝖽𝗂𝗇.


**𝖭𝖮𝖳:**
𝖸𝖺𝗅𝗇𝗂𝗓𝖼𝖺 𝖲𝗎𝖽𝗈 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋𝗂 𝗂𝖼𝗂𝗇 𝗀𝖾𝖼𝖾𝗋𝗅𝗂𝖽𝗂𝗋.


/blacklistchat [CHAT_ID] 
- 𝖬𝗎𝗓𝗂𝗄 𝖻𝗈𝗍𝗎𝗇𝗎 𝗄𝗎𝗅𝗅𝖺𝗇𝖺𝗋𝖺𝗄 𝗁𝖾𝗋𝗁𝖺𝗇𝗀𝗂 𝖻𝗂𝗋 𝖲𝗈𝗁𝖻𝖾𝗍𝗂 𝗄𝖺𝗋𝖺 𝗅𝗂𝗌𝗍𝖾𝗒𝖾 𝖾𝗄𝗅𝖾𝗒𝗂𝗇.


/whitelistchat [CHAT_ID] 
- 𝖬𝗎𝗓𝗂𝗄 𝖻𝗈𝗍𝗎𝗇𝗎 𝗄𝗎𝗅𝗅𝖺𝗇𝖺𝗋𝖺𝗄 𝗁𝖾𝗋𝗁𝖺𝗇𝗀𝗂 𝖻𝗂𝗋 𝗌𝗈𝗁𝖻𝖾𝗍𝗂 𝖻𝖾𝗒𝖺𝗓 𝗅𝗂𝗌𝗍𝖾𝗒𝖾 𝖾𝗄𝗅𝖾𝗒𝗂𝗇

"""


@app.on_message(filters.command("blacklistchat") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝗆:**\n/blacklistchat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("𝖲𝗈𝗁𝖻𝖾𝗍 𝗓𝖺𝗍𝖾𝗇 𝗄𝖺𝗋𝖺 𝗅𝗂𝗌𝗍𝖾𝗒𝖾 𝖺𝗅𝗂𝗇𝖽𝗂.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text(
            "𝖲𝗈𝗁𝖻𝖾𝗍 𝖻𝖺𝗌𝖺𝗋𝗂𝗒𝗅𝖺 𝗄𝖺𝗋𝖺 𝗅𝗂𝗌𝗍𝖾𝗒𝖾 𝖺𝗅𝗂𝗇𝖽𝗂"
        )
    await message.reply_text("𝖸𝖺𝗇𝗅𝗂𝗌 𝖻𝗂𝗋 𝗌𝖾𝗒 𝗈𝗅𝖽𝗎, 𝗀𝗎𝗇𝗅𝗎𝗄𝗅𝖾𝗋𝗂 𝗄𝗈𝗇𝗍𝗋𝗈𝗅 𝖾𝖽𝗂𝗇.")


@app.on_message(filters.command("whitelistchat") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝗆:**\n/whitelistchat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("𝖲𝗈𝗁𝖻𝖾𝗍 𝗓𝖺𝗍𝖾𝗇 𝖻𝖾𝗒𝖺𝗓 𝗅𝗂𝗌𝗍𝖾𝖽𝖾.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "Sohbet başarıyla beyaz listeye alındı"
        )
    await message.reply_text("𝖸𝖺𝗇𝗅𝗂𝗌 𝖻𝗂𝗋 𝗌𝖾𝗒 𝗈𝗅𝖽𝗎, 𝗀𝗎𝗇𝗅𝗎𝗄𝗅𝖾𝗋𝗂 𝗄𝗈𝗇𝗍𝗋𝗈𝗅 𝖾𝖽𝗂𝗇.")


@app.on_message(filters.command("blacklistedchat"))
async def blacklisted_chats_func(_, message: Message):
    text = "**𝖪𝖺𝗋𝖺 𝗅𝗂𝗌𝗍𝖾𝗒𝖾 𝖺𝗅𝗂𝗇𝗆𝗂𝗌 𝖲𝗈𝗁𝖻𝖾𝗍𝗅𝖾𝗋**\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text("𝖪𝖺𝗋𝖺 𝗅𝗂𝗌𝗍𝖾𝗒𝖾 𝖺𝗅𝗂𝗇𝗆𝗂𝗌 𝖲𝗈𝗁𝖻𝖾𝗍 𝗒𝗈𝗄")
    else:
        await message.reply_text(text)
