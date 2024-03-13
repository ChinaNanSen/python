'''
Created by auto_sdk on 2021.11.05
'''
from dingtalk.api.base import RestApi
class OapiEduUserGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.class_id = None
		self.role = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.user.get'
