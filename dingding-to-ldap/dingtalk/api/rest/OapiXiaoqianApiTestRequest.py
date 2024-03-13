'''
Created by auto_sdk on 2022.03.10
'''
from dingtalk.api.base import RestApi
class OapiXiaoqianApiTestRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.xiaoqian.api.test'
