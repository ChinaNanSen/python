'''
Created by auto_sdk on 2019.09.04
'''
from top.api.base import RestApi
class DingtalkOapiIsvLingjiuTestRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return '21d8pajl08.dingtalk.oapi.isv.lingjiu.test'
