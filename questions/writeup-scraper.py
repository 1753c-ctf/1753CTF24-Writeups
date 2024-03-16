from telethon import TelegramClient, events
import time
import os

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
print(api_id, api_hash)
client = TelegramClient('dumperrr', api_id, api_hash)
client.parse_mode = 'html'


def last_message():
    with open("messages.csv", "r") as f:
        return int(f.readlines()[-1].split("#")[1].split(":")[0])

def append_to_messages(message):
    with open("messages.csv", "a") as f:
        f.write(message + "\n")

async def start():
    print("starting")
    await client.send_message("fah4rah5Ah_bot", '/start')

@client.on(events.NewMessage(from_users='fah4rah5Ah_bot'))
async def handler(event):
    try:
        nextone = int(last_message()+1)
    except:
        nextone = 0
    if "Want do you want to know" in event.raw_text:
        time.sleep(2)
        await event.click(0)
    elif "All I can give you is one tiny bit" in event.raw_text:
        time.sleep(2)
        await event.click(0)
    elif "There are a lot of them" in event.raw_text:
        time.sleep(2)
        print("Selecting part", nextone//100)
        await event.click(nextone//100)
    elif "Right, so from range" in event.raw_text:
        time.sleep(2)
        print("Selecting bit", nextone%100)
        await event.click(nextone%100)
    elif "Flag bit #" in event.raw_text:
        append_to_messages(event.raw_text)
        print(event.raw_text)
        time.sleep(2)
        await client.send_message("fah4rah5Ah_bot", '/start')

if __name__ == '__main__':
    client.start()
    client.loop.run_until_complete(start())
    client.run_until_disconnected()
