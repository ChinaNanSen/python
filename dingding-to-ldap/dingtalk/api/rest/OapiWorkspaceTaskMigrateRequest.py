'''
Created by auto_sdk on 2022.01.19
'''
from dingtalk.api.base import RestApi
class OapiWorkspaceTaskMigrateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.agentid = None
		self.operator_userid = None
		self.task = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.workspace.task.migrate'
