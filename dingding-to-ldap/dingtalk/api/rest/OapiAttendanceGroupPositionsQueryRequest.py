'''
Created by auto_sdk on 2021.09.24
'''
from dingtalk.api.base import RestApi
class OapiAttendanceGroupPositionsQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.cursor = None
		self.group_key = None
		self.op_userid = None
		self.size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.group.positions.query'
