'''
Created by auto_sdk on 2021.05.27
'''
from dingtalk.api.base import RestApi
class OapiEduCourseJoinRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.course_code = None
		self.join_role = None
		self.op_user_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.course.join'
