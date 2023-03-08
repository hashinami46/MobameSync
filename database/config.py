# -*- coding: utf-8 -*-

# Importing Section 1
import os
import sys
import json
import time
import datetime
import logging
import asyncio
import httpx
import telebot
import tabulate
import shutil

# Importing Section 
from pathlib import Path
from pytz import timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from logging.handlers import TimedRotatingFileHandler
from telebot import apihelper
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import custom_filters, types
from keyboa import Keyboa
from keyboa import Button
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

# LOADING BAR CONFIG
PBAR = Progress(
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    BarColumn(),
    MofNCompleteColumn(),
    TextColumn("•"),
    TimeElapsedColumn(),
    TextColumn("•"),
    TimeRemainingColumn(),
)

ROOT_DIR = Path(__file__).parent.parent
scrwidth, _ = shutil.get_terminal_size()

# DATABASE CONFIG
configdir   = f"{ROOT_DIR}/database/config.json"
def configfile(configname=configdir):
  with open(configname, 'r+') as configfile:
    config = json.load(configfile)
  return config
config = configfile()

# PATH CONFIG
apidir       = config['Path']['api']
databasebdir = config['Path']['database']
logdir       = config['Path']['log']
downloaddir  = config['Path']['download']
telegramdir  = config['Path']['telegram']
tempdir      = config['Path']['temp']
nogilocalmsg = f"{ROOT_DIR}/database/messagelocalnogi.json"
sakulocalmsg = f"{ROOT_DIR}/database/messagelocalsaku.json"
hinalocalmsg = f"{ROOT_DIR}/database/messagelocalhina.json"

# SUBSPATH CONFIH
groupsdir      = config['SubsPath']['groups']
membersdir     = config['SubsPath']['members']
thumbnaildir   = config['SubsPath']['thumbnail']
phone_imagedir = config['SubsPath']['phone_image']
nogidir        = config['SubsPath']['nogizaka46']
sakudir        = config['SubsPath']['sakurazaka46']
hinadir        = config['SubsPath']['hinatazaka46']

