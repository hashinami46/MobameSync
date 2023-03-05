# -*- coding: utf-8 -*-

# Importing Section
import sys
sys.path.append('../')
from database.config import *
import main

# GLOBAL CONFIG SECTION
apihelper.SESSION_TIME_TO_LIVE = 5 * 60
mobamebot = telebot.TeleBot(teletoken())
syncstate = False

# SOME FUNCTIONS SECTION
def message_sender_and_recorder(grup, servermsgdb, localmsgdb):
  with open(localmsgdb, 'r+') as localmessage:
    config = configfile()
    membersdb = config['Sakamichi_App'][grup]['telegram_services']['members']
    localmsgid = json.load(localmessage)
    for servermessage in servermsgdb:
      for memberdb in membersdb:
        if servermessage['state'] == 'published':
          if servermessage['id'] not in localmsgid and servermessage['type'] == 'text' and servermessage['group_id'] == memberdb['id']:
            mobamebot.send_message(chat_id=telechatid(), text=f"{servermessage['text'].replace('%%%',prefix).replace('％％％',prefix)}\n\n#{memberdb['name'].replace(' ','')}", disable_web_page_preview=True)
            localmsgid.append(servermessage['id'])
          if servermessage['id'] not in localmsgid and servermessage['type'] == 'picture' and 'text' in servermessage and servermessage['group_id'] == memberdb['id']:
            mobamebot.send_photo(chat_id=telechatid(), photo=servermessage['file'], caption=f"{servermessage['text'].replace('%%%',prefix).replace('％％％',prefix)}\n\n#{memberdb['name'].replace(' ','')}")
            localmsgid.append(servermessage['id'])
          if servermessage['id'] not in localmsgid and servermessage['type'] == 'picture' and 'text' not in servermessage and servermessage['group_id'] == memberdb['id']:
            mobamebot.send_photo(chat_id=telechatid(), photo=servermessage['file'], caption=f"#{memberdb['name'].replace(' ','')}")
            localmsgid.append(servermessage['id'])
          if servermessage['id'] not in localmsgid and servermessage['type'] == 'voice' and servermessage['group_id'] == memberdb['id']:
            mobamebot.send_audio(chat_id=telechatid(), audio=servermessage['file'], caption=f"#{memberdb['name'].replace(' ','')}")
            localmsgid.append(servermessage['id'])
          if servermessage['id'] not in localmsgid and servermessage['type'] == 'video' and servermessage['group_id'] == memberdb['id']:
            requestvideo = httpx.get(url=servermessage['file'])
            if int(requestvideo.headers['content-length']) <= 18000000:
              mobamebot.send_video(chat_id=telechatid(), video=servermessage['file'], caption=f"#{memberdb['name'].replace(' ','')}")
              localmsgid.append(servermessage['id'])
            else:
              videopath = f"{ROOT_DIR}{tempdir}/{os.path.basename(video.url.path)}"
              with open(videopath, 'wb') as tempvid:
                tempvid.write(requestvideo.content)
              time.sleep(5)
              mobamebot.send_video(chat_id=telechatid(), video=open(videopath,'rb'), caption=f"#{memberdb['name'].replace(' ','')}")
              localmsgid.append(servermessage['id'])
              os.remove(videopath)
    localmessage.seek(0)
    json.dump(localmsgid, localmessage, indent=2)
    localmessage.truncate()
def syncer():
  nogi = []
  nogi.clear()
  grouplister('nogizaka46',nogi)
  if nogi:
    main.Nogizaka.stream_timelines(nogi)
    message_sender_and_recorder('nogizaka46',main.nogitodaymessages, nogilocalmsg)
  saku = []
  saku.clear()
  grouplister('sakurazaka46',saku)
  if saku:
    main.Sakurazaka.stream_timelines(saku)
    message_sender_and_recorder('sakurazaka46',main.sakutodaymessages, sakulocalmsg)
  hina = []
  hina.clear()
  grouplister('hinatazaka46',hina)
  if hina:
    main.Hinatazaka.stream_timelines(hina)
    message_sender_and_recorder('hinatazaka46',main.hinatodaymessages, hinalocalmsg)

