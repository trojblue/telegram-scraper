import os
from pyrogram import Client, filters

# Replace with the user_id of the specific user
TARGET_USER_ID = 123456789

# Set the download directory
DOWNLOAD_DIR = "downloaded_images"

app = Client("my_account", config_file="config.ini")

@app.on_message(filters.chat("YOUR_GROUP_NAME") & filters.user(TARGET_USER_ID) & filters.photo)
async def download_image(_, message):
    file_id = message.photo.file_id
    await message.download(os.path.join(DOWNLOAD_DIR, f"{file_id}.jpg"))

app.run()
