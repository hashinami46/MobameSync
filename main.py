# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# Importing Section
from database.config import *
from api.sakamichiapi import *

# Global Variable Section
nogitodaymessages = []
nogipastmessages  = []
nogicustmessages  = []
sakutodaymessages = []
sakupastmessages  = []
sakucustmessages  = []
hinatodaymessages = []
hinapastmessages  = []
hinacustmessages  = []

# MAIN PROGRAM
class Main:
  def __init__(self, apihost, headers, accesstoken, refreshtoken, plainreftoken, groups):
    self.apihost       = apihost
    self.headers       = headers
    self.refreshtoken  = refreshtoken
    self.accesstoken   = accesstoken
    self.plainreftoken = plainreftoken
    self.groups        = groups
  
  def update_access_token_in_JSON(self):
    if self.groups in sakamichigroups:
      if self.plainreftoken in nullvalue:
        logging.error(refreshtokenundefined.replace('%%%', self.groups))
      elif self.plainreftoken not in nullvalue:
        browser = httpx.post(url = SecurePrefix + self.apihost + ApiVersion + UpdateTokenPath, headers = self.headers, json = self.refreshtoken)
        if browser.status_code == 200:
          browserJSON = browser.json()
          with open(configdir, 'r+') as configfile:
            config = json.load(configfile)
            config['Sakamichi_App'][self.groups]['access_token'] = browserJSON['access_token']
            configfile.seek(0)
            json.dump(config, configfile, indent=2)
            configfile.truncate()
            logging.info(accesstokenupdated.replace('%%%', self.groups))
        else:
          logging.error(refreshtokendenied.replace('%%%', self.groups))
          logging.error(f"\n \
          ===============\n \
          {browser.url}\n \
          {browser.status_code}\n \
          {browser.json()}\n \
          ===============")

  def update_access_token_in_headers(self, logger=True):
    if self.groups in sakamichigroups:
      try:
        config = configfile()
        if config['Sakamichi_App'][self.groups]['access_token'] not in  nullvalue:
          self.headers['Authorization'] = 'Bearer ' + config['Sakamichi_App'][self.groups]['access_token']
          json.dumps(self.headers)
          if logger:
            logging.info(accesstokenadded.replace('%%%', self.groups))
          return
        else:
          logging.error(accesstokenundefined.replace('%%%', self.groups))
      except Exception:
        logging.error(f'{Exception}')
      
  def check_access_token(self):
    def check(addacc):
      if config['Sakamichi_App'][self.groups]['access_token'] in nullvalue:
        logging.error(accesstokenundefined.replace('%%%', self.groups))
      elif config['Sakamichi_App'][self.groups]['access_token'] not in nullvalue:
        addacc()
        browser = httpx.get(url = SecurePrefix + self.apihost + ApiVersion + GroupsPath, headers = self.headers)
        if browser.status_code != 200:
          logging.error(accesstokenexpired.replace('%%%', self.groups))
          logging.error(f"\n \
          ===============\n \
          {browser.url}\n \
          {browser.status_code}\n \
          {browser.json()}\n \
          ===============")
        else:
          logging.info(accesstokenvalid.replace('%%%', self.groups))
    if self.groups == 'nogizaka46':
      check(Nogizaka.update_access_token_in_headers)
    elif self.groups == 'sakurazaka46':
      check(Sakurazaka.update_access_token_in_headers)
    elif self.groups == 'hinatazaka46':
      check(Hinatazaka.update_access_token_in_headers)
  
  def get_groups_or_members_lists(self, choice, xchoice):
    def getlist(addacc, updateacc, refresh):
      addacc()
      browser = httpx.get(url = SecurePrefix + self.apihost + ApiVersion + choice, headers = self.headers)
      if browser.status_code == 200:
        with open(configdir, 'r+') as configfile:
          config = json.load(configfile)
          browserjson = browser.json()
          config['Sakamichi_App'][self.groups][xchoice] = browserjson
          configfile.seek(0)
          json.dump(config, configfile, indent=2)
          configfile.truncate()
          logging.info(gmlistdbupdated.replace('%%%0', xchoice).replace('%%%', self.groups))
        return
      else:
        logging.info(accesstokenexpired.replace('%%%', self.groups))
        logging.error(f"\n \
        ===============\n \
        {browser.status_code}\n \
        {browser.url}\n \
        {browser.headers}\n \
        {browser.json()}\n \
        ===============")
        updateacc()
        refresh(choice, xchoice)
    if self.groups == 'nogizaka46':
      getlist(Nogizaka.update_access_token_in_headers, Nogizaka.update_access_token_in_JSON, Nogizaka.get_groups_or_members_lists)
    elif self.groups == 'sakurazaka46':
      getlist(Sakurazaka.update_access_token_in_headers, Sakurazaka.update_access_token_in_JSON, Sakurazaka.get_groups_or_members_lists)
    elif self.groups == 'hinatazaka46':
      getlist(Hinatazaka.update_access_token_in_headers, Hinatazaka.update_access_token_in_JSON, Hinatazaka.get_groups_or_members_lists)
  
  def get_subscribed_members(self):
    async def updater(updatelist):
      updatelist(GroupsPath, groups)
      with open(configdir, 'r+') as configfile:
        config = json.load(configfile)
        subslists = [sublist for sublist in config['Sakamichi_App'][self.groups][groups] if 'subscription' in sublist]
        config['Sakamichi_App'][self.groups]['subscribed_members'] = subslists
        configfile.seek(0)
        json.dump(config, configfile, indent=2)
        configfile.truncate()
        logging.info(subscriptionupdated.replace('%%%', self.groups))
    
    if self.groups == 'nogizaka46':
      asyncio.run(updater(Nogizaka.get_groups_or_members_lists))
    elif self.groups == 'sakurazaka46':
      asyncio.run(updater(Sakurazaka.get_groups_or_members_lists))
    elif self.groups == 'hinatazaka46':
      asyncio.run(updater(Hinatazaka.get_groups_or_members_lists))
  
  def download_thumbnail_or_phoneimage_from_groups_or_members(self, tpchoice, gmchoice, dldir=downloaddir):
    async def download(urls, checkdir):
      async with httpx.AsyncClient(timeout=None) as client:
        tasks = []
        folderpath = f"{ROOT_DIR}{dldir}/{self.groups}/{gmchoice}/{tpchoice}"
        checkdir(folderpath)
        for url in urls:
          filename = os.path.basename(url)
          if not os.path.exists(f"{folderpath}/{filename}"):
            tasks.append(asyncio.create_task(client.get(url)))
          else:
            logging.info(alreadydownloaded.replace('%%%', filename))
        if tasks:
          downloaders = await asyncio.gather(*tasks)
          for download in downloaders:
            with open(f'{folderpath}/{os.path.basename(download.url.path)}', 'wb') as file:
              file.write(download.content)
            logging.info(downloadsuccess.replace('%%%', os.path.basename(download.url.path)).replace('%dir%', folderpath))
    urls = []
    for links in config['Sakamichi_App'][self.groups][gmchoice]:
      if tpchoice in links and links[tpchoice] not in nullvalue:
        urls.append(links[tpchoice])
    asyncio.run(download(urls, create_notexist_dir))
    
  def past_messages_streamer(self, memlist):
    async def url_streamer(url, addtoken, refresher, tempmessages):
      async with httpx.AsyncClient(timeout=None) as client:
        await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), addtoken, False)
        browser = await client.get(url, headers=self.headers)
        if browser.status_code == 200:
          messages = browser.json()['messages']
          for message in messages:
            if not any(message['id'] == tempmessage['id'] for tempmessage in tempmessages):
              tempmessages.append(message)
        elif browser.status_code == 401:
          logging.error(remove_indent(f"\n \
          ===============\n \
          {browser.status_code}\n \
          {browser.url}\n \
          {browser.json()}\n \
          ==============="))
          await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), refresher)
          await url_streamer(url, addtoken, refresher, tempmessages)
        elif browser.status_code == 400:
          logging.error(remove_indent(f"\n \
          ===============\n \
          {browser.status_code}\n \
          {browser.url}\n \
          {browser.json()}\n \
          ==============="))
          logging.error(remove_indent(f"\n \
          CHECK YOUR REFRESH TOKEN!"))
          return 
        elif browser.status_code == 429:
          logging.error(remove_indent(f"\n \
          ===============\n \
          {browser.status_code}\n \
          {browser.url}\n \
          {browser.json()}\n \
          ==============="))
          time.sleep(300)
          await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), refresher)
          await url_streamer(url, addtoken, refresher, tempmessages)
    async def executor(addtoken, refresher, tempmessages):
      tempmessages.clear()
      urls = await url_creator()
      for url in urls:
        await url_streamer(url, addtoken, refresher, tempmessages)
    async def url_creator():
      urls = []
      urls.clear()
      links = [f"{SecurePrefix}{self.apihost}{ApiVersion}{GroupsPath}/{memidformatter(mem, self.groups)}{PastMessagesPath}" for mem in memlist]
      for link in links:
        realmemid = link.split('?')[0].split('/')[-2]
        if realmemid != 'None':
          urls.append(link)
      return urls
    if self.groups == 'nogizaka46':
      asyncio.run(executor(Nogizaka.update_access_token_in_headers, Nogizaka.update_access_token_in_JSON, nogipastmessages))
    elif self.groups == 'sakurazaka46':
      asyncio.run(executor(Sakurazaka.update_access_token_in_headers, Sakurazaka.update_access_token_in_JSON, sakupastmessages))
    elif self.groups == 'hinatazaka46':
      asyncio.run(executor(Hinatazaka.update_access_token_in_headers, Hinatazaka.update_access_token_in_JSON, hinapastmessages))
      
  def stream_timelines(self, memlist, datelist=[YST]):
    async def url_streamer(url, addtoken, refresher, tempmessages):
      async with httpx.AsyncClient(timeout=60) as client:
        await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), addtoken, False)
        browser = await client.get(url, headers=self.headers)
        if browser.status_code == 200:
          messages = browser.json()['messages']
          for message in messages:
            if not any(message['id'] == tempmessage['id'] for tempmessage in tempmessages):
              tempmessages.append(message)
        elif browser.status_code == 401:
          logging.error(remove_indent(f"\n \
          ===============\n \
          {browser.status_code}\n \
          {browser.url}\n \
          {browser.json()}\n \
          ==============="))
          await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), refresher)
          await url_streamer(url, addtoken, refresher, tempmessages)
        elif browser.status_code == 400:
          logging.error(remove_indent(f"\n \
          ===============\n \
          {browser.status_code}\n \
          {browser.url}\n \
          {browser.json()}\n \
          ==============="))
          logging.error(remove_indent(f"\n \
          CHECK YOUR REFRESH TOKEN!"))
          return 
        elif browser.status_code == 429:
          logging.error(remove_indent(f"\n \
          ===============\n \
          {browser.status_code}\n \
          {browser.url}\n \
          {browser.json()}\n \
          ==============="))
          time.sleep(300)
          await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), refresher)
          await url_streamer(url, addtoken, refresher, tempmessages)
    async def executor(addtoken, refresher, tempmessages):
      tempmessages.clear()
      urls = await url_creator()
      for url in urls:
        await url_streamer(url, addtoken, refresher, tempmessages)
    async def url_creator():
      urls = []
      urls.clear()
      links = [f"{SecurePrefix}{self.apihost}{ApiVersion}{GroupsPath}/{memidformatter(mem, self.groups)}{TimelinePath}?updated_from={dateformatter(date).strftime('%Y-%m-%d' + 'T00:00:00Z').replace(':','%3A')}&order=asc&count=100" for mem in memlist for date in datelist]
      for link in links:
        realmemid = link.split('?')[0].split('/')[-2]
        if realmemid != 'None':
          urls.append(link)
      return urls
    if self.groups == 'nogizaka46':
      asyncio.run(executor(Nogizaka.update_access_token_in_headers, Nogizaka.update_access_token_in_JSON, nogitodaymessages))
    elif self.groups == 'sakurazaka46':
      asyncio.run(executor(Sakurazaka.update_access_token_in_headers, Sakurazaka.update_access_token_in_JSON, sakutodaymessages))
    elif self.groups == 'hinatazaka46':
      asyncio.run(executor(Hinatazaka.update_access_token_in_headers, Hinatazaka.update_access_token_in_JSON, hinatodaymessages))
      
  def custmessage_lister(self, memlist, datelist):
    async def url_streamer(url, addtoken, refresher, tempmessages):
      async with httpx.AsyncClient(timeout=60) as client:
        await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), addtoken, False)
        browser = await client.get(url, headers=self.headers)
        if browser.status_code == 200:
          messages = browser.json()['messages']
          for message in messages:
            if not any(message['id'] == tempmessage['id'] for tempmessage in tempmessages):
              tempmessages.append(message)
        elif browser.status_code == 401:
          logging.error(remove_indent(f"\n \
          ===============\n \
          {browser.status_code}\n \
          {browser.url}\n \
          {browser.json()}\n \
          ==============="))
          await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), refresher)
          await url_streamer(url, addtoken, refresher, tempmessages)
        elif browser.status_code == 400:
          logging.error(remove_indent(f"\n \
          ===============\n \
          {browser.status_code}\n \
          {browser.url}\n \
          {browser.json()}\n \
          ==============="))
          logging.error(remove_indent(f"\n \
          CHECK YOUR REFRESH TOKEN!"))
          return
        elif browser.status_code == 429:
          logging.error(remove_indent(f"\n \
          ===============\n \
          {browser.status_code}\n \
          {browser.url}\n \
          {browser.json()}\n \
          ==============="))
          time.sleep(300)
          await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), refresher)
          await url_streamer(url, addtoken, refresher, tempmessages)
    async def executor(addtoken, refresher, tempmessages):
      tempmessages.clear()
      urls = await url_creator()
      for url in urls:
        await url_streamer(url, addtoken, refresher, tempmessages)
    async def url_creator():
      urls = []
      urls.clear()
      links = [f"{SecurePrefix}{self.apihost}{ApiVersion}{GroupsPath}/{memidformatter(mem, self.groups)}{TimelinePath}?updated_from={dateformatter(date).strftime('%Y-%m-%d' + 'T00:00:00Z').replace(':','%3A')}&order=asc" for mem in memlist for date in datelist]
      for link in links:
        realmemid = link.split('?')[0].split('/')[-2]
        if realmemid != 'None':
          urls.append(link)
      return urls
    if self.groups == 'nogizaka46':
      asyncio.run(executor(Nogizaka.update_access_token_in_headers, Nogizaka.update_access_token_in_JSON, nogicustmessages))
    elif self.groups == 'sakurazaka46':
      asyncio.run(executor(Sakurazaka.update_access_token_in_headers, Sakurazaka.update_access_token_in_JSON, sakucustmessages))
    elif self.groups == 'hinatazaka46':
      asyncio.run(executor(Hinatazaka.update_access_token_in_headers, Hinatazaka.update_access_token_in_JSON, hinacustmessages))
  
  def custmessage_downloader(self, memlist, datelist, dlpath=f'{downloaddir}'):
    async def download(url, folder, filename):
      async with httpx.AsyncClient(timeout=None) as client:
        browser = await client.get(url)
        if browser.status_code == 200:
          with open(os.path.join(folder, filename), 'wb') as file:
            file.write(browser.content)
    async def checker(membername, url, date):
      folder   = f"{ROOT_DIR}{dlpath}/{self.groups}/{membername}/{date}/"
      filename = os.path.basename(urlparse(url).path)
      filepath = os.path.join(folder, filename)
      create_notexist_dir(folder, logger=False)
      if not os.path.exists(filepath):
        await download(url, folder, filename)
        logging.info(f"{downloadsuccessv2.replace('%file%', filename)}")
      else:
        logging.info(f"{alreadydownloaded.replace('%%%', filename)}")
    async def tasker(getcustmessages, custmessages):
      await asyncio.get_running_loop().run_in_executor(ThreadPoolExecutor(), getcustmessages, memlist, datelist)
      tasks = []
      for messages in custmessages:
        for members in config['Sakamichi_App'][self.groups]['subscribed_members']:
          if messages['group_id'] == members['id'] and messages['type'] != 'text':
            url  = messages['file']
            date = messages['updated_at'].split('T')[0].replace('-','.')
            membername = members['name'].replace(' ','')
            tasks.append(checker(membername, url, date))
      await asyncio.gather(*tasks)
    if self.groups == 'nogizaka46':
      asyncio.run(tasker(Nogizaka.custmessage_lister, nogicustmessages))
    elif self.groups == 'sakurazaka46':
      asyncio.run(tasker(Sakurazaka.custmessage_lister, sakucustmessages))
    elif self.groups == 'hinatazaka46':
      asyncio.run(tasker(Hinatazaka.custmessage_lister, hinacustmessages))
      
  def teleservice_updater(self):
    def updater(getlist):
      try:
        getlist()
        servicelists = []
        servicelists.clear()
        with open(configdir, 'r+') as configfile:
          config = json.load(configfile)
          for subslist in config['Sakamichi_App'][self.groups]['subscribed_members']:
            service = {
              "id": subslist['id'],
              "name": subslist['name'],
              "service": True
            }
            if not any(service['id'] == tempservicelist['id'] for tempservicelist in servicelists):
              servicelists.append(service)
          config['Sakamichi_App'][self.groups]['telegram_services']['members'] = servicelists
          configfile.seek(0)
          json.dump(config, configfile, indent=2)
          configfile.truncate()
          logging.info(teleserviceupdated.replace('%group%', self.groups))
      except Exception as e:
        logging.error(e)
    if self.groups == 'nogizaka46':
      updater(Nogizaka.get_subscribed_members)
    elif self.groups == 'sakurazaka46':
      updater(Sakurazaka.get_subscribed_members)
    elif self.groups == 'hinatazaka46':
      updater(Hinatazaka.get_subscribed_members)
