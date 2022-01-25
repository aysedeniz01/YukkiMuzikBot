from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import SUDOERS, app
from Yukki.Database import (_get_authusers, delete_authuser, get_authuser,
                            get_authuser_count, get_authuser_names,
                            save_authuser)
from Yukki.Decorators.admins import AdminActual
from Yukki.Utilities.changers import (alpha_to_int, int_to_alpha,
                                      time_to_seconds)

__MODULE__ = "𝖠𝗎𝗍𝗁 𝖴𝗌𝖾𝗋"
__HELP__ = """

**𝖭𝖮𝖳:**
-𝖸𝖾𝗍𝗄𝗂𝗅𝖾𝗇𝖽𝗂𝗋𝗆𝖾 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋𝗂; 𝖸𝗈𝗇𝖾𝗍𝗂𝖼𝗂 𝗈𝗅𝗆𝖺𝖽𝖺𝗇 𝗌𝖾𝗌𝗅𝗂 𝗌𝗈𝗁𝖻𝖾𝗍𝗅𝖾𝗋𝗂 𝖺𝗍𝗅𝖺𝗒𝖺𝖻𝗂𝗅𝗂𝗋, 𝖽𝗎𝗋𝖽𝗎𝗋𝖺𝖻𝗂𝗅𝗂𝗋, 𝗌𝗈𝗇𝗅𝖺𝗇𝖽𝗂𝗋𝖺𝖻𝗂𝗅𝗂𝗋, 𝖽𝖾𝗏𝖺𝗆 𝖾𝗍𝗍𝗂𝗋𝖾𝖻𝗂𝗅𝗂𝗋.


/auth [ 𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝖺𝖽𝗂 & 𝖻𝗂𝗋 𝗆𝖾𝗌𝖺𝗃𝗂 𝗒𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇 ] 
- 𝖦𝗋𝗎𝖻𝗎𝗇 𝖸𝖤𝖳𝖪𝖨 𝖫𝖨𝖲𝖳𝖤𝖲𝖨'𝗇𝖾 𝖻𝗂𝗋 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝖾𝗄𝗅𝖾𝗒𝗂𝗇.

/unauth [ 𝖪𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝖺𝖽𝗂 & 𝖻𝗂𝗋 𝗆𝖾𝗌𝖺𝗃𝗂 𝗒𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇 ] 
- 𝖦𝗋𝗎𝖻𝗎𝗇 𝖸𝖤𝖳𝖪𝖨 𝖫𝖨𝖲𝖳𝖤𝖲𝖨'𝗇𝖽𝖾𝗇 𝖻𝗂𝗋 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗒𝗂 𝗄𝖺𝗅𝖽𝗂𝗋𝗂𝗇.

/authusers 
- 𝖦𝗋𝗎𝖻𝗎𝗇 𝖸𝖤𝖳𝖪𝖨 𝖫𝖨𝖲𝖳𝖤𝖲𝖨'𝗇𝗂 𝗄𝗈𝗇𝗍𝗋𝗈𝗅 𝖾𝖽𝗂𝗇.
"""


