'''
Created by auto_sdk on 2021.11.22
'''
from dingtalk.api.base import RestApi
class OapiCrmObjectmetaCustomerDescribeRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.crm.objectmeta.customer.describe'
