'''
Created by auto_sdk on 2023.03.03
'''
from dingtalk.api.base import RestApi
class OapiImChatScenegroupMemberGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.cursor = None
		self.open_conversation_id = None
		self.size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.im.chat.scenegroup.member.get'
