'''
Created by auto_sdk on 2022.04.12
'''
from dingtalk.api.base import RestApi
class OapiGettokenRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.appkey = None
		self.appsecret = None
		self.corpid = None
		self.corpsecret = None

	def getHttpMethod(self):
		return 'GET'

	def getapiname(self):
		return 'dingtalk.oapi.gettoken'
