#!/usr/bin/env python

import sys
import os
from zipfile import ZipFile
import lxml.etree as ET
from StringIO import StringIO
import shutil

ns={'p': 'urn:oasis:names:tc:opendocument:xmlns:container', 'dc':'http://purl.org/dc/elements/1.1/'}

def xgettext(root, path):
  try:
    return root.xpath(path, namespaces=ns)[0].text
  except:
    return ""


def getEpubInfo(filename):
  epub = ZipFile(filename)

  meta = ET.ElementTree()
  meta.parse(StringIO(epub.read("META-INF/container.xml")))

  root = ET.ElementTree()
  rootfilename = meta.xpath("//p:rootfile/@full-path", namespaces=ns)[0]
  root.parse(StringIO(epub.read(rootfilename)))

  title = xgettext(root, "//dc:title")
  author = xgettext(root, "//dc:creator")
  publisher = xgettext(root, "//dc:publisher")
  identifier = xgettext(root, "//dc:identifier")
  language = xgettext(root, "//dc:language")

  return {'title':title, 'author':author, 'publisher':publisher, 'identifier':identifier, 'language':language}


def getList(root):
  for item in os.listdir(root):
    item = os.path.join(root, item)
    if os.path.isfile(item) and item.lower().endswith('.epub'):
      yield item.decode('utf-8')
    elif os.path.isdir(item):
      for i in getList(item):
        yield i


if __name__ == "__main__":
  source = os.path.abspath(os.path.dirname(sys.argv[0]))

  for epub in getList(source):
    try:
      info = getEpubInfo(epub)
      dest = os.path.join(source, "ePub", "%(author)s" % info, "%(author)s - %(title)s.epub" % info)
      if dest != epub:
        if not os.path.isdir(os.path.dirname(dest)):
          os.makedirs(os.path.dirname(dest))
        shutil.move(epub, dest)
    except:
      print "Error", epub
