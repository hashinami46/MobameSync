# -*- coding: utf-8 -*-

# Importing Section
import main
import argparse
from database.config import *

# Argument Object Section
parser = argparse.ArgumentParser(
  description =\
  'This app helps you download messages (photos, voice, and videos) from the members you subscribed in the Sakamichi group series (Nogizaka46, Sakurazaka46, Hinatazaka46) mobile mail (Mobame) app. Simply input the group and member name, and this app will download all messages from your mobame account.',
  epilog      =\
  'Example Usage:\n\
  python3 mobame.py -s update -g nogizaka46\n\
  python3 mobame.py -s check -g nogizaka46\n\
  python3 mobame.py -s dl -g nogizaka46 -m 柴田柚菜\n\
  python3 mobame.py -s dl -g nogizaka46 -m 柴田柚菜 -d 2023-03-08\n\
  python3 mobame.py -s dllist -g nogizaka46 -m 柴田柚菜 早川聖来 -d 2023-03-08 2023-03-09\n\
  ',formatter_class=argparse.RawTextHelpFormatter)
  
group_choices   = ['nogizaka46', '乃木坂46', 'sakurazaka46', '櫻坂46', 'hinatazaka46', '日向坂46']
service_choices = ['updatesubslist', 'update', 'checksubslist', 'check', 'download', 'dl', 'downloadlist', 'dllist']

# Arguments Section
parser.add_argument('-s', '--service', metavar='service', help='Choose service!', choices=service_choices, required=True)
parser.add_argument('-g', '--group', metavar='group', help='Select Group!', choices=group_choices, required=True)
parser.add_argument('-m', '--member', metavar='member', help='Member name(s) in kanji without space.', nargs='+')
parser.add_argument('-d', '--date', metavar='date', help='Date(s) in YYYY-MM-DD, default is today.', nargs='+', default=[NOW])
parser.add_argument('-fd', '--fromdate', metavar='fromdate', help='Message date in YYYY-MM-DD')
parser.add_argument('-td', '--todate', metavar='todate', help='Message date in YYYY-MM-DD')

args = parser.parse_args()

# FUNCTION SECTION
def dl_result(args, choosedgroup, mainprogram):
  print('=' * scrwidth)
  print(f"Queried at       : {NOW.strftime('%Y-%m-%d %H:%M:%S')}")
  print(f"Requested Group  : {choosedgroup}")
  print(f"Requested Member : {', '.join(args.member)}")
  print(f"Requested Date   : {', '.join(args.date)}")
  print('=' * scrwidth)
  mainprogram(memlist=args.member, datelist=args.date, logger=False, mode="terminal")
  print('=' * scrwidth)
  print("Result :")
  print(f" Downloaded Successfully : {len(main.resultokdl)} file(s)")
  print(f" Already Downloaded      : {len(main.resultnokdl)} file(s)")
  print(f"Download saved at : {downloaddir}")
  print('=' * scrwidth)
def dllist_result(args, choosedgroup, mainprogram):
  print('=' * scrwidth)
  print(f"Queried at       : {NOW.strftime('%Y-%m-%d %H:%M:%S')}")
  print(f"Requested Group  : {choosedgroup}")
  print(f"Requested Member : {', '.join(args.member)}")
  print(f"From date        : {args.fromdate}")
  print(f"To date          : {args.todate}")
  print('=' * scrwidth)
  print("Progress :")
  mainprogram(memlist=args.member, datelist=date_list(args.fromdate, args.todate), logger=False, mode="terminal")
  print('=' * scrwidth)
  print("Result :")
  print(f" Downloaded Successfully : {len(main.resultokdl)} file(s)")
  print(f" Already Downloaded      : {len(main.resultnokdl)} file(s)")
  print(f"Download saved at : {downloaddir}")
  print('=' * scrwidth)
def update_subslist(args, choosedgroup, mainprogram):
  print('=' * scrwidth)
  print(f"Queried at       : {NOW.strftime('%Y-%m-%d %H:%M:%S')}")
  print(f"Requested Group  : {choosedgroup}")
  print('=' * scrwidth)
  mainprogram(main.GroupsPath, main.groups, logger=False)
  mainprogram(main.MembersPath, main.members, logger=False)
  print('=' * scrwidth)
def check_subslist(choosedgroup, choosedgroupkanji):
  print('=' * scrwidth)
  print(f"Queried at       : {NOW.strftime('%Y-%m-%d %H:%M:%S')}")
  print(f"Requested Group  : {choosedgroupkanji}")
  print('=' * scrwidth)
  config = configfile()
  counter = 1
  for number, member in enumerate(config['Sakamichi_App'][choosedgroup]['groups']):
    if 'subscription' in member:
      counter_str = str(counter).zfill(2)
      print(f"{counter_str}. Member ID   : {member['id']}")
      print(f"    Member Name : {member['name'].replace(' ', '')}")
      print(f"    Expired At  : {member['subscription'].get('end_at', '-').split('T')[0]}")
      counter += 1
  print('=' * scrwidth)

if args.service in ['download', 'dl'] and args.group in ['nogizaka46', '乃木坂46']:
  dl_result(args, '乃木坂46', main.Nogizaka.custmessage_downloader)
elif args.service in ['download', 'dl'] and args.group in ['sakurazaka46', '櫻坂46']:
  dl_result(args, '櫻坂46', main.Sakurazaka.custmessage_downloader)
elif args.service in ['download', 'dl'] and args.group in ['hinatazaka46', '日向坂46']:
  dl_result(args, '日向坂46', main.Hinatazaka.custmessage_downloader)

elif args.service in ['downloadlist', 'dllist'] and args.group in ['nogizaka46', '乃木坂46']:
  dllist_result(args, '乃木坂46', main.Nogizaka.custmessage_downloader)
elif args.service in ['downloadlist', 'dllist'] and args.group in ['sakurazaka46', '櫻坂46']:
  dllist_result(args, '櫻坂46', main.Sakurazaka.custmessage_downloader)
elif args.service in ['downloadlist', 'dllist'] and args.group in ['hinatazaka46', '日向坂46']:
  dllist_result(args, '日向坂46', main.Hinatazaka.custmessage_downloader)
  
elif args.service in ['updatesubslist', 'update'] and args.group in ['nogizaka46', '乃木坂46']:
  update_subslist(args, '乃木坂46', main.Nogizaka.get_groups_or_members_lists)
elif args.service in ['updatesubslist', 'update'] and args.group in ['sakurazaka46', '櫻坂46']:
  update_subslist(args, '櫻坂46', main.Sakurazaka.get_groups_or_members_lists)
elif args.service in ['updatesubslist', 'update'] and args.group in ['hinatazaka46', '日向坂46']:
  update_subslist(args, '日向坂46', main.Hinatazaka.get_groups_or_members_lists)
  
elif args.service in ['checksubslist', 'check'] and args.group in ['nogizaka46', '乃木坂46']:
  check_subslist('nogizaka46', '乃木坂46')
elif args.service in ['checksubslist', 'check'] and args.group in ['sakurazaka46', '櫻坂46']:
  check_subslist('sakurazaka46', '櫻坂46')
elif args.service in ['checksubslist', 'check'] and args.group in ['hinatazaka46', '日向坂46']:
  check_subslist('hinatazaka46', '日向坂46')

# mobame.py [--group or -g] Groupname [--member or -members] Membername [--date or -d]