'''
Created by auto_sdk on 2021.11.26
'''
from dingtalk.api.base import RestApi
class OapiAttendanceShiftQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.op_user_id = None
		self.shift_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.shift.query'
