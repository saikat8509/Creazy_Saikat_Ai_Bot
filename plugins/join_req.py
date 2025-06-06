from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS,MAX_SUBSCRIPTION_TIME,LAZYCONTAINER
from utils import temp,to_small_caps
from datetime import datetime, timedelta
import pytz
import logging
import asyncio
from Script import script
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import get_file_details
from database.users_chats_db import db
from info import *
#5 => verification_steps ! [Youtube@LazyDeveloperr]
from utils import  get_size, temp
from urllib.parse import quote
from utils import schedule_deletion, to_small_caps

import base64
logger = logging.getLogger(__name__)
from utils import temp
import pytz  # Make sure to handle timezone correctly

timezone = pytz.timezone("Asia/Kolkata")

@Client.on_chat_join_request(filters.chat(temp.ASSIGNED_CHANNEL))  # Fetch channels dynamically
async def join_reqs(client, message: ChatJoinRequest):
    try:

        user = await db.get_user(message.from_user.id)

        if user:
            joined_channels = set(user.get("joined_channels", []))
            if message.chat.id in joined_channels:
                logging.info(f"{message.chat.id} is already in joined channels list {joined_channels} ::>> for user ::> {message.from_user.first_name} \n🛑 STOPPED subscription process...")
                return
            joined_channels.add(message.chat.id)  
            await db.update_user({"id": message.from_user.id, "joined_channels": list(joined_channels)})

            user = await db.get_user(message.from_user.id)
            assigned_channels = set(user.get("assigned_channels"))  # Get assigned channels
            if assigned_channels.issubset(joined_channels):  # If all are joined
                lmg = []
                expiry_time = datetime.now(timezone) + timedelta(hours=MAX_SUBSCRIPTION_TIME)  # 24 hours from now
                expiry_str = expiry_time.strftime("%Y-%m-%d %H:%M:%S")  # Format as YYYY-MM-DD HH:MM:SS

                await db.update_user({"id": message.from_user.id, "subscription": "limited", "subscription_expiry": expiry_str})
                user_id = message.from_user.id
                if user_id in LAZYCONTAINER:
                    file_id = LAZYCONTAINER[user_id]["file_id"]
                    lazymsg = LAZYCONTAINER[user_id]["lazymsg"]
                    try:
                        lazy = await client.send_message(user_id, f"🎉")
                        await lazymsg.delete()
                        lmg.append(lazy)
                        await asyncio.sleep(3)
                    except Exception as e:
                        logging.info(f"Error deleting previous message: {e}")
                    files_ = await get_file_details(file_id)           
                    files = files_[0]
                    title = files.file_name
                    size=get_size(files.file_size)
                    f_caption=files.caption
                    if CUSTOM_FILE_CAPTION:
                        try:
                            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                        except Exception as e:
                            logger.exception(e)
                            f_caption=f_caption
                    if f_caption is None:
                        f_caption = f"{files.file_name}"

                    along_with_lazy_info = "**⚠ Auto-deleting in 1 minute ⚠**"
                    along_with_lazy_footer = f"**Dear {message.from_user.mention} ! <b>{script.DONATION_TEXT}</b>"
                    lazy_caption_template =f"{f_caption}\n\n{along_with_lazy_footer}"
                    share_url = f"https://t.me/{temp.U_NAME}?start=file_{file_id}"
                    sharelazymsg = f"{to_small_caps('•❤ Your favorite movies, just a tap away! ❤•')}\n{to_small_caps('🍿 Be the first to watch the latest movies! Join us now for unlimited entertainment!')}"
                    lazydeveloper_text = quote(sharelazymsg)
                    button = [[
                            InlineKeyboardButton(to_small_caps('🔁 Share with friends... 💕'), url=f"https://t.me/share/url?url={share_url}&text={lazydeveloper_text}")
                        
                        ],[
                            InlineKeyboardButton('😊 sᴜᴘᴘᴏʀᴛ ᴏᴜʀ ᴡᴏʀᴋ ᴡɪᴛʜ ᴀ ᴅᴏɴᴀᴛɪᴏɴ ♥️', url=DONATION_LINK),
                        ]]
                    keyboard = InlineKeyboardMarkup(button)
                    lazy_file = await client.send_cached_media(
                        chat_id=message.from_user.id,
                        file_id=file_id,
                        caption=lazy_caption_template,
                        reply_markup=keyboard,  
                        protect_content=PROTECT_CONTENT,
                        )
                    lmg.append(lazy_file)
                    # 
                    if await db.deduct_limit(user_id):
                        logging.info(f"\n\n::::::::::>> Deducted limit for user [{message.from_user.first_name}] AT : {datetime.now()}")
                    else:
                        logging.info(f"❤")
                    
                    asyncio.create_task(schedule_deletion(client, user_id, lmg, BATCH=True))

                    msg = await client.send_message(
                                                    user_id,
                                                    f"{script.VERIFIED_TEXT.format(message.from_user.mention, expiry_str)}",
                                                    parse_mode=enums.ParseMode.HTML,
                                                    disable_web_page_preview=True
                                                )
    except Exception as lazydeveloper:
        logging.info(f"Error: {lazydeveloper}")


@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.del_join_req()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")
