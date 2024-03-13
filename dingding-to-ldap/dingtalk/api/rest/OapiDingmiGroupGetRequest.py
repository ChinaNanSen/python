'''
Created by auto_sdk on 2022.12.20
'''
from dingtalk.api.base import RestApi
class OapiDingmiGroupGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.conversation_id = None
		self.date = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.dingmi.group.get'
