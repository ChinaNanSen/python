'''
Created by auto_sdk on 2021.10.20
'''
from dingtalk.api.base import RestApi
class OapiFinanceAlipayAccountGetbyuidRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.finance.alipay.account.getbyuid'
