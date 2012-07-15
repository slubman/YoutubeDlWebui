# -*- coding: utf-8 -*-

from celery import Celery
import os
import tempfile
import smtplib
from email.mime.text import MIMEText
from datetime import *
from dateutil.relativedelta import *
from dateutil.tz import tzutc
from django.conf import settings

celery =  Celery('tasks', broker=settings.BROKER_URL)

__videos = ('.webm', '.mp4', '.flv')

# Download a video and mail the URL for the download
@celery.task
def download(url, email):
   print 'Downloading: %s' % (url)
   print 'Send result to: %s' % (email)
   script_file = os.getcwd() + '/lib/youtube-dl/youtube-dl'
   args = ['youtube-dl', script_file, '--title']
   if settings.DEBUG == False:
      args += ['--quiet', '--no-progress']
   args += [url]
   print 'PWD: %s' % (os.getcwd())
   print 'Command: %s' % (args)

   directory = None
   name = ''
   expiration = datetime.now(tzutc()) + relativedelta(day=+1)
   try:
      # Create a directory for the download
      directory = tempfile.mkdtemp(prefix='ytdlwui')
      # Go to the created directory
      os.chdir(directory)
      print 'PWD: %s' % (os.getcwd())
      # Download video
      os.spawnvp(os.P_WAIT, 'python2', args)
      print 'Download done'
      for entry in os.listdir(directory):
         for extension in __videos:
            if entry.endswith(extension):
               name = entry
               print 'Video file name: %s' % (name)
               print 'Download available until: %s' % (expiration.strftime('%Y-%m-%d %H:%M:%S%z'))
               break
         if len(name) > 0:
            break
   except Exception as e:
      print 'Download failed: %s' % (e)

   # Send email
   print 'Preparing mail'
   msg = MIMEText('''Hi,

You have requested the download the following video:
%s

I'm pleased to let you download the video there:
%s/%s/%s

The download will be available for 1 day, until:
%s

Best regards
--
youtube-dl\'s (simple) webui
      ''' % (url, settings.BASE_URL, os.path.basename(directory), name, expiration.strftime('%Y-%m-%d %H:%M:%S%z')))
   msg['From'] = settings.DEFAULT_FROM_MAIL
   msg['To'] = email
   msg['Subject'] = 'Video download finished'
   s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
   s.starttls()
   s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
   s.sendmail(settings.DEFAULT_FROM_MAIL, email, msg.as_string())
   print 'Mail sent'
   
   print 'Task done.'

#
@celery.task
def delete(directory):
   pass
