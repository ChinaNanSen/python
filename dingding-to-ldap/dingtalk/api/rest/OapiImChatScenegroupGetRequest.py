'''
Created by auto_sdk on 2021.05.25
'''
from dingtalk.api.base import RestApi
class OapiImChatScenegroupGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.open_conversation_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.im.chat.scenegroup.get'
