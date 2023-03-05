# -*- coding: utf-8 -*-

from database.config import *

# Sakamichi Api Host
nogiApi = 'api.n46.glastonr.net'
sakuApi = 'api.s46.glastonr.net'
hinaApi = 'api.kh.glastonr.net'

# Sakamichi Api Endpoint
SecurePrefix        = 'https://'
ApiVersion          = '/v2'
SigninPath          = '/signin'
UpdateTokenPath     = '/update_token'
TagsPath            = '/tags'
GroupsPath          = '/groups'
MembersPath         = '/members'
TimelinePath        = '/timeline'
MessagesPath        = '/messages'
PastMessagesPath    = '/past_messages'
AnnouncementsPath   = '/announcements'
BlogsPath           = '/blogs'

# Sakamichi Plain Headers
useragent       = 'Dalvik/2.1.0 (Linux; U; Android 12; 2201117TY Build/SKQ1.211103.001)'
connection      = 'keep-alive'
contenttype     = 'application/json'
accept          = 'application/json'
acceptlanguage  = 'ja-JP'
acceptencodingA = 'gzip'
acceptencodingB = 'deflate'
TE              = 'deflate'

NogiPlainHeaders = {
  'host'            : nogiApi,
  'X-Talk-App-ID'   : 'jp.co.sonymusic.communication.nogizaka 2.2',
  'user-agent'      : useragent,
  'connection'      : connection,
  'content-type'    : contenttype,
  'accept'          : accept,
  'accept-language' : acceptlanguage,
  'accept-encoding' : acceptencodingA,
  'accept-encoding' : acceptencodingB,
  'TE'              : TE,
}

SakuPlainHeaders = {
  'host'            : sakuApi,
  'X-Talk-App-ID'   : 'jp.co.sonymusic.communication.sakurazaka 2.2',
  'user-agent'      : useragent,
  'connection'      : connection,
  'content-type'    : contenttype,
  'accept'          : accept,
  'accept-language' : acceptlanguage,
  'accept-encoding' : acceptencodingA,
  'accept-encoding' : acceptencodingB,
  'TE'              : TE,
}

HinaPlainHeaders = {
  'host'            : hinaApi,
  'X-Talk-App-ID'   : 'jp.co.sonymusic.communication.hinatazaka 2.2',
  'user-agent'      : useragent,
  'connection'      : connection,
  'content-type'    : contenttype,
  'accept'          : accept,
  'accept-language' : acceptlanguage,
  'accept-encoding' : acceptencodingA,
  'accept-encoding' : acceptencodingB,
  'TE'              : TE,
}

# Advanced Authorization
NogiPlainRefToken = config['Sakamichi_App']['nogizaka46']['refresh_token']
SakuPlainRefToken = config['Sakamichi_App']['sakurazaka46']['refresh_token']
HinaPlainRefToken = config['Sakamichi_App']['hinatazaka46']['refresh_token']

NogiRefreshToken = {"refresh_token":config['Sakamichi_App']['nogizaka46']['refresh_token']}
SakuRefreshToken = {"refresh_token":config['Sakamichi_App']['sakurazaka46']['refresh_token']}
HinaRefreshToken = {"refresh_token":config['Sakamichi_App']['hinatazaka46']['refresh_token']}

NogiAccessToken = 'Bearer ' + config['Sakamichi_App']['nogizaka46']['access_token']
SakuAccessToken = 'Bearer ' + config['Sakamichi_App']['sakurazaka46']['access_token']
HinaAccessToken = 'Bearer ' + config['Sakamichi_App']['hinatazaka46']['access_token']