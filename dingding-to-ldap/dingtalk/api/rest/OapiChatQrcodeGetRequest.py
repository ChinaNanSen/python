'''
Created by auto_sdk on 2021.07.09
'''
from dingtalk.api.base import RestApi
class OapiChatQrcodeGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.chatid = None
		self.openConversationId = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.chat.qrcode.get'
