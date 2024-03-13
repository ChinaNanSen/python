'''
Created by auto_sdk on 2023.03.16
'''
from dingtalk.api.base import RestApi
class OapiV2UserCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.avatarMediaId = None
		self.dept_id_list = None
		self.dept_order_list = None
		self.dept_position_list = None
		self.dept_title_list = None
		self.email = None
		self.exclusive_account = None
		self.exclusive_account_type = None
		self.exclusive_mobile = None
		self.exclusive_mobile_verify_status = None
		self.ext_attrs = None
		self.ext_attrs_update_mode = None
		self.extension = None
		self.gender = None
		self.hide_mobile = None
		self.hired_date = None
		self.init_password = None
		self.job_number = None
		self.login_email = None
		self.login_id = None
		self.manager_userid = None
		self.mobile = None
		self.name = None
		self.nickname = None
		self.org_email = None
		self.org_email_type = None
		self.outer_exclusive_corpid = None
		self.outer_exclusive_userid = None
		self.remark = None
		self.senior_mode = None
		self.telephone = None
		self.title = None
		self.userid = None
		self.work_place = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.v2.user.create'
