'''
Created by auto_sdk on 2023.08.07
'''
from dingtalk.api.base import RestApi
class OapiAttendanceRecordUploadRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.device_id = None
		self.device_name = None
		self.photo_url = None
		self.user_check_time = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.record.upload'
