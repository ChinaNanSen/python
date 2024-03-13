'''
Created by auto_sdk on 2022.12.13
'''
from dingtalk.api.base import RestApi
class OapiAttendanceShiftAddRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.op_user_id = None
		self.shift = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.shift.add'
