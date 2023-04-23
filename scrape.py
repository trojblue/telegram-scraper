import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Replace with your own Telegram bot token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Replace with the user_id of the specific user
TARGET_USER_ID = 123456789

# Set the download directory
DOWNLOAD_DIR = "downloaded_images"

def download_image(update: Update, context: CallbackContext):
    if update.message.from_user.id == TARGET_USER_ID:
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            file = context.bot.get_file(file_id)
            file.download(os.path.join(DOWNLOAD_DIR, f"{file_id}.jpg"))

def main():
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add a handler for messages with images
    dispatcher.add_handler(MessageHandler(Filters.photo, download_image))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    main()
