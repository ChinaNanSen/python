'''
Created by auto_sdk on 2022.04.19
'''
from dingtalk.api.base import RestApi
class OapiAtsJobBatchaddRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.biz_code = None
		self.jobs = None
		self.op_user_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.ats.job.batchadd'
