'''
Created by auto_sdk on 2021.04.25
'''
from dingtalk.api.base import RestApi
class OapiAttendanceVacationRecordListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.leave_code = None
		self.offset = None
		self.op_userid = None
		self.size = None
		self.userids = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.vacation.record.list'