# Logging Section
logging.basicConfig(
  level    = logging.INFO,
  format   = "%(asctime)s - %(levelname)s - %(message)s",
  handlers = [
        logging.handlers.TimedRotatingFileHandler(
          filename    = f"{ROOT_DIR}{logdir}/logging.log",
          when        = 'midnight',
          backupCount = 30,
          encoding    = None,
          delay       = 0,
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

# KEY-VALUE CONFIG
nullvalue = ("", [], None, 0, False)

# GROUPS LIST CONFIG
sakamichigroups = ['nogizaka46', 'sakurazaka46', 'hinatazaka46']
groups          = config['Databases']['groups']
members         = config['Databases']['members']
thumbnail       = config['Databases']['thumbnail']
phone_image     = config['Databases']['phone_image']

# TIMEZONE CONFIG
NOW = datetime.datetime.now()
UTC = datetime.datetime.now(timezone('UTC'))
WIB = UTC.astimezone(timezone(config['Timezone']['TZ']))
YST = WIB - datetime.timedelta(days=1)

# LOGGING PHRASE CONFIG
refreshtokenundefined  = 'Maaf, harap memasukkan refresh token %%% terlebih dahulu'
refreshtokendenied     = 'Maaf, sepertinya refresh token %%% yang anda masukkan salah'
refreshtokenupdated    = 'Refresh token %grup% berhasil diupdate!'
accesstokenundefined   = 'Maaf, akses token %%% kosong, harap update akses token terlebih dahulu!'
accesstokenupdated     = 'Berhasil mengupdate akses token %%%'
accesstokenadded       = 'Menambahkan akses token %%% ke headers...'
accesstokenvalid       = 'Akses token %%% valid!'
accesstokenexpired     = 'Ups, sepertinya akses token %%% salah atau sudah tidak berlaku'
gmlistundefined        = 'Database list %%%0 %%% kosong, harap update terlebih dahulu!'
pleaseupdategmlist     = 'Harap mengupdate list %%%0 %%% terlebih dahulu!'
gmlistdbupdated        = 'Berhasil mengupdate list %%%0 %%%'
downloadsuccess        = 'File %%% berhasil diunduh di direktori %dir%'
downloadsuccessv2      = 'File %file% berhasil diunduh!'
alreadydownloaded      = 'File %%% telah diunduh!'
foldercreated          = 'Folder %%% berhasil dibuat!'
subscriptionupdated    = 'Daftar member %%% yang disubscribe berhasil diupdate!'
teleserviceupdated     = 'Database service telegram %group% diupdate'
wrongmembername        = 'Ups, sepertinya nama member yang anda masukkan di bawah ini salah!'

# BASIC FUNCTION CONFIG
def create_notexist_dir(dirpath, logger=True):
  if not os.path.exists(dirpath):
    os.makedirs(dirpath)
    if logger:
      logging.info(foldercreated.replace('%%%', dirpath))
      return
def memidformatter(memid, groupname):
    if isinstance(memid, str):
      for group in config['Sakamichi_App'][groupname][groups]:
        for subslist in config['Sakamichi_App'][groupname]['subscribed_members']:
          if memid == group['name'].replace(' ','') and memid == subslist['name'].replace(' ',''):
            return group['id']
    elif isinstance(memid, int):
      return str(memid)
def dateformatter(date):
  if isinstance(date, str):
    date = datetime.datetime.strptime(date.replace('.','-').replace(' ','-'), '%Y-%m-%d').date()
  return date
def remove_indent(longtext):
  lines  = longtext.split('\n')
  lines  = [line.strip() for line in lines]
  result = '\n'.join(lines)
  return result
def browser_errlog(value):
  logging.error(remove_indent(f"\n \
  {'=' * scrwidth}\n \
  {value.status_code}\n \
  {value.url}\n \
  {value.json()}\n \
  {'=' * scrwidth}"))
def date_list(fromdate, todate):
  fromdate  = datetime.datetime.strptime(fromdate, "%Y-%m-%d")
  enddate   = datetime.datetime.strptime(todate, "%Y-%m-%d")
  daterange = [fromdate + datetime.timedelta(days=i) for i in range(0, (enddate-fromdate).days+1)]
  datestr   = [d.strftime('%Y-%m-%d') for d in daterange]
  return datestr
  
# TELEGRAM CONFIG
service       = config['Telegram_Config']['service']
servicemode   = config['Telegram_Config']['servicemode']
botdebugtoken = config['Telegram_Config']['botdebugtoken']
botdebuggroup = config['Telegram_Config']['botdebuggroup']
botfinaltoken = config['Telegram_Config']['botfinaltoken']
botfinalgroup = config['Telegram_Config']['botfinalgroup']
ownerid       = config['Telegram_Config']['ownerid']
prefix        = config['Telegram_Config']['prefix']

tabulate.PRESERVE_WHITESPACE = True

def teletoken():
  if servicemode == 'debug':
    return botdebugtoken
  elif servicemode == 'prod':
    return botfinaltoken
def telechatid():
  if servicemode == 'debug':
    return botdebuggroup
  elif servicemode == 'prod':
    return botfinalgroup
def telemessagelogger(message):
  logging.info(remove_indent(f"\n \
  {'=' * scrwidth}\n \
  - ID Pengirim : {message.from_user.id}\n \
  - UN Pengirim : {message.from_user.username}\n \
  - ID Chat     : {message.chat.id}\n \
  - Tipe Chat   : {message.chat.type}\n \
  - Pesan       : {message.text}\n \
  {'=' * scrwidth}"))
  return
def telecalllogger(call):
  logging.info(remove_indent(f"\n \
  {'=' * scrwidth}\n \
  - ID Chat     : {call.message.chat.id}\n \
  - Tipe Chat   : {call.message.chat.type}\n \
  - UN Pengirim : {call.message.chat.username}\n \
  - Call Key    : {call.data}\n \
  {'=' * scrwidth}"))
  return
def report_message(message):
  text = remove_indent(f"\n \
  `==============================\n \
  WARNING\! Intruders detected\!\n \
  ==============================\n \
  - ID Pengirim : {message.from_user.id}\n \
  - UN Pengirim : {message.from_user.username}\n \
  - ID Chat     : {message.chat.id}\n \
  - Tipe Chat   : {message.chat.type}\n \
  - Pesan       : {message.text}\n \
  ==============================`")
  return text
def telegroupservicetoggler(group):
  with open(configdir, 'r+') as configfile:
    config = json.load(configfile)
    config['Sakamichi_App'][group]['telegram_services']['services'] = not config['Sakamichi_App'][group]['telegram_services']['services']
    configfile.seek(0)
    json.dump(config, configfile, indent=2)
    configfile.truncate()
def telememberservicetoggler(calltext, group):
  memid = calltext.split('-')[1]
  memberlists = []
  memberlists.clear()
  with open(configdir, 'r+') as configfile:
    config = json.load(configfile)
    for member in config['Sakamichi_App'][group]['telegram_services']['members']:
      if member['id'] == int(memid):
        member['service'] = not member['service']
        break
    configfile.seek(0)
    json.dump(config, configfile, indent=2)
    configfile.truncate()
def grouplister(group, appendto):
  with open(configdir) as configfile:
    config = json.load(configfile)
    services = config['Sakamichi_App'][group]['telegram_services']['services']
    for memberlist in config['Sakamichi_App'][group]['telegram_services']['members']:
      if services and memberlist['service'] == True:
        appendto.append(memberlist['id'])
def update_refresh_token(grup, refreshtoken):
  with open(configdir, 'r+') as configfile:
    config = json.load(configfile)
    config['Sakamichi_App'][grup]['refresh_token'] = refreshtoken
    configfile.seek(0)
    json.dump(config, configfile, indent=2)
    configfile.truncate()
  logging.info(refreshtokenupdated.replace('%grup%', grup))

def get_subsinfo(group):
  config = configfile()
  sublists = [[realmember['id'], 
               realmember['subscription'].get('end_at', 'None').split('T')[0].replace('-','') if member['service'] else '',
               realmember['name']] 
              for realmember in config['Sakamichi_App'][group]['subscribed_members'] 
              for member in config['Sakamichi_App'][group]['telegram_services']['members'] 
              if  member['id'] == realmember['id'] and member['service']]
  if sublists:
    return tabulate.tabulate(sublists, headers=["ID", "Exp", "Member"], 
                           colalign=("center", "center", "left"), disable_numparse=True, 
                           maxcolwidths=[2, 10, 11], tablefmt="rst")
  else:
    return "Maaf, layanan tidak tersedia!"
# TELEGRAM MESSAGE PHRASE CONFIG
replystart = "\
Halo %user%\!\n\
Perkenalkan, bot ini bernama Miyumiyuland\_bot\. \
Bot ini didesain untuk menyinkronisasikan pesan \
dari tiga aplikasi Sakamichi Mobile Message ke telegram\. \
Pembuat bot ini bermaksud agar memudahkan pengguna \
untuk mengarsipkan pesan dari ketiga aplikasi tersebut\."

preventintruders = "\
Mohon maaf\, anda tidak diperkenankan untuk menjalankan \
perintah ini\."

configmessages = f"\n\
`=============================\n\
         KONFIGURASI         \n\
=============================\n\
Harap pilih salah satu menu\n\
dibawah ini\.\n\
\- Update database\n\
Opsi untuk mengupdate list \n\
member langganan kalian\.\n\
\- Service toggle\n\
Opsi untuk mengaktifkan atau \n\
menonaktifkan layanan\.\n\
`"

selectgm = f"\n\
`=============================\n\
         KONFIGURASI         \n\
=============================\n\
Pilih layanan yang ingin\n\
diaktifkan atau \n\
dinonaktifkan\.`"

syncstarted ="\
Sinkronisasi dimulai ! 🫡"

syncstopped ="\
Sinkronisasi telah dihentikan ! 🫡"

incorrectsubsinfo ="\
Maaf, command yang anda masukkan \
salah. Harap masukkan nama grup \
(nogizaka46, sakurazaka46, hinatazaka46).\n\
Contoh :\n\
/subsinfo nogizaka46"

incorrectsendpast ="\
Maaf, command yang anda masukkan \
salah. Harap masukkan nama grup \
(nogizaka46, sakurazaka46, hinatazaka46) \
dan diikuti oleh nama member tanpa spasi!\n\
Contoh :\n\
/sendpastmessage nogizaka46 柴田柚菜"

aboutmessage ="\
*MENGENAI BOT*\n\
`Nama   : Miyumiyuland_bot\n\
Versi  : 2.0.0`\n\
\n\
*CHANGELOG*\n\
\- Perubahan sintak dari\n\
versi 1\.1\.2\n\
\- Penambahan fungsi\n\
Asynchronous\n\
\n\
*DEVELOPER*\n\
`Nama   : HASHINAMI\n\
Kontak : `[linktr\.ee](https://linktr\.ee/hashinami)"