# BUTTON CONFIG SECTION
updatedb      = Button(button_data={"Update Database":"updatedb"}).button
togglegroup   = Button(button_data={"Group Toggle":"grouptoggleservice"}).button
togglemember  = Button(button_data={"Member Toggle":"membertoggleservice"}).button
backtoconfig  = Button(button_data={"Kembali":"backtoconfig"}).button
cancel        = Button(button_data={"Batal":"cancel"}).button

# KEYBOARD CREATOR
def configkeyboard():
  togglekey = Keyboa(items=list([togglegroup,togglemember]), items_in_row=2).keyboard
  updatedbkey = Keyboa(items=[updatedb]).keyboard
  keyboard = Keyboa.combine(keyboards=(togglekey, updatedbkey, Keyboa(items=[cancel]).keyboard))
  return keyboard
def grouptogglepagekeyboardgenerator():
  grouplists = []
  grouplists.clear()
  with open(configdir, 'r') as configfile:
    config = json.load(configfile)
    for group in ['nogizaka46','sakurazaka46','hinatazaka46']:
      isservice = config['Sakamichi_App'][group]['telegram_services']['services']
      kanjiname = config['Sakamichi_App'][group]['telegram_services']['kanjiname']
      grouplists.append({
        "text": f"✓ {kanjiname}" if isservice else kanjiname,
        "callback_data": f"{kanjiname}toggle"
      })
  grouplistkey = Keyboa(items=list(grouplists),items_in_row=3).keyboard
  navkey       = Keyboa(items=list([backtoconfig,cancel]),items_in_row=2).keyboard
  keyboard     = Keyboa.combine(keyboards=(grouplistkey,navkey))
  return keyboard
def membertogglepagekeyboardgenerator():
  grouplists = []
  grouplists.clear()
  with open(configdir) as configfile:
    config = json.load(configfile)
    for group in ['nogizaka46','sakurazaka46','hinatazaka46']:
      isservice = config['Sakamichi_App'][group]['telegram_services']['services']
      kanjiname = config['Sakamichi_App'][group]['telegram_services']['kanjiname']
      if isservice:
        grouplists.append({
          "text": f"{kanjiname}",
          "callback_data":f"{kanjiname}enter"
          })
  grouplistkey = Keyboa(items=list(grouplists),items_in_row=3).keyboard
  navkey       = Keyboa(items=list([backtoconfig,cancel]),items_in_row=2).keyboard
  keyboard     = Keyboa.combine(keyboards=(grouplistkey,navkey))
  return keyboard
def membertogglepage2keyboardgenerator(group):
  memberlists = []
  memberlists.clear()
  with open(configdir) as configfile:
    config = json.load(configfile)
    for member in config['Sakamichi_App'][group]['telegram_services']['members']:
      memberid  = member['id']
      kanjiname = member['name'].replace(' ','')
      isservice = member['service']
      memberlists.append({
        "text": f"✓ {kanjiname}" if isservice else kanjiname,
        "callback_data": f"{group}-{memberid}"
      })
  memberlistkey = Keyboa(items=list(memberlists),items_in_row=3).keyboard
  navkey        = Keyboa(items=list([{"text":"Kembali","callback_data":"membertoggleservice"},cancel]),items_in_row=2).keyboard
  keyboard      = Keyboa.combine(keyboards=(memberlistkey, navkey))
  return keyboard

# MESSAGE HANDLER SECTION
@mobamebot.message_handler(commands=["start"])
def bot_start(message):
  if message.chat.type == 'private':
    mobamebot.send_message(message.chat.id, text=replystart.replace('%user%', str(message.from_user.username)), parse_mode='MarkdownV2')
  else:
    mobamebot.reply_to(message, text=replystart.replace(' %user%', ''), parse_mode='MarkdownV2')
  telemessagelogger(message)

