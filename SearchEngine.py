#-*- coding:utf-8 -*-

import urllib
import os
import re
import HtmlToText
import SearchEngineLog

class SearchEngine:
	def __init__(self):
		self.lstSearchedItems 	= []
		self.lstKeywords 		= []
		self.strKeywords 		= ''
		self.iItemsEachPage 	= 10
		self.iCurrentPage       = 1
		self.strConfigFile 		= './config.ini'
		self.log 				= SearchEngineLog.SearchEngineLog()
		self.initCommand()
		self.readConfigFile()
		self.headWidth			= 80
		self.strCurrentSite		= ''
		
	def initCommand(self):
		self.cmdCommand 		= 'command'
		self.cmdKeywords 		= 'keywords'
		self.cmdQuit 			= 'q'
		self.cmdBack 			= 'b'
		self.cmdNextPage 		= 'n'
		self.cmdPrevPage 		= 'l'
		self.cmdRefresh 		= 'r'
		self.cmdSavePage 		= 's'

	def work(self):
		while True:
			self.mainSurface('')
			self.useKeywordsInput()
			
	def mainSurface(self,info):
		self.strSurface = 'MAIN_SURFACE'
		os.system('cls')
		print '=' * self.headWidth
		print ' ' * (( self.headWidth - len('SEARCH ENGINE') )/2), 'SEARCH ENGINE'
		print ' ' * (( self.headWidth - len(info) )/2), info
		print '=' * self.headWidth
		
	def searchSurface(self,info):
		self.strSurface = 'SEARCH_SURFACE'
		os.system('cls')
		print '=' * self.headWidth
		print 'The search result of :  ' , self.strKeywords
		print '-' * self.headWidth
		if len(self.lstSearchedItems) == 0:
			print 'Cannot find "%s"!' % self.strKeywords
		else :
			iCount = 0
			for item in self.lstSearchedItems:
				if item[0] > (self.iCurrentPage-1)*self.iItemsEachPage and item[0] <= self.iItemsEachPage * self.iCurrentPage:
					iCount = iCount + 1
					print '%d  %s' % (iCount,item[1])
					print '  ',item[2]
					print ''
		print '=' * self.headWidth
		print 'Current page: %d/%d' % (self.iCurrentPage,len(self.lstSearchedItems)/self.iItemsEachPage + 1)
		
	def downWebsite(self,urlpath):
		print urlpath, 'is downloading...'
		####创建存放网页内容的文件夹
		regex = r'(.*//www.)(.*)(.com|.cn|.net)'
		res = re.match(regex,urlpath)
		saveFolder = res.group(2)
		cmd = 'md ' + saveFolder
		os.system(cmd)
		textFilePath = saveFolder+ '/' +res.group(2)+'.html'
		####下载文本网页
		print 'downloading the html file...'
		webContex = ''
		try:
			ul = urllib.urlopen(urlpath)
			webContext = ul.read()
			ul.close()
		except Exception,err:
			print 'Cannot open %s,please check your network!' % urlpath
			self.log.errorLog('download website "%s" fail' % urlpath)
			exit(-1)
		try:
			file = open(textFilePath,'w')
			file.write(webContext)
			file.close()
		except Exception,err:
			print 'Create file "%s" fail!' % textFilePath
			self.log.errorLog('create file "%s" fail' % textFilePath)
		####下载图片
		print 'downloading pictures...'
		regex = r'(http:.+?\.png|http:.+?\.jpg|http:.+?\.jpeg|http:.+?\.gif|http:.+?\.bmp)'
		lstPictures = re.findall(regex,webContext)
		for picPath in lstPictures:
			regex = r'(.*)(<|>|")(.*)'
			if re.match(regex,picPath): continue
			regex = r'(.*)(/.*)'
			picName = re.match(regex,picPath)
			if picName:
				picFilePath = saveFolder + '/%s' % picName.group(2).strip(' \n\t\r')
				try:
					urllib.urlretrieve(picPath,picFilePath)
				except Exception,err:
					pass
		print 'Finished, and we saved all into the folder ', res.group(2)
		self.log.downloadLog(urlpath)
			
	def detailSurface(self,info,urlpath):
		self.strSurface = 'DETAIL_SURFACE'
		os.system('cls')
		print '=' * self.headWidth
		print ' ' * (( self.headWidth - len(urlpath) )/2), urlpath
		print '-' * self.headWidth
		print 'We opened this page using your local browser, pls use your brower view this page!'
		print 'At this page, you have these things can do.'
		print '[b] back'
		print '[s] save this page'
		print '[q] quit'
		print '=' * self.headWidth
		
	def getWebContext(self,urlpath):
		cmd = 'start ' + urlpath
		os.system(cmd)
		self.strCurrentSite = urlpath
		self.detailSurface('',urlpath)
		self.useCommandInput('')
		self.log.webLog(urlpath)
		
	def useCommandInput(self,info):
		print 'Current status:     *Command Input*'
		print info
		strWrongInfo = 'Wrong Command!'
		strCommand = raw_input('COMMAND: ').lower()
		if strCommand == self.cmdQuit: exit(0)
		elif strCommand == self.cmdBack:
			if self.strSurface == 'MAIN_SURFACE': exit(0)
			elif self.strSurface == 'DETAIL_SURFACE':
				self.searchSurface('')
			else : pass 
		elif strCommand == self.cmdKeywords:
			if self.strSurface == 'DETAIL_SURFACE':
				info = strWrongInfo
			else:
				self.useKeywordsInput()
				return
		elif strCommand == self.cmdNextPage:
			if self.strSurface != 'SEARCH_SURFACE':
				info = strWrongInfo
			else:
				if self.iCurrentPage * self.iItemsEachPage < len(self.lstSearchedItems):
					self.iCurrentPage = self.iCurrentPage + 1
					self.searchSurface('')		
		elif strCommand == self.cmdPrevPage:
			if self.strSurface != 'SEARCH_SURFACE':
				info = strWrongInfo
			else:
				if self.iCurrentPage > 1:
					self.iCurrentPage = self.iCurrentPage - 1
					self.searchSurface('')		
		elif strCommand == self.cmdRefresh:
			if self.strSurface == 'MAIN_SURFACE':
				info = strWrongInfo
			elif self.strSurface == 'SEARCH_SURFACE':
				self.startSearch()
				self.searchSurface('')
			elif self.strSurface == 'DETAIL_SURFACE':
				self.getWebContext(self.strCurrentSite)
			else : pass	
		elif strCommand == self.cmdSavePage:
			if self.strSurface != 'DETAIL_SURFACE':
				info = strWrongInfo
			else:
				self.downWebsite(self.strCurrentSite)
		elif int(strCommand) <= self.iItemsEachPage and int(strCommand) >= 1:
			iItemNum = (self.iCurrentPage - 1) * self.iItemsEachPage +  int(strCommand)
			self.getWebContext(self.lstSearchedItems[iItemNum - 1][1])
		else :
			info = strWrongInfo
		self.useCommandInput(info)
		
	def useKeywordsInput(self):
		print 'Current status:     *KeyWords Input*'
		self.strKeywords = raw_input('KEY WORDS:')
		if self.strKeywords == self.cmdCommand:
			self.useCommandInput('')
		else:
			del self.lstSearchedItems[:]
			self.divideKeywords()
			self.startSearch()
			self.searchSurface('')
			self.useKeywordsInput()
			
	def startSearch(self):
		self.iCurrentPage = 1
		self.log.searchLog(self.strKeywords)
		for url in self.lstWebsites:
			self.getAbstractContext(url)
			
	def divideKeywords(self):
		##暂时先做成的以空格区分关键字
		self.lstKeywords = self.strKeywords.split(' ')
		
	def getAbstractContext(self,urlpath):
		webLine = ''
		try:
			ul = urllib.urlopen(urlpath)
			webLine = ul.read().split('\n')
			ul.close()
		except Exception,err:
			return
		#####在一个网页只输出一个查找结果
		#####查找策略是输出匹配关键字最多的段落
		maxCount = 0
		abstractLine = ''
		#htt = HtmlToText.HtmlToText()
		#lstLines = htt.ChangeFormat(webLine)
		lstLines = webLine
		for line in lstLines:
			tempCount = 0
			for word in self.lstKeywords:
				if re.search(word.lower(),line.lower()): 
					tempCount = tempCount+1
			if tempCount > maxCount:
				maxCount = tempCount
				abstractLine = line
		if maxCount > 0:
			####若段落太长，则进行缩减
			if len(abstractLine) > self.headWidth * 4:
				for item in self.lstKeywords:
					abstractLine = abstractLine + '...' + item + '...'
			temp = (len(self.lstSearchedItems) + 1,urlpath,abstractLine.strip(' \t\n\r'))
			self.lstSearchedItems.append(temp)
		
	def loadKeywordsforRegex(self):
		strTemp = r''
		for index in range(0,len(self.lstKeywords)-1):
			strTemp = strTemp + self.lstKeywords[index] + '|'
		strTemp = strTemp + self.lstKeywords[len(self.lstKeywords)-1]
		self.strRegex = re.compile(strTemp)
		pass
		
	def readConfigFile(self):
		self.lstWebsites 	= []
		try:
			file = open('./config.ini')
			self.lstWebsites = file.read().split('\n')
			file.close()
		except Exception,err:
			print 'Open config.ini failed! You should create file "config.ini" at first!'
			self.log.errorLog('Open config.ini failed')
			exit(-1)
		for index in range(0,len(self.lstWebsites)):
			self.lstWebsites[index] = self.lstWebsites[index].strip(' \t')
		nonWebsiteStrCount = self.lstWebsites.count('')
		while nonWebsiteStrCount != 0:
			self.lstWebsites.remove('')
			nonWebsiteStrCount = nonWebsiteStrCount - 1
		
if __name__ == '__main__':
	se = SearchEngine()
	se.work()