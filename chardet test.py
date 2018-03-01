# -*- coding: utf-8 -*-  
import chardet  
import urllib2
import sys
req = urllib2.Request("http://www.163.com/")
content = urllib2.urlopen(req).read()
typeEncode = sys.getfilesystemencoding()
infoencode = chardet.detect(content).get('encoding','utf-8')
html = content.decode(infoencode,'ignore').encode(typeEncode)
print html
