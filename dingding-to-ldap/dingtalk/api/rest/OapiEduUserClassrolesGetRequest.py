'''
Created by auto_sdk on 2022.07.06
'''
from dingtalk.api.base import RestApi
class OapiEduUserClassrolesGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.request = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.user.classroles.get'
