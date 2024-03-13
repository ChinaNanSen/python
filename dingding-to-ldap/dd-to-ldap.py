import configparser
from typing import Tuple
import xpinyin
import dingtalk.api
from alibabacloud_dingtalk.oauth2_1_0.client import Client as DingTalkClient
# from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.oauth2_1_0 import models as dingtalk_oauth_models
from alibabacloud_dingtalk.hrm_1_0.client import Client as dingtalkhrm_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.hrm_1_0 import models as dingtalkhrm__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES, MODIFY_REPLACE


class Config:
    def __init__(self, config_path: str) -> None:
        self._config_path = config_path

        self.config = configparser.ConfigParser()
        self.config.read(self._config_path)

    def get_ak_sk(self, section: str) -> Tuple[str, str]:
        """
        获取钉钉ak，sk
        :return:
        """
        app_key = self.config.get(section, 'app_key')
        app_secret = self.config.get(section, 'app_secret')
        return app_key, app_secret


class DingTalk:
    BASE_URL = "https://oapi.dingtalk.com"

    def __init__(self, _ak, _sk):
        self._ak = _ak
        self._sk = _sk
        self._access_token = self._get_access_token()
        self._dismission_staff = []

    @staticmethod
    def _create_client() -> DingTalkClient:
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return DingTalkClient(config)

    @staticmethod
    def _create_hrm_client() -> dingtalkhrm_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkhrm_1_0Client(config)

    def _get_access_token(self) -> str:
        client = self._create_client()
        request = dingtalk_oauth_models.GetAccessTokenRequest(
            app_key=self._ak,
            app_secret=self._sk
        )
        try:
            response = client.get_access_token(request)
            return response.body.access_token
        except Exception as err:
            print(f"Error getting access token: {err}")
            return ""

    def _api_call(self, api_request, method, dept_id=None, cursor=1, size=50):
        req = (getattr(dingtalk.api, api_request)
               (f"{self.BASE_URL}/{method}"))
        if dept_id is not None:
            req.dept_id = dept_id
        req.cursor = cursor
        req.size = size
        try:
            return req.getResponse(self._access_token)
        except Exception as e:
            print(e)
            return None

    def get_department_info(self, dept_id=1):
        response = self._api_call("OapiV2DepartmentGetRequest", "topapi/v2/department/get", dept_id)
        return response['result'] if response else None

    def get_sub_department_list(self, dept_id=None):
        """
        不传dept_id获取顶级子部门
        :param dept_id:
        :return:
        """
        response = self._api_call("OapiV2DepartmentListsubRequest", "topapi/v2/department/listsub", dept_id)
        return response['result'] if response else None

    def get_department_userid_list(self, dept_id) -> list:
        """
        获取部门用户userid列表
        :param dept_id:
        :return:
        """
        response = self._api_call("OapiUserListidRequest", "topapi/user/listid", dept_id)
        return response['result']['userid_list'] if response else None

    def get_department_user_parent_list(self, userid):
        """
        根据user id 获取所有父部门
        :param userid:
        :return:
        """
        req = dingtalk.api.OapiV2DepartmentListparentbyuserRequest(
            "https://oapi.dingtalk.com/topapi/v2/department/listparentbyuser")
        req.userid = userid
        try:
            resp = req.getResponse(self._access_token)
            return resp['result']['parent_list'][-1]['parent_dept_id_list']
        except Exception as e:
            print(e)

    def get_user_info(self, user_id) -> dict:
        """
        获取用户信息
        :param user_id:
        :return:
        """
        req = dingtalk.api.OapiV2UserGetRequest("https://oapi.dingtalk.com/topapi/v2/user/get")
        req.userid = user_id
        try:
            resp = req.getResponse(self._access_token)
            return resp['result']
        except Exception as e:
            print(e)

    def _get_dismission_staff(self, dismission_staff, next_token=0) -> None:
        """
        获取离职员工列表
        :return:
        """
        client = self._create_hrm_client()
        query_dismission_staff_id_list_headers = dingtalkhrm__1__0_models.QueryDismissionStaffIdListHeaders()
        query_dismission_staff_id_list_headers.x_acs_dingtalk_access_token = self._access_token
        query_dismission_staff_id_list_request = dingtalkhrm__1__0_models.QueryDismissionStaffIdListRequest(
            next_token=next_token,
            max_results=50
        )
        try:
            res = client.query_dismission_staff_id_list_with_options(query_dismission_staff_id_list_request, query_dismission_staff_id_list_headers, util_models.RuntimeOptions())
            dismission_staff += res.body.user_id_list
            res_next_token = res.body.next_token
            if not res_next_token:
                return
            self._get_dismission_staff(dismission_staff, res_next_token)
        except Exception as err:
                print(err)


