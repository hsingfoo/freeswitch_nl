#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import urllib
import os

#There are two Dutch voices
voices=[{'id':21,'name': 'Anika'},{'id':22,'name': 'Markus'}]

#Talking speed for Natural Readers
speed=0
#folder names for freeswitch (language, dialect)
language=['nl','nl']
#Free API key. May change in the future. Please check website Natural Readers
apikey='b98x9xlfs54ws4k0wc0o8g4gwc0w8ss'

get_params={'apikey': apikey, 'src': 'pw', 'r':voices[0]['id'], 's':speed, 't':''}
with open('freeswitch_nl_translations.csv', 'rb') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
  for row in csvreader:
    if row[2] != '':
      for voice in voices:
        get_params['t'] = row[2]
        url = 'https://api.naturalreaders.com/v4/tts/macspeak?%s'%(urllib.urlencode(get_params))

        targetdir  = 'naturalreaders/%s/%s'%(voice['name'], row[0][1:] if row[0][0]=='/' else row[0])
        targetfile = '%s'%(row[1])

        try:
          os.stat(targetdir)
        except:
          #print 'Creating folder %s'%(targetdir)
          os.makedirs(targetdir)
        print 'Processing %s/%s'%(targetdir,targetfile)
        #print 'Downloading %s'%(url)
        urllib.urlretrieve (url, "%s/%s.mp3" %(targetdir, targetfile) )
        #print 'Converting %s/%s.mp3 to %s/%s'%(targetdir,targetfile,targetdir,targetfile)
        os.system( 'ffmpeg -v 0 -y -i %s/%s.mp3 %s/%s'%(targetdir,targetfile,targetdir,targetfile) )

        for samplerate in [8000,16000,32000,48000]:
          targetdir2  = 'output/%s/%s/%s/%s/%d'%(language[0],language[1],voice['name'], row[0][1:] if row[0][0]=='/' else row[0], samplerate)
          try:
            os.stat(targetdir2)
          except:
            #print 'Creating folder %s'%(targetdir2)
            os.makedirs(targetdir2)
          #print 'Converting %s/%s to %s/%s'%(targetdir,targetfile,targetdir2,targetfile)
          os.system( 'sox %s/%s -r 8k -c 1 -e signed-integer %s/%s'%(targetdir,targetfile,targetdir2,targetfile) )

        #print
