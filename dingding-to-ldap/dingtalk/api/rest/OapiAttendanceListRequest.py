'''
Created by auto_sdk on 2022.06.16
'''
from dingtalk.api.base import RestApi
class OapiAttendanceListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.isI18n = None
		self.limit = None
		self.offset = None
		self.userIdList = None
		self.workDateFrom = None
		self.workDateTo = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.list'
