'''
Created by auto_sdk on 2022.04.25
'''
from dingtalk.api.base import RestApi
class OapiCspaceAuditlogListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.end_date = None
		self.load_more_biz_id = None
		self.load_more_gmt_create = None
		self.page_size = None
		self.start_date = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.cspace.auditlog.list'
