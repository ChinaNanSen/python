'''
Created by auto_sdk on 2021.09.22
'''
from dingtalk.api.base import RestApi
class OapiImChatScenegroupUpdateRequest(RestApi):
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
		self.open_conversation_id = None
		self.owner_user_id = None
		self.plugin_customize_verify = None
		self.searchable = None
		self.show_history_type = None
		self.title = None
		self.validation_type = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.im.chat.scenegroup.update'
