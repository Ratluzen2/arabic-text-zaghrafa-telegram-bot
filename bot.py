# -*- coding: utf-8 -*-
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from zaghrafa import zaghraf_text

# تفعيل التسجيل (Logging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# الحصول على توكن البوت من متغيرات البيئة
# يجب على المستخدم تعيين هذا المتغير قبل التشغيل
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN environment variable not set.")
    # يمكن إيقاف التطبيق هنا أو استخدام قيمة وهمية للاختبار المحلي
    # لكن للتشغيل الفعلي، يجب أن يكون التوكن موجودًا.

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
    if not BOT_TOKEN:
        print("خطأ: لم يتم تعيين متغير البيئة TELEGRAM_BOT_TOKEN. يرجى تعيينه قبل التشغيل.")
        return

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