@app.on_message(filters.command("auth") & filters.group)
@AdminActual
async def auth(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "𝖡𝗂𝗋 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗇𝗂𝗇 𝗆𝖾𝗌𝖺𝗃𝗂𝗇𝗂 𝗒𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇 𝗏𝖾𝗒𝖺 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝖺𝖽𝗂 𝗏𝖾𝗋𝗂𝗇/user_id."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        user_id = message.from_user.id
        token = await int_to_alpha(user.id)
        from_user_name = message.from_user.first_name
        from_user_id = message.from_user.id
        _check = await get_authuser_names(message.chat.id)
        count = 0
        for smex in _check:
            count += 1
        if int(count) == 20:
            return await message.reply_text(
                "You can only have 20 Users In Your Groups Authorised Users List (AUL)"
            )
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            await save_authuser(message.chat.id, token, assis)
            await message.reply_text(
                f"𝖡𝗎 𝗀𝗋𝗎𝖻𝗎𝗇 𝗒𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋 𝗅𝗂𝗌𝗍𝖾𝗌𝗂𝗇𝖾 𝖾𝗄𝗅𝖾𝗇𝖽𝗂."
            )
            return
        else:
            await message.reply_text(f"𝖹𝖺𝗍𝖾𝗇 𝗒𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋 𝗅𝗂𝗌𝗍𝖾𝗌𝗂𝗇𝖽𝖾.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    token = await int_to_alpha(user_id)
    from_user_name = message.from_user.first_name
    _check = await get_authuser_names(message.chat.id)
    count = 0
    for smex in _check:
        count += 1
    if int(count) == 20:
        return await message.reply_text(
            "You can only have 20 Users In Your Groups Authorised Users List (AUL)"
        )
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        await save_authuser(message.chat.id, token, assis)
        await message.reply_text(
            f"𝖡𝗎 𝗀𝗋𝗎𝖻𝗎𝗇 𝗒𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋 𝗅𝗂𝗌𝗍𝖾𝗌𝗂𝗇𝖾 𝖾𝗄𝗅𝖾𝗇𝖽𝗂."
        )
        return
    else:
        await message.reply_text(f"Already in the Authorised Users List.")


@app.on_message(filters.command("unauth") & filters.group)
@AdminActual
async def whitelist_chat_func(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "𝖡𝗂𝗋 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗇𝗂𝗇 𝗆𝖾𝗌𝖺𝗃𝗂𝗇𝗂 𝗒𝖺𝗇𝗂𝗍𝗅𝖺𝗒𝗂𝗇 𝗏𝖾𝗒𝖺 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝖺𝖽𝗂 𝗏𝖾𝗋𝗂𝗇/user_id."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(message.chat.id, token)
        if deleted:
            return await message.reply_text(
                f"𝖡𝗎 𝗀𝗋𝗎𝖻𝗎𝗇 𝗒𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋 𝗅𝗂𝗌𝗍𝖾𝗌𝗂𝗇𝖽𝖾𝗇 𝗄𝖺𝗅𝖽𝗂𝗋𝗂𝗅𝖽𝗂."
            )
        else:
            return await message.reply_text(f"𝖸𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝖽𝖾𝗀𝗂𝗅.")
    user_id = message.reply_to_message.from_user.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(message.chat.id, token)
    if deleted:
        return await message.reply_text(
            f"𝖡𝗎 𝗀𝗋𝗎𝖻𝗎𝗇 𝗒𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋 𝗅𝗂𝗌𝗍𝖾𝗌𝗂𝗇𝖽𝖾𝗇 𝗄𝖺𝗅𝖽𝗂𝗋𝗂𝗅𝖽𝗂."
        )
    else:
        return await message.reply_text(f"𝖸𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝖽𝖾𝗀𝗂𝗅.")


@app.on_message(filters.command("authusers") & filters.group)
async def authusers(_, message: Message):
    _playlist = await get_authuser_names(message.chat.id)
    if not _playlist:
        return await message.reply_text(
            f"𝖡𝗎 𝗀𝗋𝗎𝖻𝗍𝖺 𝗒𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂 𝗒𝗈𝗄.\n\n𝖸𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋𝗂 𝖾𝗄𝗅𝖾 /auth 𝗏𝖾𝗒𝖺 𝖼𝗂𝗄𝖺𝗋 /unauth."
        )
    else:
        j = 0
        m = await message.reply_text(
            "𝖸𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋 𝖺𝗅𝗂𝗇𝗂𝗒𝗈𝗋... 𝖫𝗎𝗍𝖿𝖾𝗇 𝖡𝖾𝗄𝗅𝖾𝗒𝗂𝗇"
        )
        msg = f"**𝖸𝖾𝗍𝗄𝗂𝗅𝗂 𝗄𝗎𝗅𝗅𝖺𝗇𝗂𝖼𝗂𝗅𝖺𝗋 𝗅𝗂𝗌𝗍𝖾𝗌𝗂[AUL]:**\n\n"
        for note in _playlist:
            _note = await get_authuser(message.chat.id, note)
            user_id = _note["auth_user_id"]
            user_name = _note["auth_name"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_users(user_id)
                user = user.first_name
                j += 1
            except Exception:
                continue
            msg += f"{j}➤ {user}[`{user_id}`]\n"
            msg += f"    ┗ Added By:- {admin_name}[`{admin_id}`]\n\n"
        await m.edit_text(msg)
