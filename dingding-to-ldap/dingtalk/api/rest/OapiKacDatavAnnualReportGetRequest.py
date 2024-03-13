'''
Created by auto_sdk on 2021.12.24
'''
from dingtalk.api.base import RestApi
class OapiKacDatavAnnualReportGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.dept_id = None
		self.type = None
		self.user_id = None
		self.year = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.kac.datav.annual_report.get'
