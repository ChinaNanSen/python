'''
Created by auto_sdk on 2022.12.30
'''
from dingtalk.api.base import RestApi
class OapiDingmiCommonO2oPushRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.chatbot_id = None
		self.msg_key = None
		self.msg_param = None
		self.staff_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.dingmi.common.o2o.push'
