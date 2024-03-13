'''
Created by auto_sdk on 2021.10.29
'''
from dingtalk.api.base import RestApi
class OapiProcessSaveRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.saveProcessRequest = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.process.save'
