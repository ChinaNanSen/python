'''
Created by auto_sdk on 2021.04.27
'''
from dingtalk.api.base import RestApi
class OapiAlitripBtripInvoiceSearchRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.rq = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.alitrip.btrip.invoice.search'
