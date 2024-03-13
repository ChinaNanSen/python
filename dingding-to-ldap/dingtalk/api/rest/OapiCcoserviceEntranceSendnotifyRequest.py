'''
Created by auto_sdk on 2019.07.01
'''
from dingtalk.api.base import RestApi
class OapiCcoserviceEntranceSendnotifyRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.app_id = None
		self.content = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.ccoservice.entrance.sendnotify'
