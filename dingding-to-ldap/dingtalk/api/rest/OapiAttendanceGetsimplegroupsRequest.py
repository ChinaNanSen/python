'''
Created by auto_sdk on 2023.11.07
'''
from dingtalk.api.base import RestApi
class OapiAttendanceGetsimplegroupsRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.offset = None
		self.size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.getsimplegroups'
