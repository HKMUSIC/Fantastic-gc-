from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db_main = client["referral_bot"]
users = db_main["users"]

def get_user(user_id):
    return users.find_one({"_id": user_id})

def create_user(user_id):
    users.insert_one({"_id": user_id, "points": 0, "referrals": []})

def get_points(user_id):
    user = get_user(user_id)
    return user["points"] if user else 0

def update_user(user_id, field, value):
    users.update_one({"_id": user_id}, {"$set": {field: value}})

def add_referral(user_id, referred_id):
    users.update_one({"_id": user_id}, {"$push": {"referrals": referred_id}})

def has_referred(user_id, referred_id):
    user = get_user(user_id)
    return referred_id in user.get("referrals", []) if user else False

def increment_points(user_id, points):
    users.update_one({"_id": user_id}, {"$inc": {"points": points}})
