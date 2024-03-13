'''
Created by auto_sdk on 2022.03.24
'''
from dingtalk.api.base import RestApi
class OapiWorkrecordAddRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.biz_id = None
		self.create_time = None
		self.formItemList = None
		self.originator_user_id = None
		self.pcUrl = None
		self.pc_open_type = None
		self.source_name = None
		self.title = None
		self.url = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.workrecord.add'
