# bot/handlers/start.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the official welcome message matching the UME Kratie layout."""
    
    # Text from the image: "✨ សូមស្វាគមន៍មកកាន់ សាកលវិទ្យាល័យ UME សាខាខេត្តក្រចេះ"
    welcome_text = "✨ សូមស្វាគមន៍មកកាន់ សាកលវិទ្យាល័យ UME សាខាខេត្តក្រចេះ"
    
    # 6 explicit vertical buttons mapping to the image layout
    keyboard = [
        [InlineKeyboardButton("អំពីសាកលវិទ្យាល័យ", callback_data="about_uni")],
        [InlineKeyboardButton("🎓🧑‍🎓 ព័ត៌មានសិក្សា 🧑‍🎓🎓", callback_data="academic_info")],
        [InlineKeyboardButton("✍️🎓 ការចុះឈ្មោះចូលរៀន ✍️🎓", callback_data="registration")],
        [InlineKeyboardButton("✍️💧 បង់ថ្លៃសិក្សា ✍️🚰", callback_data="tuition_payment")],
        [InlineKeyboardButton("ទំនាក់ទំនង 📞", callback_data="contact_us")],
        [InlineKeyboardButton("📍 ទីតាំងសាកលវិទ្យាល័យ", callback_data="location")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=welcome_text, 
        reply_markup=reply_markup
    )