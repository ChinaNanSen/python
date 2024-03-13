'''
Created by auto_sdk on 2022.07.20
'''
from dingtalk.api.base import RestApi
class OapiRobotMessageOtotaskQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.chatbot_id = None
		self.process_query_key = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.robot.message.ototask.query'
