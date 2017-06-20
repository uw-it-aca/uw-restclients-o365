from unittest import TestCase
from commonconf import settings
from uw_o365.user import User
from restclients_core.exceptions import DataFailureException
from uw_pws.util import fdao_pws_override
from uw_o365.util import fdao_o365_override


@fdao_pws_override
@fdao_o365_override
class O365TestUser(TestCase):

    def test_users_info(self):
        user = User()
        users = user.get_users()
        self.assertEquals(len(users), 2)
        self.assertEquals(len(users[0].assigned_licenses), 1)
        self.assertEquals(users[0].assigned_licenses[0].sku_id, 'aaaaaaaa-1111-2222-3333-4444-ffffffffffff')
        self.assertEquals(len(users[0].assigned_plans), 1)
        self.assertEquals(users[0].assigned_plans[0].service_plan_name, 'MUMBLE')

    def test_users_generator_info(self):
        users = []
        user = User()
        for u in user.get_users_generator():
            users.append(u)

        self.assertEquals(len(users), 2)
        self.assertEquals(len(users[0].assigned_licenses), 1)
        self.assertEquals(users[0].assigned_licenses[0].sku_id, 'aaaaaaaa-1111-2222-3333-4444-ffffffffffff')
        self.assertEquals(len(users[0].assigned_plans), 1)
        self.assertEquals(users[0].assigned_plans[0].service_plan_name, 'MUMBLE')

    def test_user_info(self):
        user = User()
        u = user.get_user('javerage')
        self.assertEquals(len(u.assigned_plans), 7)
        self.assertEquals(u.user_principal_name, 'javerage@dogfood.com')

    def test_netid_info(self):
        user = User()
        u = user.get_user_by_netid('javerage')
        self.assertEquals(u.dir_sync_enabled, True)
        self.assertEquals(len(u.assigned_plans), 0)
        self.assertEquals(len(u.assigned_licenses), 0)
        self.assertEquals(u.mail_nick_name, 'javerage')

    def test_user_property(self):
        user = User()
        u = user.get_user_property('javerage', 'usageLocation')

    def test_netid_property(self):
        user = User()
        u = user.get_property_for_netid('javerage', 'usageLocation')

    def test_user_location(self):
        user = User()
        u = user.get_user_location('javerage')

    def test_netid_location(self):
        user = User()
        u = user.get_location_for_netid('javerage')

    def test_set_user_property(self):
        user = User()
        u = user.set_user_property('javerage', 'usageLocation', 'US')

    def test_netid_property(self):
        user = User()
        u = user.set_property_for_netid('javerage', 'usageLocation', 'US')

    def test_set_user_location(self):
        user = User()
        u = user.set_user_location('javerage', 'US')

    def test_set_netid_location(self):
        user = User()
        u = user.set_location_for_netid('javerage', 'US')
