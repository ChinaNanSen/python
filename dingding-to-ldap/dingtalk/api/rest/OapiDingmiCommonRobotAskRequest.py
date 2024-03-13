'''
Created by auto_sdk on 2022.12.20
'''
from dingtalk.api.base import RestApi
class OapiDingmiCommonRobotAskRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.question = None
		self.robot_app_key = None
		self.session_uuid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.dingmi.common.robot.ask'
