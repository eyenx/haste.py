#! /usr/bin/env python
#
# lpaste.net python uploader
# by eyenx
#

# imports

import sys
import os
import getopt
import urllib.request
import urllib.parse

# usage

def usage(message=""):
  print("""usage:

  hpaste.py [options] [filepath or input]

  options:

  -p, --private    private paste (standard: public)
  -t, --title      title of paste (standard: filename or stdin)
  -a, --author     author name  (standard: none)
  -l, --language   language (standard: depends on filename ending)
  -s, --stdin      read from stdin
  -u, --url        change haste server url (standard: lpaste.net)
  """)
  print(message)
  sys.exit(1)

# option parser

def parse_options():
  try:
    options,arguments=getopt.getopt(sys.argv[1:],"pt:a:l:s",["private","title=","author=","language=","stdin"])
    return(options,arguments)
  except getopt.GetOptError as error:
    usage(str(error))

# request class

class HasteRequest():
  def __init__(self,private=False,title="",author="",language="",data="",url="http://lpaste.net/new"):
    self._private=private
    self._title=title
    self._author=author
    self._language=language
    self._data=data
    self._url=url
  def set_private(self,private):
    self._private=private
  def set_title(self,title):
    self._title=title
  def set_author(self,author):
    self._author=author
  def set_language(self,author):
    self._language=language
  def set_data(self,data):
    self._data=data
  def prepare_data(self):
    if self._private:
      self._jsonprivate="Private"
    else:
      self._jsonprivate="Public"
    self._jsondata={"public":self._jsonprivate,"title":self._title,"author":self._author,"language":self._language,"channel":"","paste":self._data,"email":""}
    self._requestdata=urllib.parse.urlencode(self._jsondata).encode('utf-8')
  def set_url(self,url):
    self._url=url
  # check if set
  def is_title_set(self):
    if self._title:
      return(True)
    else:
      return(False)
  # request with urllib
  def request(self):
    # prepare data
    self.prepare_data()
    # create request
    self._request=urllib.request.Request(self._url,self._requestdata,{"Content-Type":" application/x-www-form-urlencoded;charset=utf-8","User-Agent":"Mozilla/5.0"})
    # try to post
    try:
      self._response=urllib.request.urlopen(self._request)
    except urllib.error.URLError as error:
      print(str(error))
      sys.exit(1)
    self._pasteurl=self._response.geturl()
  def return_pasteurl(self):
    if self._pasteurl:
      return(self._pasteurl)

# main

if __name__ == "__main__":
  options,arguments=parse_options()
  # initialize HasteRequest
  myHasteRequest = HasteRequest();
  # if stdin, read from stdin
  for o,a in options:
    if o in ["-p","--private"]:
      myHasteRequest.set_private(True)
    if o in ["-t","--title"]:
      myHasteRequest.set_title(a)
    if o in ["-a","--author"]:
      myHasteRequest.set_author(a)
    if o in ["-l","--language"]:
      myHasteRequest.set_language(a)
    if o in ["-s","--stdin"]:
      if not myHasteRequest.is_title_set():
        myHasteRequest.set_title("stdin")
      myHasteRequest.set_data(sys.stdin.read())
    if o in ["-u","--url"]:
      myHasteRequest.set_url(a)

  if len(arguments):
    # to implement
    # if not myHasteRequest.is_language_set():
    #    set language from file ending
    if not myHasteRequest.is_title_set():
      myHasteRequest.set_title(os.path.basename(arguments[0]))
    myHasteRequest.set_data(open(arguments[0]).read())
  myHasteRequest.request();
  print(myHasteRequest.return_pasteurl())
