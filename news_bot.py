import re
from telethon import TelegramClient, events

# API ma'lumotlari
API_ID = 28147849  # O'zingizning API_ID ni qo'ying
API_HASH = "d19451239e49bce5f831fa9d2d95d30d"  # O'zingizning API_HASH ni qo'ying
SESSION_NAME = "news_bot"  # Sessiyani saqlash uchun nom

# Kanallar ro'yxati (ID yoki Usernames)
CHANNELS = [
    "https://t.me/fut_test",
    "https://t.me/xayrulla_hamidov",
    "https://t.me/OzbekistonningQizilSherlari",
    "https://t.me/FUTBOLTV",
    "https://t.me/stock_football_tv_stok_futbol",
    "https://t.me/Davron_Fayziev",
    "https://t.me/vamosfarrukh"
]

# Postlarni yuboradigan kanaling ID si
DEST_CHANNEL = "https://t.me/test_futbol_tv"  # O'z kanalingiz username'ini kiriting

# Telethon Client yaratish
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ❗ ORTIQCHA BELGILARNI TOZALASH
def clean_text(text):
    # 1️⃣ Havolalarni o'chirish
    text = re.sub(r"http\S+", "", text)  
    
    # 2️⃣ @username lar va kanallarni olib tashlash
    text = re.sub(r"@\S+", "", text)  
    
    # 3️⃣ Hashtaglarni olib tashlash
    text = re.sub(r"#[\w]+", "", text)  
    
    # 4️⃣ Emoji va ortiqcha belgilarni olib tashlash
    text = re.sub(r"[^\w\s.,!?-]", "", text)  
    
    # 5️⃣ Ortib ketgan bo‘sh joylarni tozalash
    text = re.sub(r"\n+", "\n", text).strip()  
    
    return text

# 📌 POSTNI FORMATGA KELTIRISH
def format_post(text):
    # 1️⃣ Post boshiga sarlavha qo‘shish
    header = "⚽️ Futbol olamida | MUHIM YANGILIK 🔥\n"
    
    # 2️⃣ Post oxiriga hashtaglar qo‘shish
    footer = "\n📢 CHAMPIONS ARENA | Futbol shiddatini birga his qilamiz! 🔥\n\n#ChampionsArena #Saralash #Uzbekiston #Futbol #JCH2026"
    
    return f"{header}{text}{footer}"

# 📨 YANGI POSTNI QABUL QILISH
@client.on(events.NewMessage(chats=CHANNELS))
async def forward_post(event):
    post_text = event.message.text
    if post_text:
        cleaned_text = clean_text(post_text)
        formatted_post = format_post(cleaned_text)
        if formatted_post:
            await client.send_message(DEST_CHANNEL, formatted_post)

# Clientni ishga tushirish
with client:
    print("Bot ishlayapti...")
    client.run_until_disconnected()
