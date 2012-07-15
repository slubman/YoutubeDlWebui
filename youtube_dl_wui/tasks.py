# -*- coding: utf-8 -*-

from celery import Celery
import os
import tempfile

celery =  Celery('tasks', broker='amqp://guest@localhost//')

# Download a video and mail the URL for the download
@celery.task
def download(url, email):
   print 'Downloading: %s' % (url)
   print 'Send result to: %s' % (email)
   script_file = os.getcwd() + '/lib/youtube-dl/youtube-dl'
   args = ['youtube-dl', script_file, '--title', '--quiet', '--no-progress', url]
   print 'PWD: %s' % (os.getcwd())
   print 'Command: %s' % (args)
   try:
      # Create a directory for the download
      directory = tempfile.mkdtemp(prefix='youtube-dl')
      # Go to the created directory
      os.chdir(directory)
      print 'PWD: %s' % (os.getcwd())
      # Download video
      os.spawnvp(os.P_WAIT, 'python2', args)
      print 'Download done'
   except Exception as e:
      print 'Download failed: %s' % (e)

   print 'Task done.'

#
@celery.task
def delete(directory):
   pass
