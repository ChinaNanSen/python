'''
Created by auto_sdk on 2021.05.20
'''
from dingtalk.api.base import RestApi
class OapiMedalCorpmedalQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.template_ids = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.medal.corpmedal.query'
