'''
Created by auto_sdk on 2023.11.29
'''
from dingtalk.api.base import RestApi
class OapiProcessBaseinfoListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.process_codes = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.process.baseinfo.list'
