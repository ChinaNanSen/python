'''
Created by auto_sdk on 2021.10.12
'''
from dingtalk.api.base import RestApi
class OapiFugongProcessCodeGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.fugong.process_code.get'
