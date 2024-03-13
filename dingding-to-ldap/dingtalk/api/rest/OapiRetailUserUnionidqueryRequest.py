'''
Created by auto_sdk on 2021.05.20
'''
from dingtalk.api.base import RestApi
class OapiRetailUserUnionidqueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.channel = None
		self.outer_id = None
		self.sub_outer_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.retail.user.unionidquery'
