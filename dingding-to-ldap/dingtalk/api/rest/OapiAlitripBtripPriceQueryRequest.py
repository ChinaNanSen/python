'''
Created by auto_sdk on 2021.08.16
'''
from dingtalk.api.base import RestApi
class OapiAlitripBtripPriceQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.req = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.alitrip.btrip.price.query'
