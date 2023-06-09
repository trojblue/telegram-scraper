import configparser
import os
import asyncio
import time
from tqdm.auto import tqdm
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import datetime
from pyrogram import enums

"""
Create a config.ini file, and put these inside:

[pyrogram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
"""


class TelegramUserImageScraper():

    def __init__(self, group_id, user_id, download_dir="downloaded_images"):
        # Read the config.ini file
        self.group_id = group_id
        self.user_id = user_id
        self.download_dir = download_dir

        self.sleep_threshold = 10
        self.app = self._get_app()

    def _get_app(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        api_id = config.get("pyrogram", "api_id")
        api_hash = config.get("pyrogram", "api_hash")
        return Client("my_account", api_id, api_hash, sleep_threshold=self.sleep_threshold)

    async def _download_image(self, message):
        app = self.app
        unique_id = message.photo.file_unique_id
        date_str = message.date.strftime("%Y-%m-%d")
        file_path = os.path.join(self.download_dir,
                                 f"{date_str}_{unique_id}.jpg")  # Assuming all images are jpg for simplicity

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
                    await asyncio.sleep(1)
                else:
                    break

            except FloodWait as e:
                wait_time = e.value
                print(f"FloodWait triggered: Waiting for {wait_time} seconds")
                await asyncio.sleep(wait_time)

    async def _scrape_user(self):
        async with self.app:
            async for message in self.app.search_messages(self.group_id, from_user=self.user_id):
                if message.photo:
                    no_need_wait = await self._download_image(message)
                    if not no_need_wait:
                        time.sleep(1)

    def scrape_user(self):
        self.app.run(self._scrape_user())


from pyrogram.raw.types import InputMessagesFilterPhotos


def do_job():
    # Replace with the user_id of the specific user
    TARGET_GROUP_ID = -1001893538021
    TARGET_USER_ID = 5668980055

    scraper = TelegramUserImageScraper(
        group_id=TARGET_GROUP_ID,
        user_id=TARGET_USER_ID,
    )
    scraper.scrape_user()
    # scraper.scrape(start_date="20230323", end_date="20230408")


if __name__ == '__main__':
    do_job()
