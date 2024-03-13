'''
Created by auto_sdk on 2021.12.14
'''
from dingtalk.api.base import RestApi
class OapiProcessTemplateManageGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.app_uuid = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.process.template.manage.get'
