#!/usr/bin/env python

# Copyright (C) 2012 DavBfr
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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
