'''
Created by auto_sdk on 2021.10.20
'''
from dingtalk.api.base import RestApi
class OapiSmartworkHrmEmployeeListdimissionRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.userid_list = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.smartwork.hrm.employee.listdimission'
