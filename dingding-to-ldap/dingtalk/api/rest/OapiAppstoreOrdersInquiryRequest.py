'''
Created by auto_sdk on 2021.10.12
'''
from dingtalk.api.base import RestApi
class OapiAppstoreOrdersInquiryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.corpid = None
		self.cyc_num = None
		self.cyc_unit = None
		self.goods_code = None
		self.item_code = None
		self.mobile = None
		self.quantity = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.appstore.orders.inquiry'
