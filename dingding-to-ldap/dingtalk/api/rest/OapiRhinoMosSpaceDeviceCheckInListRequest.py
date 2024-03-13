'''
Created by auto_sdk on 2021.06.07
'''
from dingtalk.api.base import RestApi
class OapiRhinoMosSpaceDeviceCheckInListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.request = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.rhino.mos.space.device.check.in.list'
