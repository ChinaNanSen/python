'''
Created by auto_sdk on 2021.05.31
'''
from dingtalk.api.base import RestApi
class OapiEduClassCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.open_class = None
		self.operator = None
		self.super_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.class.create'
