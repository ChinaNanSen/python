'''
Created by auto_sdk on 2023.07.14
'''
from dingtalk.api.base import RestApi
class OapiRhinoMosExecClothesUnperformedFilterRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.req = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.rhino.mos.exec.clothes.unperformed.filter'
