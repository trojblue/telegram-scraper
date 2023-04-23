import configparser
import os
import asyncio
import time
from tqdm.auto import tqdm
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import datetime

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

    async def download_image(self, message):
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
                    await asyncio.sleep(30)
                else:
                    break

            except FloodWait as e:
                wait_time = e.value
                print(f"FloodWait triggered: Waiting for {wait_time} seconds")
                await asyncio.sleep(wait_time)

    async def scrape(self, start_date: str, end_date: str):
        """downloads all images sent by a specific user in a group chat, between the start and end dates
        :param group_id: group id
        :param user_id: user id
        :param start_date: start date in the format YYYYMMDD
        :param end_date: end date in the format YYYYMMDD
        """
        start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
        end_date = datetime.datetime.strptime(end_date, "%Y%m%d")

        async with self.app:
            async for message in self.app.get_chat_history(self.group_id, limit=0):
                if message.photo and message.from_user.id == self.user_id:
                    message_date = message.date.replace(tzinfo=None)  # Remove timezone info for comparison

                    if start_date <= message_date <= end_date:
                        no_need_wait = await self.download_image(message)
                        if not no_need_wait:
                            time.sleep(5)


def do_job():

    # Replace with the user_id of the specific user
    TARGET_GROUP_ID = -1001893538021
    TARGET_USER_ID = 5668980055

    scraper = TelegramUserImageScraper(
        group_id=TARGET_GROUP_ID,
        user_id=TARGET_USER_ID,
    )
    scraper.scrape(start_date="20230323", end_date="20230417")


if __name__ == '__main__':
    do_job()
