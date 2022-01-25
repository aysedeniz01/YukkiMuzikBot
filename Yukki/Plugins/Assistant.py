import random

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from Yukki import ASSISTANT_PREFIX, SUDOERS, app, random_assistant
from Yukki.Database import get_assistant, save_assistant
from Yukki.Utilities.assistant import get_assistant_details

__MODULE__ = "𝖠𝗌𝗂𝗌𝗍𝖺𝗇"
__HELP__ = f"""


/checkassistant
- 𝖲𝗈𝗁𝖻𝖾𝗍𝗂𝗇𝗂𝗓𝖾 𝗍𝖺𝗁𝗌𝗂𝗌 𝖾𝖽𝗂𝗅𝖾𝗇 𝗒𝖺𝗋𝖽𝗂𝗆𝖼𝗂𝗒𝗂 𝗄𝗈𝗇𝗋𝗍𝗈𝗅 𝖾𝖽𝗂𝗇.


**𝖭𝖮𝖳:**
- 𝖲𝖺𝖽𝖾𝖼𝖾 𝖲𝗎𝖽𝗈 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋𝗂 𝗂𝖼𝗂𝗇 𝗀𝖾𝖼𝖾𝗋𝗅𝗂𝖽𝗂𝗋.

{ASSISTANT_PREFIX[0]}block [ 𝖡𝗂𝗋 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝗆𝖾𝗌𝖺𝗃𝗂𝗇𝗂 𝗒𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇 ]
- 𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗒𝗂 𝖺𝗌𝗂𝗌𝗍𝖺𝗇 𝗁𝖾𝗌𝖺𝖻𝗂𝗇𝖽𝖺𝗇 𝖾𝗇𝗀𝖾𝗅𝗅𝖾𝗋.

{ASSISTANT_PREFIX[0]}unblock [ 𝖡𝗂𝗋 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝗆𝖾𝗌𝖺𝗃𝗂𝗇𝗂 𝗒𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇 ]
- 𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗇𝗂𝗇 𝖺𝗌𝗂𝗌𝗍𝖺𝗇 𝗁𝖾𝗌𝖺𝖻𝗂𝗇𝖽𝖺𝗄𝗂 𝖾𝗇𝗀𝖾𝗅𝗅𝖾𝗆𝖾𝗌𝗂𝗇𝗂 𝗄𝖺𝗅𝖽𝗂𝗋𝗂𝗋.

{ASSISTANT_PREFIX[0]}approve [ 𝖡𝗂𝗋 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝗆𝖾𝗌𝖺𝗃𝗂𝗇𝗂 𝗒𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇 ]
- 𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗒𝗂 𝖣𝖬 𝗂𝖼𝗂𝗇 𝗈𝗇𝖺𝗒𝗅𝖺𝗋.

{ASSISTANT_PREFIX[0]}disapprove [ 𝖡𝗂𝗋 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝗆𝖾𝗌𝖺𝗃𝗂𝗇𝗂 𝗒𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇 ]
- 𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗒𝗂 𝖣𝖬 𝗂𝖼𝗂𝗇 𝗈𝗇𝖺𝗒𝗅𝖺𝗆𝖺𝗓.

{ASSISTANT_PREFIX[0]}pfp [ 𝖡𝗂𝗋 𝖿𝗈𝗍𝗈𝗀𝗋𝖺𝖿𝗂 𝗒𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇 ]
- 𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝗁𝖾𝗌𝖺𝖻𝗂𝗇 PFP'𝗌𝗂𝗇𝗂 𝖽𝖾𝗀𝗂𝗌𝗍𝗂𝗋𝗂𝗋.

{ASSISTANT_PREFIX[0]}bio [ 𝖡𝗂𝗒𝗈 𝗆𝖾𝗍𝗂𝗇 ]
- 𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝗁𝖾𝗌𝖺𝖻𝗂𝗇𝗂𝗇 𝖻𝗂𝗒𝗈𝗀𝗋𝖺𝖿𝗂𝗌𝗂𝗇𝗂 𝖽𝖾𝗀𝗂𝗌𝗍𝗂𝗋𝗂𝗋.

/changeassistant [ 𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝗇𝗎𝗆𝖺𝗋𝖺𝗌𝗂 ]
- 𝖤𝗌𝗄𝗂 𝖺𝗌𝗂𝗌𝗍𝖺𝗇𝗂 𝗒𝖾𝗇𝗂𝗌𝗂𝗒𝗅𝖾 𝖽𝖾𝗀𝗂𝗌𝗍𝗂𝗋𝗂𝗋.

/setassistant [ 𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝗇𝗎𝗆𝖺𝗋𝖺𝗌𝗂 & 𝗋𝖺𝗌𝗍𝗀𝖾𝗅𝖾 ]
- 𝖲𝗈𝗁𝖻𝖾𝗍 𝗂𝖼𝗂𝗇 𝖻𝗂𝗋 𝖺𝗌𝗂𝗌𝗍𝖺𝗇 𝖺𝗒𝖺𝗋𝗅𝖺𝗒𝗂𝗇 .
"""


ass_num_list = ["1", "2", "3", "4", "5"]


