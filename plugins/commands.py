import os
import logging
import random
import asyncio
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Message
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import *
#5 => verification_steps ! [Youtube@LazyDeveloperr]
from utils import  check_verification, imdb,  get_token,  verify_user, check_token, get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
from urllib.parse import quote
import datetime
from utils import get_seconds,lazy_readable,schedule_deletion, lazy_has_subscribed, to_small_caps, get_shortlink
from database.users_chats_db import db 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
import re
import json
import base64
logger = logging.getLogger(__name__)
import math
from pyrogram.errors import MessageNotModified,PeerIdInvalid,FloodWait
from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL, CHANNELS_PER_PAGE, LAZYCONTAINER
from utils import temp
import re
from math import ceil
import pytz  # Make sure to handle timezone correctly
timezone = pytz.timezone("Asia/Kolkata")
from PIL import Image

# the Strings used for this "thing"
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from database.lazy_ffmpeg import take_screen_shot
from random import choice

BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    try:
        user_id = message.from_user.id
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            buttons = [[
                    InlineKeyboardButton('𓆩ཫ⛱ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ⛱ཀ𓆪', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('✇ Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟꜱ ✇', callback_data='main_channel')
                  ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
            await asyncio.sleep(2) # 😢 https://github.com/LazyDeveloperr/LazyPrincess/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
            if not await db.get_chat(message.chat.id):
                total=await client.get_chat_members_count(message.chat.id)
                await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
                await db.add_chat(message.chat.id, message.chat.title)
            return 
        if not await db.is_user_exist(message.from_user.id):
            await db.add_user(message.from_user.id, message.from_user.first_name)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
        if len(message.command) != 2:
            buttons = [[
                    InlineKeyboardButton('➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                    ],
                    [
                    InlineKeyboardButton('🍿 ᴜᴘᴅᴀᴛᴇs', url=f'https://t.me/vj_botz'),
                    InlineKeyboardButton('🤖 ʙᴏᴛs', url=f'https://t.me/vj_bots')
                    ],[
                    InlineKeyboardButton('🎬 ʜᴇʟᴘ', callback_data='help'),
                    InlineKeyboardButton('❤️ ɢʀᴏᴜᴘ', url=f'https://t.me/+cBX3YJbHToU0ZjNl'),
                    ],[
                    InlineKeyboardButton('☻︎ ʜᴇʟᴘ ᴜs ʙʏ ᴍᴀᴋɪɴɢ ᴀ ᴅᴏɴᴀᴛɪᴏɴ ☻︎', url=DONATION_LINK),
                    ]]

            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_photo(
                photo=random.choice(PICS),
                caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                has_spoiler=True
            )
            return
        

        if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:

            buttons = [[
                    InlineKeyboardButton('➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                    ],
                    [
                    InlineKeyboardButton('🍿 ᴜᴘᴅᴀᴛᴇs', url=f'https://t.me/vj_botz'),
                    InlineKeyboardButton('🤖 ʙᴏᴛs', url=f'https://t.me/vj_bots')
                    ],[
                    InlineKeyboardButton('🎬 ʜᴇʟᴘ', callback_data='help'),
                    InlineKeyboardButton('❤️ ɢʀᴏᴜᴘ', url=f'https://t.me/+cBX3YJbHToU0ZjNl'),
                    ],[
                    InlineKeyboardButton('☻︎ ʜᴇʟᴘ ᴜs ʙʏ ᴍᴀᴋɪɴɢ ᴀ ᴅᴏɴᴀᴛɪᴏɴ ☻︎', url=DONATION_LINK),
                    ]]

            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_photo(
                photo=random.choice(PICS),
                caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                has_spoiler=True
            )
            return
        data = message.command[1]
        try:
            pre, file_id = data.split('_', 1)
        except:
            file_id = data
            pre = ""
# ==========================🚧 BARIER 1 🚧 ==========================================
        if AUTH_CHANNEL and not await lazy_has_subscribed(client, message):
            lazydeloper = 0
            lazybuttons = []
            for channel in AUTH_CHANNEL:
                lazydeloper = lazydeloper + 1
                try:
                    invite_link = await client.create_chat_invite_link(int(channel), creates_join_request=False)
                except ChatAdminRequired:
                    logger.error("Initail Force Sub is not working because of ADMIN ISSUE. Please make me admin there ⚠️")
                    return
                lazybuttons.append([
                            InlineKeyboardButton(text=f"🔰 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ✅ {lazydeloper} •", url=invite_link.invite_link),
                            ])

            if message.command[1] != "subscribe":
                try:
                    kk, file_id = message.command[1].split("_", 1)
                    pre = 'checksubp' if kk == 'filep' else 'checksub' 
                    lazybuttons.append([InlineKeyboardButton(f"♻ • {to_small_caps('Click To Verify')} • ♻", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
                except (IndexError, ValueError):
                    lazybuttons.append([InlineKeyboardButton(f"♻ • {to_small_caps('Click To Verify')} • ♻", callback_data=f"{pre}#{file_id}")])
            await client.send_message(
                chat_id=message.from_user.id,
                text=f"{script.FORCESUB_MSG.format(message.from_user.mention)}",
                reply_markup=InlineKeyboardMarkup(lazybuttons),
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
                )
            return            
# ====================================================================
# ==========================🚧 BARIER 2 🚧 ==========================================
        if pre != "" and file_id != "requestmovie":
            lzy = message.from_user.first_name
            daily_limit, subscription, assigned_channels, al_joined_channels= await lazybarier(client, lzy, user_id)
            # Limit free users to 3 videos per day
            if subscription == "free" and daily_limit <= 0:
                try:
                    lazybtn = []
                    lazydeloper = 0
                    for channel in assigned_channels:
                        if await is_subscribed(client, channel, user_id):
                            await db.users.update_one(
                                    {"id": user_id},
                                    {"$addToSet": {"joined_channels": channel}},  # Append channel if not already present
                                    upsert=True
                                )
                            updated_data = await db.get_user(user_id)
                            joined_channels = set(updated_data.get("joined_channels", []))
                            if assigned_channels.issubset(joined_channels):
                                expiry_time = datetime.datetime.now(timezone) + datetime.timedelta(hours=MAX_SUBSCRIPTION_TIME)  # 24 hours from now
                                expiry_str = expiry_time.strftime("%Y-%m-%d %H:%M:%S")  # Format as YYYY-MM-DD HH:MM:SS
                                await db.update_user({"id": message.from_user.id, "subscription": "limited", "subscription_expiry": expiry_str})
                                msg = await client.send_message(
                                                    user_id,
                                                    f"{script.VERIFIED_TEXT.format(message.from_user.mention, expiry_str)}",
                                                    parse_mode=enums.ParseMode.HTML,
                                                    disable_web_page_preview=True
                                                )
                        else:
                            lazydeloper = lazydeloper + 1
                            invite_link = await client.create_chat_invite_link(int(channel), creates_join_request=True)
                            lazybtn.append([
                                    InlineKeyboardButton(f"{to_small_caps('🔰 Join Channel ✅')} {lazydeloper}", url=invite_link.invite_link),
                                    ]) # bahut deemag khraab hua h is feature ko add krne mei #lazydeveloper 😢
                    
                    lazy_updated_data = await db.get_user(user_id)
                    lazy_joined_channels = set(lazy_updated_data.get("joined_channels", []))
                    if not assigned_channels.issubset(lazy_joined_channels):
                        if message.command[1] != "subscribe":
                            try:
                                kk, file_id = message.command[1].split("_", 1)
                                pre = 'checksubp' if kk == 'filep' else 'checksub' 
                                lazybtn.append([InlineKeyboardButton(f"♻ • {to_small_caps('Click To Verify')} • ♻", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
                            except (IndexError, ValueError):
                                lazybtn.append([InlineKeyboardButton(f"♻ ♡ • {to_small_caps('Click To Verify')} • ♡ ♻", callback_data=f"{pre}#{file_id}")])

                        # 

                        lazz = await message.reply_text(to_small_caps(script.UPGRADE_TEXT),
                                reply_markup=InlineKeyboardMarkup(lazybtn)
                                    )
                        LAZYCONTAINER[user_id] = {
                                "lazymsg": lazz,
                                "file_id": file_id,
                                "the_one&only_LazyDeveloper": True
                            }
                        return
                except Exception as e:
                    logging.info(f"Error in Barier: {e}")
                    return await message.reply(f"{script.FAILED_VERIFICATION_TEXT}")                

# ===========================[ ❤ PASS 🚀 ]======================================

        # if data.startswith("sendfiles"):
        #     try:
        #         userid = message.from_user.id if message.from_user else None
        #         chat_id = int("-" + file_id.split("-")[1])
        
        #         ghost_url = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=allfiles_{file_id}")

        #         client_msg = await client.send_message(
        #             chat_id=userid,
        #             text=f"👋 Hey {message.from_user.mention}\n\nDownload Link Generated ✔, Kindly click on download button below 👇 .\n\n",
        #             reply_markup=InlineKeyboardMarkup(
        #                 [
        #                     [
        #                         InlineKeyboardButton('📁 ᴅᴏᴡɴʟᴏᴀᴅ 📁', url=ghost_url)
        #                     ],
        #                     [
        #                         InlineKeyboardButton('⚡ ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ⚡', url=f"https://t.me/+lI9zStHfHlllNjQ1")
        #                     ]
        #                 ]
        #             )
        #         )

        #         await asyncio.sleep(1800)
        #         await client_msg.edit("<b>ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ ɪꜱ ᴅᴇʟᴇᴛᴇᴅ !\nᴋɪɴᴅʟʏ ꜱᴇᴀʀᴄʜ ᴀɢᴀɪɴ.</b>")
        #         return
        #     except Exception as e:
        #         logging.info(f"Error handling sendfiles: {e}")

        # if data.startswith("short"):         
        #     user_id = message.from_user.id
        #     chat_id = temp.SHORT.get(user_id)
        #     files_ = await get_file_details(file_id)

        #     files = files_[0]
        #     ghost = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
        #     k = await client.send_message(
        #         chat_id=user_id,
        #         text=f"🫂 ʜᴇʏ {message.from_user.mention}\n\n✅ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴅᴏᴡɴʟᴏᴀᴅ ʙᴜᴛᴛᴏɴ.\n\n⚠️ ꜰɪʟᴇ ɴᴀᴍᴇ : <code>{files.file_name}</code> \n\n⚕ ꜰɪʟᴇ ꜱɪᴢᴇ : <code>{get_size(files.file_size)}</code>\n\n",
        #         reply_markup=InlineKeyboardMarkup(
        #             [[
        #                 InlineKeyboardButton('📁 ᴅᴏᴡɴʟᴏᴀᴅ 📁', url=ghost)
        #             ],
        #             [
        #                 InlineKeyboardButton('⚡ ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ⚡', url=f"https://t.me/+lI9zStHfHlllNjQ1")
        #             ]]
        #         )
        #     )
        #     await asyncio.sleep(600)
        #     await k.edit("<b>ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ ɪꜱ ᴅᴇʟᴇᴛᴇᴅ !\nᴋɪɴᴅʟʏ ꜱᴇᴀʀᴄʜ ᴀɢᴀɪɴ.</b>")
        #     return

# ===========================[ ❤ PASS 🚀 ]======================================
        if data.startswith("all"):
            user_id = message.from_user.id
            files = temp.GETALL.get(file_id)
            if not files:
                return await message.reply('<b><i>ɴᴏ ꜱᴜᴄʜ ꜰɪʟᴇ ᴇxɪꜱᴛꜱ !</b></i>')
            lazyfiles = []
            for file in files:
                file_id = file.file_id
                files_ = await get_file_details(file_id)
                files1 = files_[0]
                title = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))
                size=get_size(files1.file_size)
                f_caption=files1.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                    except Exception as e:
                        logger.exception(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))}"
                
                share_url = f"https://t.me/{temp.U_NAME}?start=file_{file_id}"
                sharelazymsg = f"{to_small_caps('•❤ Your favorite movies, just a tap away! ❤•')}\n{to_small_caps('🍿 Be the first to watch the latest movies! Join us now for unlimited entertainment!')}"
                lazydeveloper_text = quote(sharelazymsg)
                lazybtn = [[
                        InlineKeyboardButton(to_small_caps(f"🔁 Share this file... 💕"), url=f"https://t.me/share/url?url={share_url}&text={lazydeveloper_text}")
                    
                    ],[
                        InlineKeyboardButton('😊 • ᴅᴏɴᴀᴛᴇ ᴜꜱ • ♥️', url=DONATION_LINK),
                    ]]
                msg = await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(lazybtn),
                    protect_content=True if pre == 'filep' else False
                    )
                lazyfiles.append(msg)
            
            if await db.deduct_limit(user_id):
                logging.info(f"\n\n::::::::::>> Deducted limit for user [{message.from_user.first_name}] |::> ♻ REMAINING : {daily_limit} |::> AT : {datetime.datetime.now()}")
            else:
                logging.info(f"❤")

            asyncio.create_task(schedule_deletion(client, message.chat.id, lazyfiles, BATCH=True))

            return
        
        # elif data.startswith("files"):
        #     user_id = message.from_user.id

        #     if temp.SHORT.get(user_id)==None:
        #         return await message.reply_text(text="<b>Please Search Again in Group</b>")
        #     else:
        #         chat_id = temp.SHORT.get(user_id)
        #     settings = await get_settings(chat_id)
        #     if not await db.has_prime_status(user_id) and settings['url_mode']:
        #         files_ = await get_file_details(file_id)
        #         files = files_[0]
        #         generatedurl = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
        #         k = await client.send_message(chat_id=message.from_user.id,text=f"🫂 ʜᴇʏ {message.from_user.mention}\n\n✅ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴅᴏᴡɴʟᴏᴀᴅ ʙᴜᴛᴛᴏɴ.\n\n⚠️ ꜰɪʟᴇ ɴᴀᴍᴇ : <code>{files.file_name}</code> \n\n⚕ ꜰɪʟᴇ ꜱɪᴢᴇ : <code>{get_size(files.file_size)}</code>\n\n", reply_markup=InlineKeyboardMarkup(
        #                 [
        #                     [
        #                         InlineKeyboardButton('📁 ᴅᴏᴡɴʟᴏᴀᴅ 📁', url=generatedurl)
        #                     ],
        #                     [
        #                         InlineKeyboardButton('⚡ ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ⚡', url=f"https://t.me/+W1v7gkr5HAhmOWM1")
        #                     ],
        #                     [
        #                         InlineKeyboardButton('💸 ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ʀᴇᴍᴏᴠᴇ ᴀᴅꜱ 💸', callback_data='seeplans')
        #                     ]
        #                 ]
        #             )
        #         )
        #         await asyncio.sleep(600)
        #         await k.edit("<b>ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ ɪꜱ ᴅᴇʟᴇᴛᴇᴅ !\nᴋɪɴᴅʟʏ ꜱᴇᴀʀᴄʜ ᴀɢᴀɪɴ.</b>")
        #         return
        
        elif data.startswith("requestmovie"):
            user_id = message.chat.id
            await message.delete()
            await message.reply_text("<i><b>»» Please enter a movie or series name along with year of release...</b></i>",	
            reply_to_message_id=message.id,  
            reply_markup=ForceReply(True)) 


        files_ = await get_file_details(file_id)           
        if not files_:
            pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
            try:                
                share_url = f"https://t.me/{temp.U_NAME}?start=file_{file_id}"
                sharelazymsg = f"{to_small_caps('•❤ Your favorite movies, just a tap away! ❤•')}\n{to_small_caps('🍿 Be the first to watch the latest movies! Join us now for unlimited entertainment!')}"
                lazydeveloper_text = quote(sharelazymsg)
                button = [[
                        InlineKeyboardButton(to_small_caps('🔄 Share with friends... 💕'), url=f"https://t.me/share/url?url={share_url}&text={lazydeveloper_text}")
                    
                    ],[
                        InlineKeyboardButton('😊 • ᴅᴏɴᴀᴛᴇ ᴜꜱ • ♥️', url=DONATION_LINK),
                    ]]                # Create the inline keyboard markup with the button
                keyboard = InlineKeyboardMarkup(button)
                msg = await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=file_id,
                    reply_markup=keyboard,
                    protect_content=True if pre == 'filep' else False,
                    )
                
                filetype = msg.media
                file = getattr(msg, filetype.value)
                title = file.file_name
                size=get_size(file.file_size)
                f_caption = f"<code>{title}</code>"
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                    except:
                        return
                along_with_lazy_info = "**⚠ DELETING IN 10 minute ⚠**"
                along_with_lazy_footer = f"**Dear {message.from_user.mention} ! <b>{script.DONATION_TEXT}</b>"
                lazy_caption_template =f"{f_caption}\n\n{along_with_lazy_footer}"
                await msg.edit_caption(lazy_caption_template)
                
                asyncio.create_task(schedule_deletion(client, message.chat.id, msg))

                return
            except:
                pass
            return await message.reply('No such file exist.')
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

        along_with_lazy_info = "**⚠ DELETING IN 10 minute ⚠**"
        along_with_lazy_footer = f"**Dear {message.from_user.mention} ! <b>{script.DONATION_TEXT}</b>"
        lazy_caption_template =f"{f_caption}\n\n{along_with_lazy_footer}"
        share_url = f"https://t.me/{temp.U_NAME}?start=file_{file_id}"
        sharelazymsg = f"{to_small_caps('•❤ Access file at your fingertip ❤•')}\n{to_small_caps('🤝 Join us now for the latest movies and entertainment!')}"
        lazydeveloper_text = quote(sharelazymsg)
        button = [[
                InlineKeyboardButton(to_small_caps('🔄 Share with friends... 💕'), url=f"https://t.me/share/url?url={share_url}&text={lazydeveloper_text}")
            
            ],[
                InlineKeyboardButton('😊 • ᴅᴏɴᴀᴛᴇ ᴜꜱ • ♥️', url=DONATION_LINK),
            ]]
        # Create the inline keyboard markup with the button
        keyboard = InlineKeyboardMarkup(button)
        lazy_file = await client.send_cached_media(
            chat_id=message.from_user.id,
            file_id=file_id,
            caption=lazy_caption_template,
            reply_markup=keyboard,  # Use the created keyboard
            protect_content=True if pre == 'filep' else False,
            )

        # 
        if await db.deduct_limit(user_id):
            logging.info(f"\n\n::::::::::>> Tried to Deduct limit for user [{message.from_user.first_name}] :|::> ID ::> {user_id} :|::> AT : {datetime.datetime.now()}")
        else:
            logging.info(f"❤")
        
        asyncio.create_task(schedule_deletion(client, message.chat.id, lazy_file))

    except Exception as lazydeveloper:
        logging.info(lazydeveloper)

# 
async def lazybarier(bot, l, user_id):
    user = await db.get_user(user_id) # user ko database se call krna h
    all_channels = await db.get_required_channels()
    # if isinstance(AUTH_CHANNEL, int):  
    #     all_channels.append(AUTH_CHANNEL)  # Lazy  
    # else:
    #     all_channels.extend(AUTH_CHANNEL)  # Lazy  
    temp.ASSIGNED_CHANNEL = all_channels
    # 
    if not user:
        joined_channels = set()
        for channel in all_channels:
            if await is_subscribed(bot, channel, user_id):
                joined_channels.add(channel)

        today = str(datetime.date.today())
        # new_assigned_channels = set(random.sample(all_channels, 2)) #  
        # new_assigned_channels = set(sorted(all_channels, reverse=True)[:2])
        new_assigned_channels = set(sorted(set(all_channels) - joined_channels)[:2])

        attach_data = {
            "id": user_id,
            "subscription": "free",
            "subscription_expiry": None,
            "daily_limit": DAILY_LIMIT,
            "assigned_channels": list(new_assigned_channels),
            "joined_channels": list(joined_channels) ,
            "last_access": today
        }
        await db.update_user(attach_data)
        user = await db.get_user(user_id)
    subscription = user.get("subscription", "free")
    subscription_expiry = user.get("subscription_expiry")
    daily_limit = user.get("daily_limit", DAILY_LIMIT)
    last_access = user.get("last_access")
    assigned_channels = set(user.get("assigned_channels", []))
    joined_channels = set(user.get("joined_channels", []))
    
    today = str(datetime.date.today())
    if last_access != today:
        if subscription == "free":
            for channel in all_channels:
                if await is_subscribed(bot, channel, user_id):
                    joined_channels.add(channel)
            new_channels = set(sorted(set(all_channels) - joined_channels)[:2])
            if not new_channels:
                joined_channels = set()  # Reset joined channels
                new_channels = set(random.sample(all_channels, 2))  # Pick 2 random channels

            data = {"id": user_id,
                    "daily_limit": DAILY_LIMIT, 
                    "last_access": today,
                    "assigned_channels": list(new_channels),
                    "joined_channels": list(joined_channels),
                    }
            await db.update_user(data)

    # Check for expired subscriptions
    # sabko indian time zone ke hisab se chlna pdega #LazyDeveloper 😂
    if subscription == "limited" and subscription_expiry:
        expiry_time = datetime.datetime.strptime(subscription_expiry, "%Y-%m-%d %H:%M:%S")
        expiry_time = timezone.localize(expiry_time)  # Ensure expiry time is in UTC
        current_time = datetime.datetime.now(timezone)  # Current time in IST
        if current_time > expiry_time:
            for channel in all_channels:
                if await is_subscribed(bot, channel, user_id):
                    joined_channels.add(channel)
            new_channels = set(sorted(set(all_channels) - joined_channels)[:2])
            if not new_channels:
                joined_channels = set()  # Reset joined channels
                new_channels = set(random.sample(all_channels, 2))  # Pick 2 random channels
            usersdata = {
                "id": user_id,
                "subscription": "free", 
                "subscription_expiry": None, 
                "daily_limit": DAILY_LIMIT,
                "assigned_channels": list(new_channels),
                "joined_channels": list(joined_channels),
                }
            await db.update_user(usersdata)

    updated_data = await db.get_user(user_id)
    daily_limit = updated_data.get("daily_limit", DAILY_LIMIT)
    subscription = updated_data.get("subscription", "free")
    assigned_channels = set(updated_data.get("assigned_channels", []))
    joined_channels = set(updated_data.get("joined_channels", []))
    logging.info(f"""\n\n
    [:::::::::::[ x❤x User Details x❤x ]:::::::::::]
    [::>> USER ID : {user_id}
    [::>> NAME : {l}
    [::>> DAILY_LIMIT : {daily_limit}
    [::>> SUBSCRIPTION : {subscription}
    [::>> EXPIRY TIME : {subscription_expiry}
    [::>> ASSIGNED CHANNELS : {assigned_channels}
    [::>> JOINED CHANNELS : {joined_channels}
    [::::::::::::::::::::::::::::::::::::::::::::::::]\n\n
""")
    return daily_limit, subscription, assigned_channels,joined_channels

@Client.on_message(filters.command("reset_user") & filters.user(ADMINS))  # Only admin can use it
async def delete_user(client, message):
    try:
        # Extract user ID from the command
        if len(message.command) < 2:
            return await message.reply_text("❌ **Usage:** `/reset_user <user_id>`")
        
        target_user_id = int(message.command[1])

        # Delete user from database
        result = await db.users.delete_one({"id": target_user_id})

        if result.deleted_count > 0:
            await message.reply_text(f"✅ **User {target_user_id} has been removed from the database!**")
        else:
            await message.reply_text(f"⚠️ **User {target_user_id} not found in the database!**")

    except Exception as e:
        await message.reply_text("⚠️ **Failed to delete user. Check logs for details.**")




# reset assigned channels:

@Client.on_message(filters.command("sold_channel") & filters.user(ADMINS))
async def sold_channel(bot, message):
    try:
        if len(message.command) < 2:
            return await message.reply_text("❌ Invalid command usage!\n\nUse: `sold_channel <channel_id>`")

        sold_channel_id = int(message.command[1])

        all_channels = await db.get_required_channels()  # Ensure awaiting

        users = await db.get_all_joins()  # Ensure awaiting
        
        affected_users = []
        async for user in users:
            if sold_channel_id in user.get("assigned_channels", []):
                affected_users.append(user)
        print(affected_users)

        if not affected_users:
            return await message.reply("✅ No users were assigned to this channel.", quote=True)

        for user in affected_users:
            user_id = user["id"]
            assigned_channels = set(user["assigned_channels"])
            assigned_channels.discard(sold_channel_id)

            available_channels = set(all_channels) - assigned_channels
            if available_channels:
                new_channel = choice(list(available_channels))
                assigned_channels.add(new_channel)

                await db.update_user({
                    "id": user_id,
                    "assigned_channels": list(assigned_channels)
                })

        await message.reply(f"✅ The channel `{sold_channel_id}` has been removed & replaced for affected users.", quote=True)
    except Exception as lazyerror:
        print(lazyerror)

@Client.on_message(filters.command("user_info") & filters.user(ADMINS))
async def user_info(bot, message):
    try:
        user_id = int(message.text.split()[1])  # Extract user ID from command
    except (IndexError, ValueError):
        return await message.reply("❌ Invalid command usage!\n\nUse: `/user_info <user_id>`", quote=True)

    user = await db.get_user(user_id)  # Fetch user data from DB

    if not user:
        return await message.reply(f"❌ No data found for user `{user_id}`.", quote=True)

    # Extract user details
    subscription = user.get("subscription", "free")
    subscription_expiry = user.get("subscription_expiry", "N/A")
    daily_limit = user.get("daily_limit", "N/A")
    last_access = user.get("last_access", "N/A")
    assigned_channels = user.get("assigned_channels", [])
    joined_channels = user.get("joined_channels", [])

    # Format the response
    user_info_text = f"""
**👤 User Information**
━━━━━━━━━━━━━━━
👤 **User ID:** `{user_id}`
📅 **Last Access:** `{last_access}`
💳 **Subscription:** `{subscription}`
⏳ **Expiry:** `{subscription_expiry}`
📌 **Daily Limit:** `{daily_limit}`
📢 **Assigned Channels:** `{', '.join(map(str, assigned_channels)) or 'None'}`
✅ **Joined Channels:** `{', '.join(map(str, joined_channels)) or 'None'}`
━━━━━━━━━━━━━━━
"""

    await message.reply(user_info_text, quote=True)



@Client.on_message(filters.command("approveall") & filters.user(ADMINS))  # Only admins can use it
async def approveall_user(client, message):
    try:
        if len(message.command) < 2:
            return await message.reply_text("❌ **Usage:** `/approveall <channel_id>`")

        target_channel_id = int(message.command[1])
        await message.reply(to_small_caps("Please wait...\nProcessing your request..."))
        # ✅ Get all user IDs correctly
        users = await db.get_all_joins() 
        print(users)
        approved_count = 0
        async for user in users:
            lazyidx = user.get('id')
            if lazyidx:  # ✅ Only approve users with pending requests
                try:
                    await client.approve_chat_join_request(target_channel_id, lazyidx)
                    approved_count += 1
                except:
                    pass
            else:
                print(f"⚠️ Skipped {lazyidx} (No pending request)")

        await message.reply_text(f"✅ Approved ::>> {approved_count} users")

    except Exception as e:
        print(f"⚠️ Error in approveall_user: {e}")
        await message.reply_text("💔 **Failed to approve users. Check logs for details.**")


# @Client.on_message(filters.command("approveall") & filters.user(ADMINS))  # Only admins can use it
# async def approveall_user(client, message):
#     try:
#         if len(message.command) < 2:
#             return await message.reply_text("❌ **Usage:** `/approveall <channel_id>`")
        
#         target_channel_id = int(message.command[1])

#         users = []  # Store user IDs here

#         # ✅ Iterate over the cursor properly (NO `await` on cursor!)
#         async for user in db.users.find({}, {"id": 1}):
#             users.append(user["id"])  # Extract user IDs

#         approved_count = 0
#         failed_count = 0

#         # ✅ Fetch pending join requests
#         pending_requests = await client.get_chat_join_requests(target_channel_id)
#         pending_users = {request.from_user.id for request in pending_requests}  # Store as a set

#         for user_id in users:
#             if user_id in pending_users:  # ✅ Only approve users with pending requests
#                 try:
#                     await client.approve_chat_join_request(target_channel_id, user_id)
#                     approved_count += 1
#                 except Exception as err:
#                     print(f"❌ Failed to approve {user_id}: {err}")
#                     failed_count += 1
#             else:
#                 print(f"⚠️ Skipped {user_id} (No pending request)")

#         await message.reply_text(f"✅ Approved {approved_count} users\n❌ Failed: {failed_count}")

#     except Exception as e:
#         print(f"⚠️ Error in approveall_user: {e}")
#         await message.reply_text("⚠️ **Failed to approve users. Check logs for details.**")


@Client.on_message(filters.command("resetall_subs") & filters.user(ADMINS))
async def reset_all_subscriptions(client, message):
    try:

        await db.users.drop()
        await message.reply("✅ All user subscriptions have been reset to **Free** mode.\n\n")
    
    except Exception as e:
        await message.reply("⚠️ Failed to reset subscriptions. Check logs for errors.")


@Client.on_message(filters.command("reset_trending") & filters.user(ADMINS))
async def reset_trending_searched(client, message):
    try:

        await db.top_search.drop()
        await message.reply("✅ All Top Searches have been reset.")
    
    except Exception as e:
        await message.reply("⚠️ Failed to reset Trending. Check logs for errors.")

@Client.on_message(filters.private & filters.command("add_channel") & filters.user(ADMINS))
async def setup_force_channel(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ Usage: /add_channel <channel_id>")
        return

    channel_id = message.command[1]

    # Try to insert the new channel
    inserted_channel_id = await db.add_new_required_channel(channel_id)

    if inserted_channel_id:
        await message.reply(f"✅ Channel ID: {channel_id} has been successfully added.")
    else:
        await message.reply(f"⚠️ Channel ID: {channel_id} is already in the list.")

@Client.on_message(filters.private & filters.command("remove_channel") & filters.user(ADMINS))
async def remove_force_channel(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ Usage: /remove_channel <channel_id>")
        return

    channel_id = message.command[1]

    removed = await db.remove_required_channel(channel_id)

    if removed:
        await message.reply(f"✅ Channel ID: {channel_id} has been removed successfully.")
    else:
        await message.reply(f"❌ Channel ID: {channel_id} was not found in the list.")


# =====================================================
# @Client.on_message(filters.command("list_channels") & filters.user(ADMINS))
# async def list_required_channels(client, message):
#     try:
#         channels = await db.get_required_channels()  # Fetch all channels

#         if not channels:
#             await message.reply("⚠️ No required channels found.")
#             return

#         keyboard = []
#         for channel_id in channels:
#             try:
#                 chat = await client.get_chat(channel_id)
#                 channel_name = chat.title
#             except:
#                 channel_name = "Unknown"

#             # Create a row with 3 buttons (one channel per row)
#             row = [
#                 InlineKeyboardButton(f"📢 {channel_name}", callback_data=f"info_{channel_id}"),
#                 InlineKeyboardButton(f"{channel_id[3:]}", callback_data=f"info_{channel_id}"),
#                 InlineKeyboardButton("🗑 Remove", callback_data=f"remove_{channel_id}")
#             ]
#             keyboard.append(row)  # Add the row to the keyboard

#         await message.reply(
#             "📌 **Required Channels:**",
#             reply_markup=InlineKeyboardMarkup(keyboard)  # Correct format
#         )
#     except Exception as LazyDeveloper:
#         logging.info(LazyDeveloper)
# ====================================================


async def generate_channel_keyboard(client, page=1):
    channels = await db.get_required_channels()
    
    if not channels:
        return None  
    
    total_pages = ceil(len(channels) / CHANNELS_PER_PAGE)
    page = max(1, min(page, total_pages))  #lazy page bounding
    
    start = (page - 1) * CHANNELS_PER_PAGE
    end = start + CHANNELS_PER_PAGE
    keyboard = []

    for channel_id in channels[start:end]:
        try:
            chat = await client.get_chat(channel_id)
            channel_name = f"{to_small_caps(chat.title)}"
        except:
            channel_name = f"{to_small_caps('❌ADMIN❌')}"
        
        clean_channel_id = str(channel_id).replace("-100", "")  # Remove "-100"
        
        row = [
            InlineKeyboardButton(f"📢 {channel_name}", callback_data=f"info_{channel_id}"),
            InlineKeyboardButton(f"{clean_channel_id}", callback_data=f"info_{channel_id}"),
            InlineKeyboardButton("🗑 Remove", callback_data=f"remove_{channel_id}")
        ]
        keyboard.append(row)

    # Pagination buttons
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(f"{BACK_BTN_TXT}", callback_data=f"page_{page-1}"))
    pagination_buttons.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="pages_info"))
    if page < total_pages:
        pagination_buttons.append(InlineKeyboardButton(f"{NEXT_BTN_TXT}", callback_data=f"page_{page+1}"))

    keyboard.append(pagination_buttons)  # Add pagination row

    return InlineKeyboardMarkup(keyboard)

from random import choice
@Client.on_message(filters.command("sold_channel") & filters.user(ADMINS))
async def sold_channel(bot, message):
    try:
        sold_channel_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        return await message.reply("❌ Invalid command usage!\n\nUse: `sold_channel <channel_id>`", quote=True)

    all_channels = await db.get_required_channels()

    # Fetch all users who have this channel assigned
    users = await db.get_all_users()
    affected_users = [user for user in users if sold_channel_id in user.get("assigned_channels", [])]

    if not affected_users:
        return await message.reply("✅ No users were assigned to this channel.", quote=True)

    for user in affected_users:
        user_id = user["id"]
        assigned_channels = set(user["assigned_channels"])
        assigned_channels.discard(sold_channel_id)  # Remove the sold channel

        # Pick a new random channel from available ones
        available_channels = set(all_channels) - assigned_channels
        if available_channels:
            new_channel = choice(list(available_channels))
            assigned_channels.add(new_channel)

            # Update user data
            await db.update_user({
                "id": user_id,
                "assigned_channels": list(assigned_channels)
            })

    await message.reply(f"✅ The channel `{sold_channel_id}` has been removed & replaced for affected users.", quote=True)


@Client.on_message(filters.command("user_info") & filters.user(ADMINS))
async def user_info(bot, message):
    try:
        user_id = int(message.text.split()[1])  # Extract user ID from command
    except (IndexError, ValueError):
        return await message.reply("❌ Invalid command usage!\n\nUse: `/user_info <user_id>`", quote=True)

    user = await db.get_user(user_id)  # Fetch user data from DB

    if not user:
        return await message.reply(f"❌ No data found for user `{user_id}`.", quote=True)

    # Extract user details
    subscription = user.get("subscription", "free")
    subscription_expiry = user.get("subscription_expiry", "N/A")
    daily_limit = user.get("daily_limit", "N/A")
    last_access = user.get("last_access", "N/A")
    assigned_channels = user.get("assigned_channels", [])
    joined_channels = user.get("joined_channels", [])

    # Format the response
    user_info_text = f"""
**👤 User Information**
━━━━━━━━━━━━━━━
👤 **User ID:** `{user_id}`
📅 **Last Access:** `{last_access}`
💳 **Subscription:** `{subscription}`
⏳ **Expiry:** `{subscription_expiry}`
📌 **Daily Limit:** `{daily_limit}`
📢 **Assigned Channels:** `{', '.join(map(str, assigned_channels)) or 'None'}`
✅ **Joined Channels:** `{', '.join(map(str, joined_channels)) or 'None'}`
━━━━━━━━━━━━━━━
"""

    await message.reply(user_info_text, quote=True)


@Client.on_message(filters.private & filters.command("list_channels") & filters.user(ADMINS))
async def list_required_channels(client, message):
    try:
        keyboard = await generate_channel_keyboard(client, page=1)
        
        if not keyboard:
            await message.reply("⚠️ No required channels found.")
            return
        
        await message.reply("📌 **Required Channels:**", reply_markup=keyboard)
    except Exception as e:
        logging.info(e)


@Client.on_callback_query(filters.regex(r"^(page|remove|info)_(.+)"))
async def callback_handler(client, query):
    action, data = query.data.split("_", 1)

    if action == "page":
        page = int(data)
        keyboard = await generate_channel_keyboard(client, page)
        
        if keyboard:
            await query.message.edit_reply_markup(reply_markup=keyboard)  
    elif action == "info":
        channel_id = data.replace("-100", "")
        await query.answer(f"CHANNEL ID: {channel_id}", show_alert=True)

    elif action == "remove":
        channel_id = data 
        success = await db.remove_required_channel(channel_id)

        if success:
            keyboard = await generate_channel_keyboard(client, page=1)
            if keyboard:
                await query.message.edit_reply_markup(reply_markup=keyboard) 
            else:
                await query.message.edit_text("⚠️ No required channels found.")
            
            await query.answer("✅ Channel removed successfully!", show_alert=True)
        else:
            await query.answer("❌ Failed to remove the channel. Please try again.", show_alert=True)

# ======================================================
@Client.on_message(filters.private & filters.command('channels') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)

@Client.on_message(filters.private & filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.private & filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/LazyDeveloperr/lazyPrincess/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')

@Client.on_message(filters.private & filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )

@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer(f'• With ❤ {temp.B_NAME} ⛱')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')

@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    await save_group_settings(grp_id, 'url_mode', False)
    if settings is not None:
        buttons = [
                [
                    InlineKeyboardButton(
                        'Filter Button',
                        callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                    ),
                    InlineKeyboardButton(
                        'Single' if settings["button"] else 'Double',
                        callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        'Bot PM',
                        callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                    ),
                    InlineKeyboardButton(
                        '✅ Yes' if settings["botpm"] else '❌ No',
                        callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        'File Secure',
                        callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                    ),
                    InlineKeyboardButton(
                        '✅ Yes' if settings["file_secure"] else '❌ No',
                        callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        'IMDB',
                        callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                    ),
                    InlineKeyboardButton(
                        '✅ Yes' if settings["imdb"] else '❌ No',
                        callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        'Spell Check',
                        callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                    ),
                    InlineKeyboardButton(
                        '✅ Yes' if settings["spell_check"] else '❌ No',
                        callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        'Welcome',
                        callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                    ),
                    InlineKeyboardButton(
                        '✅ Yes' if settings["welcome"] else '❌ No',
                        callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                    ),
                ],
            ]
        
        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_text(
            text=f"<b>Change Your Settings for {title} As Your Wish ⚙</b>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.id
        )

@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("Checking template")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("No Input!!")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"Successfully changed template for {title} to\n\n{template}")

@Client.on_message(filters.command("set_tutorial"))
async def settutorial(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"I did'nt recognise you as an admin. Try again ")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("This command works only in group")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>ɢɪᴠᴇ ᴍᴇ ᴀ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.\n\nᴜꜱᴀɢᴇ : /set_tutorial <code>https://t.me/LazyTutorialLink/23</code></b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
        tutorial = message.command[1]
        await save_group_settings(grpid, 'tutorial', tutorial)
        await save_group_settings(grpid, 'is_tutorial', True)
        await reply.edit_text(f"<b>Tutorial added successfully ✔\n\nʏᴏᴜʀ ɢʀᴏᴜᴘ : {title}\n\nʏᴏᴜʀ ᴛᴜᴛᴏʀɪᴀʟ : <code>{tutorial}</code></b>")
    else:
        return await message.reply("<b>ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ɪɴᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ !\nᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ : /set_tutorial <code>https://t.me/LazyTutorialLink/23</code></b>")

@Client.on_message(filters.command("remove_tutorial"))
async def removetutorial(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"I did'nt recognise you as an admin. Please Try Again")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("This command only works in group !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    reply = await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
    await save_group_settings(grpid, 'is_tutorial', False)
    await reply.edit_text(f"<b>Tutorial link removed ✔</b>")


    # Credit @LazyDeveloper.
    # Please Don't remove credit.
    # Born to make history @LazyDeveloper !

    # Thank you LazyDeveloper for helping us in this Journey
    # 🥰  Thank you for giving me credit @LazyDeveloperr  🥰

    # for any error please contact me -> telegram@LazyDeveloperr or insta @LazyDeveloperr 

@Client.on_message(filters.private & filters.command(['view_thumb','view_thumbnail','vt']))
async def viewthumb(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("💔")
    # await add_user_to_database(client, message)
    # if AUTH_CHANNEL:
    #   fsub = await handle_force_subscribe(client, message)
    #   if fsub == 400:
    #     return
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(
	   chat_id=message.chat.id, 
	   photo=thumb,
       caption=f"Current thumbnail for direct renaming",
       reply_markup=InlineKeyboardMarkup([
           [InlineKeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ" , callback_data="deleteThumbnail")]
       ]))
    else:
        await message.reply_text("😔**Sorry ! No thumbnail found...**😔") 

@Client.on_message(filters.private & filters.command(['del_thumb','delete_thumb','dt']))
async def removethumb(client, message):
    print('called')
    if message.from_user.id not in ADMINS:
        return await message.reply_text("💔")
    # await add_user_to_database(client, message)
    # if AUTH_CHANNEL:
    #   fsub = await handle_force_subscribe(client, message)
    #   if fsub == 400:
    #     return
    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("**Okay sweetie, I deleted your custom thumbnail for direct renaming. Now I will apply default thumbnail. ✅️**✅️")

@Client.on_message(filters.private & filters.command(['set_thumbnail','set_thumb','st']))
async def addthumbs(client, message):
    replied = message.reply_to_message
    
    if message.from_user.id not in ADMINS:
        return await message.reply_text("💔")
        
    # await add_user_to_database(client, message)
    
    # if AUTH_CHANNEL:
    #     fsub = await handle_force_subscribe(client, message)
    #     if fsub == 400:
    #         return
        
    LazyDev = await message.reply_text("Please Wait ...")
        # Check if there is a replied message and it is a photo
    if replied and replied.photo:
        # Save the photo file_id as a thumbnail for the user
        await db.set_thumbnail(message.from_user.id, file_id=replied.photo.file_id)
        await LazyDev.edit("**✅ Custom thumbnail set successfully!**")
    else:
        await LazyDev.edit("**❌ Please reply to a photo to set it as a custom thumbnail.**")

async def Gthumb01(bot, update):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await db.get_lazy_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
        Image.open(thumbnail).convert("RGB").save(thumbnail)
        img = Image.open(thumbnail)
        img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None

    return thumbnail

async def Gthumb02(bot, update, duration, download_directory):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await db.get_lazy_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
    else:
        thumbnail = await take_screen_shot(download_directory, os.path.dirname(download_directory), random.randint(0, duration - 1))

    return thumbnail

async def Mdata01(download_directory):
          width = 0
          height = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")
              if metadata.has("height"):
                  height = metadata.get("height")
          return width, height, duration

async def Mdata02(download_directory):
          width = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")

          return width, duration

async def Mdata03(download_directory):

          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds

          return duration