Nogizaka   = Main(nogiApi, NogiPlainHeaders, NogiAccessToken, NogiRefreshToken, NogiPlainRefToken, 'nogizaka46')
Sakurazaka = Main(sakuApi, SakuPlainHeaders, SakuAccessToken, SakuRefreshToken, SakuPlainRefToken, 'sakurazaka46')
Hinatazaka = Main(hinaApi, HinaPlainHeaders, HinaAccessToken, HinaRefreshToken, HinaPlainRefToken, 'hinatazaka46')

# AVAILABLE FUNCTION
# <Groupname>.update_access_token_in_JSON()
# <Groupname>.update_access_token_in_headers()
# <Groupname>.get_groups_or_members_lists(MembersPath/GroupsPath, members/groups)
# <Groupname>.get_subscribed_members()
# <Groupname>.download_thumbnail_or_phoneimage_from_groups_or_members(thumbnail/phone_image, groups/members)
# <Groupname>.stream_timelines([listmember], [listdate]) #listdate default YST
# <Groupname>.custmessage_lister([listmember],[listdate]) 
# <Groupname>.custmessage_downloader([listmember],[listdate],dlpath) #dlpath default './mobame'
# <Groupname>.teleservice_updater()

#fromdate  = datetime.datetime.strptime("2023-02-25", "%Y-%m-%d")
#enddate   = datetime.datetime.strptime("2023-03-02", "%Y-%m-%d")
#daterange = [fromdate + datetime.timedelta(days=i) for i in range(0, (enddate-fromdate).days+1)]
#datestr   = [d.strftime('%Y-%m-%d') for d in daterange]
