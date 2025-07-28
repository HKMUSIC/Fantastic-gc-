from pyrogram.errors import UserNotParticipant
from database import db

def get_ref_link(user_id):
    return f"https://t.me/Free_Star4Tg_bot?start={user_id}"

async def check_channels(client, user_id, channels):
    for channel in channels:
        try:
            member = await client.get_chat_member(channel, user_id)
            if not member or member.status in ("left", "kicked"):
                return False
        except UserNotParticipant:
            return False
    return True

def update_points(ref_id, referred_id):
    if not db.has_referred(ref_id, referred_id):
        db.increment_points(ref_id, 3)
        db.add_referral(ref_id, referred_id)
