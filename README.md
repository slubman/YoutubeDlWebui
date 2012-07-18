
# What is it?

YoutubeDlWebui (abreviated to ytdlwui) is a (simple) frontend to the [youtube-dl](http://rg3.github.com/youtube-dl/) unix command.

This frontend provide a simple webpage to have a video downloaded, and receive a link to this video by mail.

The application is using the BSD license, as seen in the LICENSE file.

## TODO

* Automatic deletion of retreived files
* Have more control other what is being retrieved
* Handle playlists
* Make an API

# Installation requirements

```
Django==1.4
celery==3.0.1
django-celery==3.0.1
python-dateutil==2.1
```
Installing those packages should bring all the required dependencies.

As an alternative you can use the requirements.txt file with
```
pip -r requirements.txt
```

# Configuration

More than the standard configuration for a Django application, you’ll need to define the following variables your project settings

## Standard Django settings that will need to be defined

###DEFAULT_FROM_MAIL
###EMAIL_HOST_USER
###EMAIL_HOST
###EMAIL_PORT
###EMAIL_HOST_PASSWORD

## Parameter for Celery

###BROKER_URL
How does Celery handle the message queue.

## Application specific parameters

###DOWNLOAD_DIRECTORY
This is the directory where the downloads will take place.
This directory must be writable by the user which will run the Celery tasks.

###BASE_URL
Here you define the front part of the URL that will be embeded in the mail.
A webserver must be configured to serve file located in `DOWNLOAD_DIRECTORY` at this url.
