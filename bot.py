# -*- coding: utf-8 -*-
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# --- خريطة ودالة الزخرفة (Zaghrafa Map and Function) ---

# خريطة الزخرفة (Zaghrafa Mapping)
# هذه الخريطة تحتوي على بعض الأمثلة الشائعة للزخرفة
# يمكن توسيعها لاحقًا لإضافة المزيد من الأنماط
ZAGHRAFA_MAP = {
    'ا': 'آ', 'أ': 'آ', 'إ': 'آ',
    'ب': 'ٻ',
    'ت': 'ٺ',
    'ث': 'ٽ',
    'ج': 'ڃ',
    'ح': 'حـ',
    'خ': 'ځ',
    'د': 'ڍ',
    'ذ': 'ڌ',
    'ر': 'ڒ',
    'ز': 'ڙ',
    'س': 'ڛ',
    'ش': 'ڜ',
    'ص': 'ڝ',
    'ض': 'ڞ',
    'ط': 'طـ',
    'ظ': 'ظـ',
    'ع': 'عـ',
    'غ': 'غـ',
    'ف': 'ڣ',
    'ق': 'ڨ',
    'ك': 'ڪ',
    'ل': 'ڶ',
    'م': 'مـ',
    'ن': 'ڼ',
    'ه': 'هـ',
    'و': 'ۅ',
    'ي': 'ې',
    'ة': 'ة',
    'ى': 'ى',
    'ء': 'ء',
    'آ': 'آ',
    'أ': 'آ',
    'إ': 'آ',
    'ؤ': 'ؤ',
    'ئ': 'ئ',
    ' ': ' 𓏲 ' # زخرفة للمسافة
}

def zaghraf_text(text):
    """
    تقوم بزخرفة النص العربي المدخل باستخدام خريطة الزخرفة.
    """
    decorated_text = ""
    for char in text:
        # تحويل الحرف إلى حرف صغير (للتأكد من مطابقة المفاتيح)
        # على الرغم من أن الأحرف العربية لا تحتوي على حالة، إلا أنها ممارسة جيدة
        char_lower = char.lower()
        
        # البحث عن الحرف في خريطة الزخرفة، وإذا لم يوجد، يتم استخدام الحرف الأصلي
        decorated_char = ZAGHRAFA_MAP.get(char_lower, char)
        
        decorated_text += decorated_char
        
    return decorated_text

# --- كود البوت الرئيسي (Main Bot Code) ---

# تفعيل التسجيل (Logging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# الحصول على توكن البوت من متغيرات البيئة
# يجب على المستخدم تعيين هذا المتغير قبل التشغيل
BOT_TOKEN = "8320082200:AAHB4DMYOmg-vXs8UhSsO-t00qf0jUxAh1Y" # تم دمج التوكن بناءً على طلب المستخدم

# تم دمج التوكن بناءً على طلب المستخدم، لذا لا حاجة للتحقق من متغير البيئة.

async def start(update: Update, context):
    """يرسل رسالة عند الأمر /start."""
    user = update.effective_user
    await update.message.reply_html(
        rf"مرحباً {user.mention_html()}! أنا بوت زخرفة الكلمات العربية. أرسل لي أي نص عربي وسأقوم بزخرفته.",
    )

async def help_command(update: Update, context):
    """يرسل رسالة عند الأمر /help."""
    await update.message.reply_text("أرسل لي النص الذي تريد زخرفته وسأقوم بالباقي. لا توجد أوامر أخرى حاليًا.")

async def handle_text(update: Update, context):
    """يزخرف النص المستلم ويرسله مرة أخرى."""
    text_to_zaghraf = update.message.text
    
    # التأكد من أن النص ليس أمرًا (مثل /start أو /help)
    if text_to_zaghraf.startswith('/'):
        return

    # زخرفة النص
    decorated_text = zaghraf_text(text_to_zaghraf)
    
    # إرسال النص المزخرف
    await update.message.reply_text(decorated_text)

async def error_handler(update: Update, context):
    """يسجل الأخطاء التي تسببها التحديثات."""
    logger.warning("Update '%s' caused error '%s'", update, context.error)
    # يمكن إرسال رسالة خطأ للمستخدم هنا إذا لزم الأمر
    # await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة طلبك.")


def main():
    """يبدأ تشغيل البوت."""
    # التوكن مدمج مباشرة، لا حاجة للتحقق.

    # إنشاء التطبيق وتمرير توكن البوت
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # إضافة معالج للرسائل النصية العادية (غير الأوامر)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # إضافة معالج للأخطاء
    application.add_error_handler(error_handler)

    # بدء البوت
    print("البوت يعمل...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
