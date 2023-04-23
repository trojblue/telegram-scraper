import asyncio
import configparser
from pyrogram import Client

# Read the config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

api_id = config.get("pyrogram", "api_id")
api_hash = config.get("pyrogram", "api_hash")


# CHANGE ME
TARGET_USER_FIRST_NAME = ""

async def main():
    async with Client("my_account", api_id, api_hash) as app:
        groups = [dialog.chat async for dialog in app.get_dialogs() ]

        for gr in groups:
            print("gr.title: ", gr.title, "gr.id: ", gr.id)

        # get members; uncomment above then change the id in get_chat_members to your desired one
        members = [dialog async for dialog in app.get_chat_members(-1001893538021) ]

        for m in members:
            user = m.user
            first_name = user.first_name
            if TARGET_USER_FIRST_NAME in first_name:
                print(f"ID: {user.id}, Username: {user.username}, Name: {first_name}")


if __name__ == '__main__':
    asyncio.run(main())
