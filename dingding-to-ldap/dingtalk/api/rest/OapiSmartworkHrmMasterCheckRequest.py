'''
Created by auto_sdk on 2021.10.27
'''
from dingtalk.api.base import RestApi
class OapiSmartworkHrmMasterCheckRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.biz_uk = None
		self.entity_code = None
		self.scope_code = None
		self.tenant_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.smartwork.hrm.master.check'
