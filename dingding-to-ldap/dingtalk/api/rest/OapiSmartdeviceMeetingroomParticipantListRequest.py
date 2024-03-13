'''
Created by auto_sdk on 2021.08.03
'''
from dingtalk.api.base import RestApi
class OapiSmartdeviceMeetingroomParticipantListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.bookid = None
		self.cursor = None
		self.size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.smartdevice.meetingroom.participant.list'
