import configparser
import os
import asyncio
import time
from tqdm.auto import tqdm
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram import errors

"""
Create a config.ini file, and put these inside:

[pyrogram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
"""

# Read the config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

api_id = config.get("pyrogram", "api_id")
api_hash = config.get("pyrogram", "api_hash")

# Replace with the user_id of the specific user
TARGET_USER_ID = 5668980055
TARGET_GROUP_ID = -1001893538021

# Set the download directory
DOWNLOAD_DIR = "downloaded_images/"

app = Client("my_account", api_id, api_hash, sleep_threshold=10)


async def download_image(message):
    unique_id = message.photo.file_unique_id
    date_str = message.date.strftime("%Y-%m-%d")
    file_path = os.path.join(DOWNLOAD_DIR, f"{date_str}_{unique_id}.jpg")  # Assuming all images are jpg for simplicity

    # Check if the file exists and is not 0kb
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        print(f"File {file_path} already exists. Skipping download.")
        return True

    async def progress(current, total):
        pbar.update(current - pbar.n)  # Update progress bar

    while True:
        try:
            with tqdm(total=message.photo.file_size, desc=f"Downloading {unique_id}", unit="B",
                      unit_scale=True) as pbar:
                await app.download_media(message, file_name=file_path, progress=progress)


            # Check if the downloaded file is empty
            if os.path.getsize(file_path) == 0:
                print(f"Downloaded file {unique_id} is empty. Waiting for 30 seconds.")
                await asyncio.sleep(30)
            else:
                break

        except FloodWait as e:
            wait_time = e.value
            print(f"FloodWait triggered: Waiting for {wait_time} seconds")
            await asyncio.sleep(wait_time)


import datetime


async def main(start_date_str, end_date_str):
    start_date = datetime.datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y%m%d")

    async with app:
        async for message in app.get_chat_history(TARGET_GROUP_ID, limit=0):
            if message.photo and message.from_user.id == TARGET_USER_ID:
                message_date = message.date.replace(tzinfo=None)  # Remove timezone info for comparison

                if start_date <= message_date <= end_date:
                    no_need_wait =  await download_image(message)
                    if not no_need_wait:
                        time.sleep(5)


if __name__ == '__main__':
    app.run(main("20230323", "20230425"))
