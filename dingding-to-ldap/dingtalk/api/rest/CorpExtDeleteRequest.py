'''
Created by auto_sdk on 2022.04.12
'''
from dingtalk.api.base import RestApi
class CorpExtDeleteRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.corp.ext.delete'
