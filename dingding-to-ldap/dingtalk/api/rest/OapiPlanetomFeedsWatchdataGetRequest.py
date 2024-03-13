'''
Created by auto_sdk on 2021.05.27
'''
from dingtalk.api.base import RestApi
class OapiPlanetomFeedsWatchdataGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.anchor_id = None
		self.chat_id = None
		self.feed_id = None
		self.index = None
		self.page_size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.planetom.feeds.watchdata.get'
