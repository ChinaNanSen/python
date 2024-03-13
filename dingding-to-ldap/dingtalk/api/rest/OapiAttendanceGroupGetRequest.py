'''
Created by auto_sdk on 2022.01.25
'''
from dingtalk.api.base import RestApi
class OapiAttendanceGroupGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.group_key = None
		self.op_userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.group.get'
