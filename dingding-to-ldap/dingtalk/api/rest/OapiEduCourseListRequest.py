'''
Created by auto_sdk on 2021.06.10
'''
from dingtalk.api.base import RestApi
class OapiEduCourseListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.course_codes = None
		self.cursor = None
		self.end_time = None
		self.name = None
		self.op_userid = None
		self.option = None
		self.participant_condition = None
		self.scene = None
		self.size = None
		self.start_time = None
		self.statuses = None
		self.suite_keys = None
		self.teacher_conditions = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.course.list'
