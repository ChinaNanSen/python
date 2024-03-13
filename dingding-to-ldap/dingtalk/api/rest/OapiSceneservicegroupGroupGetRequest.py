'''
Created by auto_sdk on 2021.09.08
'''
from dingtalk.api.base import RestApi
class OapiSceneservicegroupGroupGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.open_conversationid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.sceneservicegroup.group.get'
