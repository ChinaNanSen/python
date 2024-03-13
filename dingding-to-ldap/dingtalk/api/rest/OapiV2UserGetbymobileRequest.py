'''
Created by auto_sdk on 2022.01.17
'''
from dingtalk.api.base import RestApi
class OapiV2UserGetbymobileRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.mobile = None
		self.support_exclusive_account_search = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.v2.user.getbymobile'
