'''
Created by auto_sdk on 2021.01.20
'''
from dingtalk.api.base import RestApi
class OapiWorkspaceTaskCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.microapp_agent_id = None
		self.operator_userid = None
		self.task = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.workspace.task.create'
