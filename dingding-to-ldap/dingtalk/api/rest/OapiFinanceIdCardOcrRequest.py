'''
Created by auto_sdk on 2022.04.28
'''
from dingtalk.api.base import RestApi
class OapiFinanceIdCardOcrRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.back_picture_url = None
		self.front_picture_url = None
		self.id_card_no = None
		self.request_id = None
		self.user_mobile = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.finance.IdCard.ocr'
