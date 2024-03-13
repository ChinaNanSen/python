'''
Created by auto_sdk on 2018.04.20
'''
from top.api.base import RestApi
class DingtalkOapiLingjiuTestRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return '21d8pajl08.dingtalk.oapi.lingjiu.test'