class DeptUser(DingTalk):
    def __init__(self, _ak, _sk):
        super().__init__(_ak, _sk)

    @staticmethod
    def _pinyin(name):
        """
        默认用-连接拼音，所以我们在后面加上了
        :param name:
        :return:
        """
        s = xpinyin.Pinyin()
        return s.get_pinyin(name, '')

    def _department_user(self, dept_id) -> list:
        """
        获取该部门下所有用户信息
        :param dept_id:
        :return: 返回该部门下用户信息
        """
        department_userid_list = self.get_department_userid_list(dept_id)
        department_user = []
        for userid in department_userid_list:
            user_info = self.get_user_info(userid)
            # print(user_info)
            user_name = user_info['name']
            user_dict = {
                'uid': user_info['userid'],
                'user_name': user_name,
                'mobile': user_info['mobile'],
                'user_name_pinyin': self._pinyin(user_name)
            }
            department_user.append(user_dict)
        return department_user

    def get_top_departments(self, all_user) -> str:
        department_info = self.get_department_info(dept_id=1)
        department_name = department_info['name']
        users = self._department_user(dept_id=1)
        for user in users:
            # print(department_name+'/'+user['user_name'])
            all_user.append([department_name, user])
        return department_name

    def generate_department_hierarchy(self, department_list):
        if not department_list:
            return []

        department_hierarchy = []

        for department_info in department_list:
            department_name = department_info['name']
            department_id = department_info['dept_id']
            users = self._department_user(department_id)
            sub_department_list = self.get_sub_department_list(department_id)
            sub_department_hierarchy = self.generate_department_hierarchy(sub_department_list)
            department_hierarchy.append([department_name, users] + sub_department_hierarchy)

        return department_hierarchy

    def print_department_hierarchy(self, all_user, department_hierarchy, prefix=""):
        for department_info in department_hierarchy:
            department_name = department_info[0]
            users = department_info[1]
            sub_departments = department_info[2:]

            if prefix:
                current_path = f"{prefix}/{department_name}"
            else:
                current_path = department_name

            for user in users:
                # print(current_path+'/'+user['user_name'])
                all_user.append([current_path, user])
            if sub_departments:
                self.print_department_hierarchy(all_user, sub_departments, current_path)

    def get_all_users(self) -> list:
        """
        获取当前组织所有用户
        :return:
        """
        all_users = []
        # 获取顶级部门
        dept_name = self.get_top_departments(all_users)

        # 获取子部门
        top_department_id = 1
        top_department_list = self.get_sub_department_list(top_department_id)
        department_hierarchy = self.generate_department_hierarchy(top_department_list)
        self.print_department_hierarchy(all_users, department_hierarchy, prefix=dept_name)
        return all_users

    def get_dismission_staff(self) -> list:
        """
        获取离职员工列表
        :return:
        """
        staff_list = []
        self._get_dismission_staff(staff_list)
        return staff_list


