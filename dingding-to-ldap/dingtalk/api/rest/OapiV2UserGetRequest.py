'''
Created by auto_sdk on 2023.11.21
'''
from dingtalk.api.base import RestApi
class OapiV2UserGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.language = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.v2.user.get'