@mobamebot.message_handler(commands=["tentang"])
def bot_about(message):
  if message.chat.type == 'private':
    mobamebot.send_message(message.chat.id, text=aboutmessage, parse_mode='MarkdownV2',disable_web_page_preview=True)
  else:
    mobamebot.reply_to(message, text=aboutmessage, parse_mode='MarkdownV2')
  telemessagelogger(message)

@mobamebot.message_handler(commands=["konfigurasi"])
def bot_config(message):
  if message.chat.id == ownerid:
    mobamebot.send_message(message.chat.id, text=configmessages, parse_mode="MarkdownV2", reply_markup=configkeyboard())
  else:
    msg = mobamebot.send_message(message.chat.id, text=preventintruders, parse_mode="MarkdownV2")
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    report = mobamebot.send_message(ownerid, text=report_message(message), parse_mode="MarkdownV2")
  telemessagelogger(message)

@mobamebot.message_handler(commands=["startsync"])
def startsynchronize(message):
  if message.chat.id == ownerid:
    global syncstate
    syncstate = True
    msg = mobamebot.send_message(message.chat.id, text=syncstarted)
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    logging.info(f"✨ Sinkronisasi dimulai pada {WIB.strftime('%Y-%m-%d %H:%M:%S')} WIB")
    while syncstate:
      syncer()
      time.sleep(0)
    else:
      pass
  else:
    msg = mobamebot.send_message(message.chat.id, text=preventintruders, parse_mode="MarkdownV2")
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    report = mobamebot.send_message(ownerid, text=report_message(message), parse_mode="MarkdownV2")
  telemessagelogger(message)

@mobamebot.message_handler(commands=["stopsync"])
def stopsynchronize(message):
  if message.chat.id == ownerid:
    global syncstate
    syncstate = False
    logging.info(f"Sinkronisasi dihentikan pada {WIB.strftime('%Y-%m-%d %H:%M:%S')} WIB")
    msg = mobamebot.send_message(message.chat.id, text=syncstopped)
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
  else:
    msg = mobamebot.send_message(message.chat.id, text=preventintruders, parse_mode="MarkdownV2")
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    report = mobamebot.send_message(ownerid, text=report_message(message), parse_mode="MarkdownV2")
  telemessagelogger(message)

@mobamebot.message_handler(commands=['updatetoken'])
def update_token_func(message):
  if message.chat.id == ownerid:
    textsplit = message.text.split()
    if syncstate:
        msg = mobamebot.send_message(chat_id=message.chat.id, text="Harap mematikan sinkronisasi terlebih dahulu!")
        time.sleep(3)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    if len(textsplit) == 3:
      grupname = textsplit[1]
      reftoken = textsplit[2]
      if grupname in sakamichigroups \
      and not syncstate\
      and len(reftoken.split('-')) == 5 \
      and len(reftoken.split('-')[0]) == 8 \
      and len(reftoken.split('-')[1]) == 4 \
      and len(reftoken.split('-')[2]) == 4 \
      and len(reftoken.split('-')[3]) == 4 \
      and len(reftoken.split('-')[4]) == 12:
        update_refresh_token(grupname, reftoken)
        msg = mobamebot.send_message(message.chat.id, text=refreshtokenupdated.replace('%grup%', grupname))
        time.sleep(3)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
      if grupname not in sakamichigroups:
        msg = mobamebot.send_message(chat_id=message.chat.id, text="Format nama grup yang anda masukkan salah!")
        time.sleep(3)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
      if len(reftoken.split('-')) != 5:
        msg = mobamebot.send_message(chat_id=message.chat.id, text="Format refresh token anda salah!")
        time.sleep(3)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    if len(textsplit) != 3\
    and not syncstate:
        msg = mobamebot.send_message(chat_id=message.chat.id, text="Format command salah!")
        time.sleep(3)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
        mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
  else:
    msg = mobamebot.send_message(message.chat.id, text=preventintruders, parse_mode="MarkdownV2")
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    report = mobamebot.send_message(ownerid, text=report_message(message), parse_mode="MarkdownV2")
  telemessagelogger(message)

