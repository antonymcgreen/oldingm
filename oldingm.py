from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import socks
import asyncio
import logging
import datetime
from cred import api_id, api_hash, proxy
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

deltaJoin = 15
deltaStop = 5

client = TelegramClient('anon', api_id, api_hash)
# client = TelegramClient('anon', api_id, api_hash, proxy={'proxy_type':socks.SOCKS5, **proxy})

@client.on(events.NewMessage)
async def my_event_handler(event):
    try:
        client.newLineChats
    except AttributeError:
        client.meId = (await client.get_me()).id
        client.newLineChats={}

    noCheck = False
    noJoin = False

    if event.chat_id in client.newLineChats:
        if (datetime.datetime.now() - client.newLineChats[event.chat_id]).seconds < deltaStop:
            noJoin = True
        else:
            client.newLineChats.pop(event.chat_id)
    msg = event.message
    if msg.out:
        if msg.message == '/-':
            client.newLineChats[event.chat_id] = datetime.datetime.now()
            await msg.delete()
            return
        if msg.message == '/+':
            noJoin = False
            noCheck = True
            await msg.delete()
            msg = (await client.get_messages(event.chat_id, from_user = 'me', limit=1))[0]
        prevMsg = (await client.get_messages(event.chat_id, offset_id=msg.id, limit=1))[0]
        if prevMsg.from_id == client.meId and not noJoin:
            if noCheck or (msg.date - prevMsg.date).seconds < deltaJoin:
                success = await prevMsg.edit(text=prevMsg.message+'\n'+msg.message)
                if success:
                    await msg.delete()

client.start()
client.run_until_disconnected()