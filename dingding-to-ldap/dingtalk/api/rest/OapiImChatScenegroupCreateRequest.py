'''
Created by auto_sdk on 2023.02.26
'''
from dingtalk.api.base import RestApi
class OapiImChatScenegroupCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.add_friend_forbidden = None
		self.all_members_can_create_calendar = None
		self.all_members_can_create_mcs_conf = None
		self.chat_banned_type = None
		self.group_email_disabled = None
		self.group_live_switch = None
		self.icon = None
		self.management_type = None
		self.members_to_admin_chat = None
		self.mention_all_authority = None
		self.only_admin_can_ding = None
		self.only_admin_can_set_msg_top = None
		self.owner_user_id = None
		self.searchable = None
		self.show_history_type = None
		self.subadmin_ids = None
		self.template_id = None
		self.title = None
		self.user_ids = None
		self.uuid = None
		self.validation_type = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.im.chat.scenegroup.create'
