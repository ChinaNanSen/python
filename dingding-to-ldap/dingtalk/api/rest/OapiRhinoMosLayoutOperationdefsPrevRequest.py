'''
Created by auto_sdk on 2022.08.10
'''
from dingtalk.api.base import RestApi
class OapiRhinoMosLayoutOperationdefsPrevRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.flow_version = None
		self.need_assign_info = None
		self.operation_external_id = None
		self.operation_uid = None
		self.order_id = None
		self.tenant_id = None
		self.tmp_save = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.rhino.mos.layout.operationdefs.prev'
