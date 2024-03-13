'''
Created by auto_sdk on 2021.10.12
'''
from dingtalk.api.base import RestApi
class OapiAppstoreGoodsQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.goods_code = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.appstore.goods.query'
