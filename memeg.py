import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from config import *

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = API_ID
api_hash = API_HASH
bot_token = BOT_TOKEN
kntl = TelegramClient('dareen', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []


@kntl.on(events.NewMessage(pattern="^/start$"))
async def help(event):
  helptext = "**Halo 👋🏻!\n\nKenalin Nih, Gua Bot Tag All Yang Di Rancang Sama @Darenrorr Dengan Berbasis Python.\n\nGua Siap Membantu Lu Dengan Mention Semua Anggota Di Group Anda**"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('Developer', 't.me/darenrorr'),
      ],
      [
        Button.url('Support', 't.me/Darensupport'),
        Button.url('Channel', 't.me/cehadaren'),
      ],
    )
  )
  
@kntl.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("**Jangan Privat Tolol**!")
  
  is_admin = False
  try:
    partici_ = await kntl(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("**Lu Bukan Admin Ngentod Ngapain Mau Tag All**")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("**Minimal Kasih Text/Pesan Lah Kontol!**")
  elif event.pattern_match.group(1):
    mode = "teks_on_tempel"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "teks_on_balas"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("**Si Tolol Di Suruh Kasih Text/Pesan Batu Bet Kalo Di Bilangin**")
  else:
    return await event.respond("**Si Tolol Di Suruh Kasih Text/Pesan Batu Bet Kalo Di Bilangin**")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in kntl.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"🀄︎ [{usr.first_name}](tg://user?id={usr.id})\n"
    if usrnum == 5:
      if mode == "teks_on_tempel":
        txt = f"{msg}\n\n{usrtxt}"
        await kntl.send_message(chat_id, txt)
      elif mode == "teks_on_balas":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@kntl.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('**Lu Ngapain? Dasar Idiot, Orang Ga Ada Tagall**')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('**Iya Bang Gua Stopin**')



print("BOT AKTIF")
kntl.run_until_disconnected()
