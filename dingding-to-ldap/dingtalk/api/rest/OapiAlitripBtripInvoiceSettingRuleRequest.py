'''
Created by auto_sdk on 2022.08.24
'''
from dingtalk.api.base import RestApi
class OapiAlitripBtripInvoiceSettingRuleRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.request = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.alitrip.btrip.invoice.setting.rule'
