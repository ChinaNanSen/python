'''
Created by auto_sdk on 2021.08.26
'''
from dingtalk.api.base import RestApi
class OapiAttendanceScheduleResultListbyidsRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.op_user_id = None
		self.schedule_ids = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.schedule.result.listbyids'
