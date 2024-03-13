'''
Created by auto_sdk on 2021.04.27
'''
from dingtalk.api.base import RestApi
class OapiAttendanceGetleavestatusRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.end_time = None
		self.offset = None
		self.size = None
		self.start_time = None
		self.userid_list = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.getleavestatus'
