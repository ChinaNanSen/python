'''
Created by auto_sdk on 2023.06.09
'''
from dingtalk.api.base import RestApi
class OapiRobotMessageSendotoRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.chatbot_id = None
		self.msg_key = None
		self.msg_param = None
		self.staff_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.robot.message.sendoto'
