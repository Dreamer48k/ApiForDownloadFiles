from bonsai import LDAPClient
from app.config import ACTIVE_DIRECTORY_DOMAIN_COMPONENT, LDAP_CLIENT, DOMAIN_USER_PREFIX


class AuthorizationAD:
    dc = ACTIVE_DIRECTORY_DOMAIN_COMPONENT
    client = LDAPClient(LDAP_CLIENT)
    user_prefix = DOMAIN_USER_PREFIX

    @classmethod
    async def get_inUserGroup(cls, username: str, passwd: str, group_name: str):
        if username is None:
            raise 'username is None'
        filterexp = "(&(objectClass=user)(sAMAccountName=" + username + "))"
        cls.client.set_credentials("SIMPLE", cls.user_prefix + username, passwd)
        try:
            async with cls.client.connect(is_async=True, timeout=2.0) as conn:
                res = await conn.search(cls.dc, 2, filterexp)
                for index, grop_name in enumerate(res[0]['memberOf']):
                    grop_name = (grop_name.split(',')[0]).replace('CN=', '')
                    # groups_names.append(grop_name)
                    res[0]['memberOf'][index] = grop_name
                groups_names = res[0]['memberOf']
                if group_name in groups_names:
                    return True
                else:
                    return False
        except Exception as error:
            return error

    @classmethod
    async def get_all_group(cls, username: str, passwd: str):
        if username is None:
            raise 'username is None'
        filterexp = "(&(objectClass=user)(sAMAccountName=" + username + "))"
        cls.client.set_credentials("SIMPLE", cls.user_prefix + username, passwd)
        try:
            async with cls.client.connect(is_async=True, timeout=2.0) as conn:
                res = await conn.search(cls.dc, 2, filterexp)
                for index, grop_name in enumerate(res[0]['memberOf']):
                    grop_name = (grop_name.split(',')[0]).replace('CN=', '')
                    # groups_names.append(grop_name)
                    res[0]['memberOf'][index] = grop_name
                groups_names = res[0]['memberOf']
            return groups_names
        except Exception as error:
            return error
