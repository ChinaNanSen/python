'''
Created by auto_sdk on 2021.06.07
'''
from dingtalk.api.base import RestApi
class OapiWorkbenchShortcutGetguideuriRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.app_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.workbench.shortcut.getguideuri'
