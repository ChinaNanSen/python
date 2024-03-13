'''
Created by auto_sdk on 2021.05.08
'''
from dingtalk.api.base import RestApi
class OapiDingpayRedenvelopeSendRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.chat_id = None
		self.corp_biz_no = None
		self.ext_params = None
		self.greetings = None
		self.open_conversation_id = None
		self.pay_method = None
		self.pay_sign = None
		self.receiver_id = None
		self.sender_id = None
		self.theme_id = None
		self.total_amount = None
		self.type = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.dingpay.redenvelope.send'