@mobamebot.message_handler(commands=['subsinfo'])
def get_sub_info(message):
  if message.chat.id in [ownerid, telechatid()]:
    textsplit = message.text.split()
    if len(textsplit) == 2\
    and textsplit[1] in sakamichigroups:
      mobamebot.send_message(message.chat.id, text=f"`{get_subsinfo(textsplit[1])}`", parse_mode="MarkdownV2")
    if len(textsplit) != 2\
    or textsplit[1] not in sakamichigroups:
      msg = mobamebot.send_message(message.chat.id,text=incorrectsubsinfo)
      time.sleep(5)
      mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
      mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
  elif message.chat.id not in [ownerid, telechatid()]:
    msg = mobamebot.send_message(message.chat.id, text=preventintruders, parse_mode="MarkdownV2")
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    report = mobamebot.send_message(ownerid, text=report_message(message), parse_mode="MarkdownV2")
  telemessagelogger(message)
  
@mobamebot.message_handler(commands=['sendpastmessage'])
def send_pastmessages(message):
  if message.chat.id == ownerid:
    textsplit = message.text.split()
    if len(textsplit) == 3:
      config = configfile()
      if textsplit[1] == 'nogizaka46'\
      and textsplit[2] in [member['name'].replace(' ','') for member in config['Sakamichi_App'][textsplit[1]]['telegram_services']['members']]:
        main.Nogizaka.past_messages_streamer([textsplit[2]])
        message_sender_and_recorder(textsplit[1],main.nogipastmessages, nogilocalmsg)
      if textsplit[1] == 'sakurazaka46'\
      and textsplit[2] in [member['name'].replace(' ','') for member in config['Sakamichi_App'][textsplit[1]]['telegram_services']['members']]:
        main.Sakurazaka.past_messages_streamer([textsplit[2]])
        message_sender_and_recorder(textsplit[1],main.sakupastmessages, sakulocalmsg)
      if textsplit[1] == 'hinatazaka46'\
      and textsplit[2] in [member['name'].replace(' ','') for member in config['Sakamichi_App'][textsplit[1]]['telegram_services']['members']]:
        main.Hinatazaka.past_messages_streamer([textsplit[2]])
        message_sender_and_recorder(textsplit[1],main.hinapastmessages, hinalocalmsg)
      if textsplit[1] in sakamichigroups:
        msg = mobamebot.send_message(message.chat.id, text="Perintah diproses!")
        time.sleep(3)
        mobamebot.delete_message(msg.chat.id, msg.message_id)
      if textsplit[1] not in sakamichigroups\
      or textsplit[2] not in [member['name'].replace(' ','') for member in config['Sakamichi_App'][textsplit[1]]['telegram_services']['members']]\
      or syncstate:
        msg = mobamebot.send_message(message.chat.id, text="Maaf, nama grup yang anda masukkan salah! atau nama member yang anda masukkan tidak tersedia! Jangan lupa untuk mematikan sinkronisasi terlebih dahulu!")
        time.sleep(3)
        mobamebot.delete_message(msg.chat.id, msg.message_id)
        mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    if len(textsplit) != 3:
      msg = mobamebot.send_message(message.chat.id,text=incorrectsendpast)
      time.sleep(5)
      mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
      mobamebot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
  else:
    msg = mobamebot.send_message(message.chat.id, text=preventintruders, parse_mode="MarkdownV2")
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    report = mobamebot.send_message(ownerid, text=report_message(message), parse_mode="MarkdownV2")
  telemessagelogger(message)
@mobamebot.message_handler(commands=['ceksyncstate'])
def check_syncstate(message):
  if message.chat.id == ownerid:
    msg = mobamebot.send_message(message.chat.id, text=f"{'Sinkronisasi berjalan!' if syncstate else 'Sinkronisasi berhenti!'}")
    time.sleep(5)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
  else:
    msg = mobamebot.send_message(message.chat.id, text=preventintruders, parse_mode="MarkdownV2")
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    report = mobamebot.send_message(ownerid, text=report_message(message), parse_mode="MarkdownV2")
  telemessagelogger(message)
