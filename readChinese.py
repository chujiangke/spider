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
from getdata import *

listHighFrequency = []
def readHighFrequencyChinese( fileName):
	global listHighFrequency
	typeEncode = sys.getfilesystemencoding()
	fo = open( fileName,"r")
	for line in fo.readlines(10000):
		#print "line"
		#print line
		line=line.decode('utf-8').encode(typeEncode)
		#print "after decode"
		#print line
		linesplit = line.strip().split()
		listHighFrequency.extend(linesplit)
	fo.close()
	return listHighFrequency
def DetermineToPickHtml( strHtml ,fileName):
	global listHighFrequency
	if len(listHighFrequency) == 0:
		readHighFrequencyChinese(fileName)
	for HighFrequencyWord in listHighFrequency:
		if HighFrequencyWord in strHtml:
			return True
	return False
if __name__=='__main__':
	strHtml = getHtml("http://baby.163.com/photoview/6RJC0036/2097781.html");
	#print strHtml
	determineResult=DetermineToPickHtml(strHtml,"chinese.txt")
	print "================================================="
	print listHighFrequency
	print listHighFrequency[0]
	print listHighFrequency[5]
	print("determineResult->%d"%(determineResult) )