'''
Created by auto_sdk on 2023.02.20
'''
from dingtalk.api.base import RestApi
class OapiBlackboardListtoptenRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.categoryId = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.blackboard.listtopten'