@mobamebot.message_handler(commands=['sendlog'])
def send_today_log(message):
  if message.chat.id == ownerid:
    msg = mobamebot.send_document(message.chat.id, document=open(f"{ROOT_DIR}{logdir}/{datetime.datetime.now().strftime('%Y-%m-%d')}.log", "rb"))
  else:
    msg = mobamebot.send_message(message.chat.id, text=preventintruders, parse_mode="MarkdownV2")
    time.sleep(3)
    mobamebot.delete_message(msg.chat.id, msg.message_id)
    mobamebot.delete_message(msg.chat.id, msg.message_id - 1)
    report = mobamebot.send_message(ownerid, text=report_message(message), parse_mode="MarkdownV2")
  telemessagelogger(message)
  
# CALLBACK HANDLER SECTION
@mobamebot.callback_query_handler(func=lambda message: True)
def callback_option(call):
  if call.data == 'cancel':
    msg = mobamebot.delete_message(call.message.chat.id, call.message.message_id -1)
    mobamebot.delete_message(call.message.chat.id, call.message.message_id)
  if call.data == 'backtoconfig':
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=configmessages, parse_mode="MarkdownV2", reply_markup=configkeyboard())
  if call.data == 'updatedb':
    main.Nogizaka.teleservice_updater()
    main.Sakurazaka.teleservice_updater()
    main.Hinatazaka.teleservice_updater()
    mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Database Telah Diupdate\!', parse_mode="MarkdownV2")
    time.sleep(2)
    mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=configmessages, parse_mode="MarkdownV2", reply_markup=configkeyboard())
  if call.data == 'grouptoggleservice':
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=grouptogglepagekeyboardgenerator())
  elif call.data == 'membertoggleservice':
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=membertogglepagekeyboardgenerator())
  if call.data == '乃木坂46toggle':
    telegroupservicetoggler('nogizaka46')
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=grouptogglepagekeyboardgenerator())
  elif call.data == '櫻坂46toggle':
    telegroupservicetoggler('sakurazaka46')
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=grouptogglepagekeyboardgenerator())
  elif call.data == '日向坂46toggle':
    telegroupservicetoggler('hinatazaka46')
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=grouptogglepagekeyboardgenerator())
  if call.data == '乃木坂46enter':
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=membertogglepage2keyboardgenerator('nogizaka46'))
  elif call.data == '櫻坂46enter':
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=membertogglepage2keyboardgenerator('sakurazaka46'))
  elif call.data == '日向坂46enter':
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=membertogglepage2keyboardgenerator('hinatazaka46'))
  if "nogizaka46-" in call.data:
    telememberservicetoggler(call.data, 'nogizaka46')
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=membertogglepage2keyboardgenerator('nogizaka46'))
  elif "sakurazaka46-" in call.data:
    telememberservicetoggler(call.data, 'sakurazaka46')
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=membertogglepage2keyboardgenerator('sakurazaka46'))
  elif "hinatazaka46-" in call.data:
    telememberservicetoggler(call.data, 'hinatazaka46')
    msg = mobamebot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{selectgm}", parse_mode="MarkdownV2", reply_markup=membertogglepage2keyboardgenerator('hinatazaka46'))
  
  telecalllogger(call)

if __name__ == "__main__":
  logging.info(f"✨ Bot started at {WIB}")
  mobamebot.infinity_polling(timeout=10, long_polling_timeout=5)
  
# AVAILABLE COMMAND
# start - Mulai Bot
# subsinfo - Informasi layanan Aktif
# tentang - Mengenai Bot dan Developer
# konfigurasi - (Khusus Owner) Aktifkan atau matikan layanan
# ceksyncstate - (Khusus Owner) Cek status sinkronisasi
# startsync - (Khusus Owner) Mulai sinkronisasi pesan
# stopsync - (Khusus Owner) Hentikan sinkronisasi pesan 
# updatetoken - (Khusus Owner) Update refresh token
# sendpastmessage - (Khusus Owner) Bagikan pesan member yang baru disubscribe 
# sendlog - (Khusus Owner) download file .log
