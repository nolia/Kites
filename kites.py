#!/usr/bin/python

import sys
import time
import logging
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

def watchFiles():
  logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

  path =  sys.argv[1] if len(sys.argv) > 1 else '.'
  event_handler = LoggingEventHandler()
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
      while True:
          time.sleep(1)
  except KeyboardInterrupt:
      observer.stop()
  observer.join()
#end

def startServeFiles():

  HandlerClass = SimpleHTTPRequestHandler
  ServerClass  = BaseHTTPServer.HTTPServer
  Protocol     = "HTTP/1.0"

  if sys.argv[1:]:
      port = int(sys.argv[1])
  else:
      port = 9000
  server_address = ('localhost', port)

  HandlerClass.protocol_version = Protocol
  httpd = ServerClass(server_address, HandlerClass)

  sa = httpd.socket.getsockname()
  print "Serving HTTP on", sa[0], "port", sa[1], "..."
  httpd.serve_forever()
#end

if __name__ == "__main__":
  watchFiles()
