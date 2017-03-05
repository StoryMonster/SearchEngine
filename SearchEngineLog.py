#-*- coding:utf-8 -*-

import os
import time

class SearchEngineLog:
	def __init__(self):
		self.strLogFile   = 'SearchEngine.log'
		self.iMaxLogItems = 100
		self.iCurrentItems= self.getCurrentLogItemsCount()
		self.createLogFile()

	def searchLog(self,strKeywords):
		self.writeLog('SEARCH',strKeywords)
		
	def	webLog(self,webPath):
		self.writeLog('SCANWEB',webPath)
		
	def	errorLog(self,errInfo):
		self.writeLog('ERROR',errInfo)
		
	def downloadLog(self, info):
		self.writeLog('DOWNLOAD',info)
		
	def writeLog(self,type,info):
		if self.iCurrentItems >= self.iMaxLogItems:
			self.clearLogFile()
		self.iCurrentItems = self.iCurrentItems + 1
		file = open(self.strLogFile,'a')
		str = '%-4d %-22s %-10s %s\n' % (self.iCurrentItems, self.getCurrTime(), type, info)
		file.write(str)
		file.close()
		
	def	createLogFile(self):
		if os.path.exists(self.strLogFile): return False
		file = open(self.strLogFile,'a')
		file.close()
		return True
		
	def	clearLogFile(self):
		if not os.path.exists(self.strLogFile): return
		file = open(self.strLogFile,'w')
		file.close()
		self.iCurrentItems = 0
		
	def	getCurrTime(self):
		return time.strftime('%Y-%m-%d %X', time.localtime())
		
	def	setMaxLogItemNum(self,num):
		self.iMaxLogItems = num
		
	def	getMaxLogItemNum(self,num):
		return self.iMaxLogItems
		
	def getCurrentLogItemsCount(self):
		if not os.path.exists(self.strLogFile): return 0 
		res = 0
		file = open(self.strLogFile)
		while file.readline():
			res = res + 1
		file.close()
		return res
		
if __name__ == '__main__':
	sel = SearchEngineLog()
	for index in range(0,10):
		sel.searchLog('zhangfei guanyu')
		sel.webLog('www.baidu.com')
		sel.errorLog('open fail')
	