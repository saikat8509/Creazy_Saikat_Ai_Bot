
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from info import LOG_CHANNEL
from utils import temp, to_small_caps
from urllib.parse import quote

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    try:
        if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply):
            reply_message = message.reply_to_message
            new_name = message.text
            
            if reply_message.text == "»» Please enter new file name...":
                await message.delete()
                media = await client.get_messages(message.chat.id, message.reply_to_message.id)
                file = media.reply_to_message.document or media.reply_to_message.video or media.reply_to_message.audio
                filename = file.file_name
                types = file.mime_type.split("/")
                mime = types[0]
                mg_id = media.reply_to_message.id
                await reply_message.delete()
                try:
                    if not "." in new_name:
                        if "." in media.file_name:
                            extn = media.file_name.rsplit('.', 1)[-1]
                        else:
                            extn = "mkv"
                        new_name = new_name + "." + extn
                    if mime == "video":
                        markup = InlineKeyboardMarkup([[
                            InlineKeyboardButton("📁 Document", callback_data="upload_document"),
                            InlineKeyboardButton("🎥 Video", callback_data="upload_video")]])
                    elif mime == "audio":
                        markup = InlineKeyboardMarkup([[InlineKeyboardButton(
                            "📁 Document", callback_data="doc"), InlineKeyboardButton("🎵 audio", callback_data="upload_audio")]])
                    else:
                        markup = InlineKeyboardMarkup(
                            [[InlineKeyboardButton("📁 Document", callback_data="upload_document")]])
                    # Lazy-WarninG -> Please Dont chnage anything after this Line 
                    await message.reply_text(f"**Select the output file type**\n**🎞New Name** :- ```{out_filename}```", reply_to_message_id=mg_id, reply_markup=markup)

                except:
                    try:
                        out = filename.split(".")
                        out_name = out[-1]
                        out_filename = new_name + "." + out_name
                        # print(f"out name: {out_filename}")
                    except:
                        await message.reply_to_message.delete()
                        await message.reply_text("**Error** :  No  Extension in File, Not Supporting", reply_to_message_id=mg_id)
                        return
                    await message.reply_to_message.delete()
                    if mime == "video":
                        markup = InlineKeyboardMarkup([[InlineKeyboardButton(
                            "📁 Document", callback_data="upload_document"), InlineKeyboardButton("🎥 Video", callback_data="upload_video")]])
                    elif mime == "audio":
                        markup = InlineKeyboardMarkup([[InlineKeyboardButton(
                            "📁 Document", callback_data="upload_document"), InlineKeyboardButton("🎵 audio", callback_data="upload_audio")]])
                    else:
                        markup = InlineKeyboardMarkup(
                            [[InlineKeyboardButton("📁 Document", callback_data="upload_document")]])
                    # Lazy-WarninG -> Please Dont chnage anything after this Line 
                    await message.reply_text(f"**Select the output file type**\n**🎞New Name ->** :- {out_filename}",
                                            reply_to_message_id=mg_id, reply_markup=markup)
            
            elif reply_message.text == "»» Please enter movie name...":
                await reply_message.delete()
                movie_name = new_name
                user_id = message.from_user.id
                generated_link = f"https://google.com/search?q={quote(movie_name)}"
                reply_markup=InlineKeyboardMarkup([
                                        [InlineKeyboardButton(text=f"🤞Request Recieved", callback_data=f"notify_user_req_rcvd:{user_id}:{movie_name}")],
                                        [InlineKeyboardButton(text=f"✅Upload Done", callback_data=f"notify_userupl:{user_id}:{movie_name}")],
                                        [InlineKeyboardButton(text=f"⚡Already Upl..", callback_data=f"notify_user_alrupl:{user_id}:{movie_name}"),InlineKeyboardButton("🖊Spell Error", callback_data=f"notify_user_spelling_error:{user_id}:{movie_name}")],
                                        [InlineKeyboardButton(text=f"😒Not Available", callback_data=f"notify_user_not_avail:{user_id}:{movie_name}")],
                                        [InlineKeyboardButton("❌Reject Req", callback_data=f"notify_user_req_rejected:{user_id}:{movie_name}")],
                                        [InlineKeyboardButton("🌐Check on Google😍", url=generated_link)]
                                        ])
                await client.send_message(LOG_CHANNEL, 
                                       f"#NEW_REQUEST 📑\n\n"
                                       f"📃Content Name: <u><code>{movie_name}</code></u>\n"
                                       f"👨‍🎓USER: {message.from_user.mention if message.from_user.mention else 'N/A'}\n"
                                       f"🆔UserID : {message.from_user.id}\n"
                                       f"📅Date: {message.date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                                       f"#RequestID: {message.id}\n\n"
                                       f"with ❤ <a href=https://t.me/{temp.U_NAME}>{temp.B_NAME}</a>",
                                       reply_markup=reply_markup
                                       )

                # You can send the movie name to the admin or save it to a database, or any other action
                await message.delete()
                await message.reply_text(
                    f"❤ Thank you! You've requested: <b>{movie_name}</b> 🎥\nIt has been sent to the admins.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(f"𓆩ཫ❤𐰌  {to_small_caps('Request More')}  𐰌❤ཀ𓆪", callback_data=f"requestmovie")]
                    ]),
                    parse_mode=ParseMode.HTML
                )
                
    except Exception as e:
        print(f"error: {e}")
