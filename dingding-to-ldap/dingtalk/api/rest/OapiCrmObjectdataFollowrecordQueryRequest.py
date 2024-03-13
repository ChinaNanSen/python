'''
Created by auto_sdk on 2022.04.12
'''
from dingtalk.api.base import RestApi
class OapiCrmObjectdataFollowrecordQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.current_operator_userid = None
		self.cursor = None
		self.page_size = None
		self.query_dsl = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.crm.objectdata.followrecord.query'
