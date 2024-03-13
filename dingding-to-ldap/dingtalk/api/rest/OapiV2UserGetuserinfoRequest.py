'''
Created by auto_sdk on 2022.04.11
'''
from dingtalk.api.base import RestApi
class OapiV2UserGetuserinfoRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.code = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.v2.user.getuserinfo'
