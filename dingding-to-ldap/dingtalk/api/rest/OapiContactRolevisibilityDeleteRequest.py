'''
Created by auto_sdk on 2021.12.06
'''
from dingtalk.api.base import RestApi
class OapiContactRolevisibilityDeleteRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.role_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.contact.rolevisibility.delete'
