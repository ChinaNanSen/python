'''
Created by auto_sdk on 2022.01.18
'''
from dingtalk.api.base import RestApi
class OapiAlitripBtripFlightOrderSearchRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.rq = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.alitrip.btrip.flight.order.search'
