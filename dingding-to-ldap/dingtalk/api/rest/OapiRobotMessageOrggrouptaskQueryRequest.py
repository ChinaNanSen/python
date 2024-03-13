'''
Created by auto_sdk on 2023.06.26
'''
from dingtalk.api.base import RestApi
class OapiRobotMessageOrggrouptaskQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.chatbot_id = None
		self.cursor = None
		self.open_conversation_id = None
		self.page_size = None
		self.process_query_key = None
		self.token = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.robot.message.orggrouptask.query'