@app.on_message(filters.command("changeassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝗆:**\n/changeassistant [ASS_NO]\n\n𝖠𝗋𝖺𝗅𝖺𝗋𝗂𝗇𝖽𝖺 𝗌𝖾𝖼𝗂𝗆 𝗒𝖺𝗉𝗂𝗇\n{' | '.join(ass_num_list)}"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    num = message.text.split(None, 1)[1].strip()
    if num not in ass_num_list:
        return await message.reply_text(usage)
    ass_num = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "𝖮𝗇𝖼𝖾𝖽𝖾𝗇 𝗄𝖺𝗒𝖽𝖾𝖽𝗂𝗅𝗆𝗂𝗌 𝖺𝗌𝗂𝗌𝗍𝖺𝗇 𝖻𝗎𝗅𝗎𝗇𝖺𝗆𝖺𝖽𝗂.\n\n𝖠𝗌𝗂𝗌𝗍𝖺𝗇𝗂 𝖺𝗒𝖺𝗋𝗅𝖺𝗒𝖺𝖻𝗂𝗅𝗂𝗋𝗌𝗂𝗇𝗂𝗓 /setassistant"
        )
    else:
        ass = _assistant["saveassistant"]
    assis = {
        "saveassistant": ass_num,
    }
    await save_assistant(message.chat.id, "assistant", assis)
    await message.reply_text(
        f"**𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝖣𝖾𝗀𝗂𝗌𝗍𝗂**\n\n𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝖧𝖾𝗌𝖺𝖻𝗂 𝖣𝖾𝗀𝗂𝗌𝗍𝗂𝗋𝗂𝗅𝖽𝗂 **{ass}** 𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝖭𝗎𝗆𝖺𝗋𝖺𝗌𝗂 **{ass_num}**"
    )


ass_num_list2 = ["1", "2", "3", "4", "5", "Random"]


@app.on_message(filters.command("setassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝗆:**\n/setassistant [𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝖭𝗎𝗆𝖺𝗋𝖺𝗌𝗂 & 𝖱𝖺𝗌𝗍𝗀𝖾𝗅𝖾 ]\n\n𝖠𝗋𝖺𝗅𝖺𝗋𝗂𝗇𝖽𝖺 𝗌𝖾𝖼𝗂𝗆 𝗒𝖺𝗉𝗂𝗇\n{' | '.join(ass_num_list2)}\n\nRastgele Asistanı ayarlamak için 'Rastgele'yi kullanın"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    query = message.text.split(None, 1)[1].strip()
    if query not in ass_num_list2:
        return await message.reply_text(usage)
    if str(query) == "Random":
        ran_ass = random.choice(random_assistant)
    else:
        ran_ass = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        await message.reply_text(
            f"**__𝖲𝗍𝖺𝗋 𝖬𝗎𝗌𝗂𝖼 𝖡𝗈𝗍 𝖠𝗌𝗂𝗌𝗍𝖺𝗇𝗂 𝖠𝗍𝖺𝗇𝖽𝗂__**\n\n𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝖧𝖺𝗒𝗂𝗋. **{ran_ass}**"
        )
        assis = {
            "saveassistant": ran_ass,
        }
        await save_assistant(message.chat.id, "assistant", assis)
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"𝖮𝗇𝖼𝖾𝖽𝖾𝗇 𝗄𝖺𝗒𝖽𝖾𝖽𝗂𝗅𝗆𝗂𝗌 𝖺𝗌𝗂𝗌𝗍𝖺𝗇 𝗇𝗎𝗆𝖺𝗋𝖺𝗌𝗂 𝖻𝗎𝗅𝗎𝗇𝖽𝗎.{ass}\n\n𝖠𝗌𝗂𝗌𝗍𝖺𝗇𝗂 𝖣𝖾𝗀𝗂𝗌𝗍𝗂𝗋𝖾𝖻𝗂𝗅𝗂𝗋𝗌𝗂𝗇𝗂𝗓 /changeassistant"
        )


@app.on_message(filters.command("checkassistant") & filters.group)
async def check_ass(_, message: Message):
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "𝖮𝗇𝖼𝖾𝖽𝖾𝗇 𝗄𝖺𝗒𝖽𝖾𝖽𝗂𝗅𝗆𝗂𝗌 𝖺𝗌𝗂𝗌𝗍𝖺𝗇 𝖻𝗎𝗅𝗎𝗇𝖺𝗆𝖺𝖽𝗂.\n\n𝖠𝗌𝗂𝗌𝗍𝖺𝗇𝗂 𝖺𝗒𝖺𝗋𝗅𝖺𝗒𝖺𝖻𝗂𝗅𝗂𝗋𝗌𝗂𝗇𝗂𝗓 /play"
        )
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"𝖮𝗇𝖼𝖾𝖽𝖾𝗇 𝗄𝖺𝗒𝖽𝖾𝖽𝗂𝗅𝗆𝗂𝗌 𝖺𝗌𝗂𝗌𝗍𝖺𝗇 𝖻𝗎𝗅𝗎𝗇𝖽𝗎\n\n𝖠𝗌𝗂𝗌𝗍𝖺𝗇 𝖻𝗎𝗅𝗎𝗇𝖽𝗎 {ass} "
        )
