'''
Created by auto_sdk on 2022.09.27
'''
from dingtalk.api.base import RestApi
class OapiProcessinstanceListidsRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.cursor = None
		self.end_time = None
		self.process_code = None
		self.size = None
		self.start_time = None
		self.userid_list = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.processinstance.listids'
