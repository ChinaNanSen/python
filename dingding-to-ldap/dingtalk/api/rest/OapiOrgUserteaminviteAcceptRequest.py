'''
Created by auto_sdk on 2022.05.10
'''
from dingtalk.api.base import RestApi
class OapiOrgUserteaminviteAcceptRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.mobile = None
		self.state_code = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.org.userteaminvite.accept'
