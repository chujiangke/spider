
# -*- coding: utf-8 -*-  
import re  
import os  
import urllib2  
import string
import urllib2  
import os
import sys
import chardet  
from HTMLParser import HTMLParser  
from readChinese import *
import threading  

def getHtml(url):  
    from urllib2 import HTTPError  
    try:
      html=""  
      page = urllib2.urlopen(url,timeout = 10)  
      html = page.read();
      typeEncode = sys.getfilesystemencoding()
      infoencode = chardet.detect(html).get('encoding','utf-8')
      infoconfidence = chardet.detect(html).get('confidence') 
      #print type(infoconfidence)
      print chardet.detect(html)
      if infoconfidence != 0.99 :		#预防乱码 只取0.99识别率的
      	return ""
      html = html.decode(infoencode,'ignore').encode(typeEncode)
    except Exception as err:   
    	print "getHtml err"
    	print(err)
    finally:
    	return html
def getUrlFromHtml( str_html ):
	listUrl = []
	str_html=str_html.replace(" ","")
	urls=re.findall(r"<a.*?href=.*?<\/a>",str_html,re.I) #<a href="http://money.163.com/">财经</a></h2>
	for url in urls:
	 #print ("getUrlFromHtml -> %s " %(url) )
	 removeTagList=['jpg','apk','download','img','gif','js']
	 for tag in removeTagList:
	 	if tag in url:
	 		pass
	 pos_start=url.find("http:")
	 if pos_start == -1:
	 	pass
	 else:
	 	pos_end = url.find("\"", pos_start)
	 	if pos_end == -1:
	 		pass
	 	else:
	 		url = url[pos_start:pos_end]
	 		#print url
	 		if len(url)<=0:
	 			pass
	 			'''
			#only get tieba data
			if "http://tieba.baidu.com"  in url:		#只抓取贴吧内容。
				print("tieba: %s" %(url) )
				listUrl.append( url)
				#print 'this is over'
				'''
			else:
			
				#print("url: %s" %(url) )
				listUrl.append( url)
	return listUrl

class MyHTMLParser(HTMLParser):  
  
    def __init__(self):  
        HTMLParser.__init__(self)  
        self.data = []  
  
    def get_data(self):  
        return self.data  
  
    def handle_data(self, data):  
    	#print "====="+data
    	#print "-----"+self.lasttag
    	list_tag = ['div','li','ul','a','img','i','b','p','font','span','td','th','title']
    	#list_tag = ['br','p','a']
        if self.lasttag in list_tag:  
            if data != None and len(data.strip()) > 0:
            	#print "-----"+self.lasttag
            	#print "====="+data
                s = data.strip()  
                self.data.append(s)
def getTextFromHtml( str_html ):
	try:
		htmlParser = MyHTMLParser()
		htmlParser.feed(str_html)
		htmlParser.close()
		return htmlParser.get_data()
	except Exception as err:
		print "getTextFromHtml"
		print(err)
		return ""
	'''
	for line in htmlParser.get_data():
		print line
	'''
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return size
    except Exception as err:
    	print "getDocSize error"
        print(err)


def writeTextToFile( strFilePath, list_text ):
	fo = open(strFilePath, "a+")
	lines = fo.readlines();
	lines_set = set([line.strip() for line in lines])
	new_line_set = set(list_text)
	add_line_set = new_line_set - lines_set
	list_text = list(add_line_set)
	for i in xrange( len( list_text )):
		fo.write( list_text[i] )
		fo.write( "\n" )
	fo.close()


urlAddressPool = set()
def determineAddToUrl( store_url, list_url ):
	global urlAddressPool
	for url_temp in list_url:
		if url_temp in urlAddressPool:
			pass
		else:
			urlAddressPool.add(url_temp)
			store_url.append(url_temp)
			#print store_url


store_url  = [];
store_text = [];
fileSize = 5*1024*1024*1024
filePath = "text.txt"
def firstStartReptiles():
	global store_url
	global store_text
	global fileSize
	global filePath
	html = getHtml("http://www.163.com/");
	#html = getHtml("https://tieba.baidu.com/p/5145295063");
	list_url = getUrlFromHtml(html)
	list_text = getTextFromHtml(html)
	store_text.extend( list_text );
	determineAddToUrl( store_url, list_url )
	writeTextToFile(filePath,store_text)
	#print store_url
	#print store_text

mylock = threading.RLock()
myThreadGetHtmlTextlock = threading.RLock()  
taskNumber = 100
myThreadtaskNumberlock = threading.RLock()  
class myThreadGetHtmlText( threading.Thread ):
	def __init__(self,url):  
		threading.Thread.__init__(self)
		self.url = url
	def run(self):
		global store_text
		global store_url
		global taskNumber
		global filePath
		html=getHtml(self.url)
		print("1 get url -> %s html over" %(self.url) )
		if False == DetermineToPickHtml( html ,"chinese.txt"):
			print "throw html ,determine false"
			pass
		list_url = getUrlFromHtml(html)
		print("2 get list_url over")

		myThreadGetHtmlTextlock.acquire()
		determineAddToUrl( store_url, list_url )
		myThreadGetHtmlTextlock.release()

		print("3 add to store_url over")
		list_text = getTextFromHtml(html)
		print("4 get list_text over")

		myThreadGetHtmlTextlock.acquire()
		writeTextToFile(filePath,list_text)
		myThreadGetHtmlTextlock.release()
		print("5 add to store_text over")



if __name__ == '__main__':
	firstStartReptiles()
	while True:
		tsk = []
		for task in xrange(taskNumber): 
			myThreadGetHtmlTextlock.acquire()
			url = store_url.pop(0);
			myThreadGetHtmlTextlock.release()

			print("0 pop url -> %s over" %(url) )
			threadGetHtml = myThreadGetHtmlText(url)
			threadGetHtml.start()
			tsk.append(threadGetHtml)

		for tt in tsk:
			tt.join(10)		

	#getDocSize(filePath ) > fileSize:	

	print ("=========================================")
	print ("store_url size: %d" %( len( store_url ) ) )
	print ("urlAddressPool size: %d"%(len(urlAddressPool)))
	
	print "loop"
	print ("=========================================")
