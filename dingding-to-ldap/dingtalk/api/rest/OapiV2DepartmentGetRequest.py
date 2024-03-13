'''
Created by auto_sdk on 2023.08.31
'''
from dingtalk.api.base import RestApi
class OapiV2DepartmentGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.dept_id = None
		self.language = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.v2.department.get'