class LDAPClient:
    def __init__(self, server_url: str, base, username, password):
        self.base = base
        self.server = Server(server_url, get_info=ALL)
        self.connection = Connection(self.server, user=f'cn={username},{base}', password=password, auto_bind=True)

    def search(self, search_base, search_filter, search_scope='SUBTREE', attributes=None):
        self.connection.search(search_base=search_base,
                               search_filter=search_filter,
                               search_scope=search_scope,
                               attributes=attributes)
        return self.connection.entries

    def add(self, dn, object_class, attributes):
        self.connection.add(dn, object_class, attributes)

    def delete(self, dn):
        self.connection.delete(dn)

    def delete_all_ou(self):
        self.connection.search(search_base=self.base,
                search_filter='(objectClass=organizationalUnit)',
                search_scope=SUBTREE,
                attributes=[ALL_ATTRIBUTES])
        # 删除搜索到的所有OU
        for entry in self.connection.entries:
            dn = entry.entry_dn
            print(dn)
            self.connection.delete(dn)

    def modify(self, dn, changes):
        self.connection.modify(dn, changes)

    def unbind(self):
        self.connection.unbind()

    def add_staff(self, staff_list: list) -> None:
        for users in staff_list:
            # 部门
            dept = users[0]
            dept_list = dept.split('/')
            dept_ous_list = []
            for dept_name in dept_list:
                dept_ous_list.append(dept_name)
                dept_ous = ','.join([f'ou={dept}' for dept in dept_ous_list[::-1]])
                dept_ou_dn = f'{dept_ous},{self.base}'
                dept_ou_attrs = {
                    'objectClass': ['top', 'organizationalUnit'],
                    'ou': f'{dept_name}'
                }
                print(dept_ou_dn)
                self.add(dept_ou_dn, dept_ou_attrs['objectClass'], dept_ou_attrs)

            # 用户
            user_info = users[1]
            ncn = user_info['user_name_pinyin']
            new_user_info = {
                'uid': user_info['uid'],
                'cn': ncn,
                'mail': ncn + "@vevor.net",
                'mobile': user_info['mobile'],
                'sn': user_info['user_name'],
                'userPassword': 'vevor123456',
                'objectClass': ['top', 'person', 'inetOrgPerson']
            }
            ous = ','.join([f'ou={dept}' for dept in dept_list[::-1]])
            new_user_dn = f'cn={ncn},{ous},{self.base}'
            print(new_user_dn)
            self.add(new_user_dn, new_user_info['objectClass'], new_user_info)

    def delete_staff(self, staff_uid_list: list, company_name='') -> None:
        """
        根据员工uid 删除员工
        :param staff_uid_list:
        :param company_name: 需要禁止的公司
        :return:
        """
        search_base = self.base if company_name == '' else f'ou={company_name},{self.base}'
        for uid in staff_uid_list:
            self.connection.search(
                search_base=search_base,
                search_filter=f'(&(objectclass=person)(uid={uid}))',
                search_scope=SUBTREE
            )

            if len(self.connection.entries) > 0:
                for entry in self.connection.entries:
                    user_dn = entry.entry_dn
                    self.connection.delete(user_dn)
                    print(f"User with DN {user_dn} is now disabled.")
            else:
                print(f"User with UID {uid} not found or multiple entries found.")


if __name__ == '__main__':
    # 获取AK, SK
    conf = Config('config.ini')
    ss_ak, ss_sk = conf.get_ak_sk('ssdingtalk')
    gm_ak, gm_sk = conf.get_ak_sk('gmdingtalk')
    qtl_ak, qtl_sk = conf.get_ak_sk('qtldingtalk')

    # 初始化钉钉对象
    dingtalk_ss = DeptUser(ss_ak, ss_sk)
    dingtalk_gm = DeptUser(gm_ak, gm_sk)
    dingtalk_qtl = DeptUser(qtl_ak, qtl_sk)

    # 获取离职员工uid列表
    ss_dismission_staff = dingtalk_ss.get_dismission_staff()
    gm_dismission_staff = dingtalk_gm.get_dismission_staff()
    qtl_dismission_staff = dingtalk_qtl.get_dismission_staff()

    # 获取钉钉部门及用户
    ss_staff = dingtalk_ss.get_all_users()
    gm_staff = dingtalk_gm.get_all_users()
    qtl_staff = dingtalk_qtl.get_all_users()

    # Ldap
    ldap_client = LDAPClient('ldap://192.168.18.91:389', 'dc=vevor,dc=net', 'admin','123456')

    # 添加员工
    ldap_client.add_staff(ss_staff)
    ldap_client.add_staff(gm_staff)
    ldap_client.add_staff(qtl_staff)

    # 删除 离职员工
    # ldap_client.delete_staff(['202719250920330978'])
    ldap_client.delete_staff(ss_dismission_staff, 'xxxxxxxxxx')
    ldap_client.delete_staff(gm_dismission_staff, 'xxxxxxxxxx')
    ldap_client.delete_staff(qtl_dismission_staff, 'xxxxxxxx')

    # 断开连接
    ldap_client.unbind()