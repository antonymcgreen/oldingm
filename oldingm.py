from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import socks
import logging
import datetime
from cred import api_id, api_hash, proxy
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

deltaJoin = 20
deltaStop = 5

newLineChats = {}
me = 0

client =  TelegramClient('anon', api_id, api_hash, 
        proxy={'proxy_type':socks.SOCKS5, **proxy})

@client.on(events.NewMessage)
async def my_event_handler(event):
    global me
    global newLineChats
    if me==0:
        me = (await client.get_me()).id

    noCheck = False
    noJoin = False

    if event.chat_id in newLineChats:
        if (datetime.datetime.now() - newLineChats[event.chat_id]).seconds < deltaStop:
            noJoin = True
        else:
            newLineChats.pop(event.chat_id)
    msg = event.message
    if msg.out:
        if msg.message == '/-':
            newLineChats[event.chat_id] = datetime.datetime.now()
            await msg.delete()
            return
        if msg.message == '/+':
            noJoin = False
            noCheck = True
            await msg.delete()
            msg = (await client.get_messages(event.chat_id, from_user = 'me', limit=1))[0]
        prevMsg = (await client.get_messages(event.chat_id, offset_id=msg.id, limit=1))[0]
        if prevMsg.from_id == me and not noJoin:
            if noCheck or (msg.date - prevMsg.date).seconds < deltaJoin:
                success = await prevMsg.edit(text=prevMsg.message+'\n'+msg.message)
                if success:
                    await msg.delete()
client.start()
client.run_until_disconnected()