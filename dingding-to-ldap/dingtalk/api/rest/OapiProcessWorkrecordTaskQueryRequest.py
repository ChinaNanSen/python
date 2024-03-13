'''
Created by auto_sdk on 2023.05.08
'''
from dingtalk.api.base import RestApi
class OapiProcessWorkrecordTaskQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.count = None
		self.offset = None
		self.status = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.process.workrecord.task.query'
