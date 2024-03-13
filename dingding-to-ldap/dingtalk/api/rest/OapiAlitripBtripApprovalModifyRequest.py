'''
Created by auto_sdk on 2021.11.03
'''
from dingtalk.api.base import RestApi
class OapiAlitripBtripApprovalModifyRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.rq = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.alitrip.btrip.approval.modify'
