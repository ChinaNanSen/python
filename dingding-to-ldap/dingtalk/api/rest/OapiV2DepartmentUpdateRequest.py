'''
Created by auto_sdk on 2023.08.31
'''
from dingtalk.api.base import RestApi
class OapiV2DepartmentUpdateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.auto_add_user = None
		self.auto_approve_apply = None
		self.brief = None
		self.create_dept_group = None
		self.dept_id = None
		self.dept_manager_userid_list = None
		self.dept_permits = None
		self.emp_apply_join_dept = None
		self.extension = None
		self.force_update_fields = None
		self.group_contain_hidden_dept = None
		self.group_contain_outer_dept = None
		self.group_contain_sub_dept = None
		self.hide_dept = None
		self.hide_scene_config = None
		self.language = None
		self.name = None
		self.order = None
		self.org_dept_owner = None
		self.outer_dept = None
		self.outer_dept_only_self = None
		self.outer_permit_depts = None
		self.outer_permit_users = None
		self.outer_scene_config = None
		self.parent_id = None
		self.source_identifier = None
		self.telephone = None
		self.user_permits = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.v2.department.update'
