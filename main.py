import os 
from pyrogram 
import Client, filters 
from pyrogram.types 
import InlineKeyboardMarkup, InlineKeyboardButton 
from database 
import db 
from utils 
import check_channels, get_ref_link, update_points

BOT_TOKEN = os.getenv("BOT_TOKEN") 
API_ID = int(os.getenv("API_ID")) 
API_HASH = os.getenv("API_HASH") 
CHANNELS = os.getenv("CHANNELS", "").split() TARGET_POINTS = 50 POINTS_PER_REFERRAL = 3

bot = Client("referral_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start")) async def start(client, message): user = message.from_user ref_id = message.command[1] if len(message.command) > 1 else None user_data = db.get_user(user.id)

if not user_data:
    db.create_user(user.id)
    if ref_id and ref_id != str(user.id):
        update_points(int(ref_id), user.id)

joined = await check_channels(client, user.id, CHANNELS)
if not joined:
    buttons = [
        [InlineKeyboardButton("\ud83d\udce2 Join Channel", url=url)] for url in CHANNELS
    ] + [[InlineKeyboardButton("\u2705 Joined", callback_data="check_join")]]
    await message.reply("\ud83d\udd10 Please join all channels to continue:", reply_markup=InlineKeyboardMarkup(buttons))
    return

ref_link = get_ref_link(user.id)
points = db.get_points(user.id)
await message.reply_text(
    f"\ud83d\udc4b Welcome, {user.first_name}!\n\n"
    f"\ud83c\udfaf Your Points: {points}/{TARGET_POINTS}\n"
    f"\ud83d\udd17 Your Referral Link:\n{ref_link}"
)

@bot.on_callback_query(filters.regex("check_join")) async def recheck_join(client, callback_query): user_id = callback_query.from_user.id joined = await check_channels(client, user_id, CHANNELS) if not joined: await callback_query.answer("\u274c Still not joined all.", show_alert=True) return await callback_query.message.edit_text("\ud83d\udd10 Join all required channels first.")

ref_link = get_ref_link(user_id)
points = db.get_points(user_id)
await callback_query.message.edit_text(
    f"\u2705 Access granted!\n\n\ud83c\udfaf Your Points: {points}/{TARGET_POINTS}\n\ud83d\udd17 Your Referral Link:\n{ref_link}"
)

bot.run()

