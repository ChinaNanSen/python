'''
Created by auto_sdk on 2021.05.27
'''
from dingtalk.api.base import RestApi
class OapiEduCourseBatchcreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.course_infos = None
		self.op_userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.course.batchcreate'
