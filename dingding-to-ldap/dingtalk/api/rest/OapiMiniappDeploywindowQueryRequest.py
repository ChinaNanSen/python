'''
Created by auto_sdk on 2023.01.30
'''
from dingtalk.api.base import RestApi
class OapiMiniappDeploywindowQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.model_key = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.miniapp.deploywindow.query'
