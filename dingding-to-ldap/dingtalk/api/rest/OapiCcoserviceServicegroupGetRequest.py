'''
Created by auto_sdk on 2020.01.08
'''
from dingtalk.api.base import RestApi
class OapiCcoserviceServicegroupGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.open_group_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.ccoservice.servicegroup.get'
