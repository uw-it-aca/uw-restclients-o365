from unittest import TestCase
from commonconf import settings
from uw_o365.license import License
from restclients_core.exceptions import DataFailureException
from uw_o365.util import fdao_o365_override


@fdao_o365_override
class O365TestLicense(TestCase):

    def test_license(self):
        license = License()
        skus = license.get_subscribed_skus()
        self.assertEquals(len(skus), 2)
        self.assertEquals(skus[0].sku_part_number, 'PLAN_9')

    def test_get_user_licenses(self):
        license = License()
        l = license.get_user_licenses('javerage')
        self.assertEquals(len(l), 2)

    def test_get_licenses_for_netid(self):
        license = License()
        l = license.get_licenses_for_netid('javerage')
        self.assertEquals(len(l), 0)

    def test_set_netid_license(self):
        license = License()
        response = license.set_licenses_for_netid('javerage')

    def test_set_user_license(self):
        license = License()
        response = license.set_user_licenses('javerage@test')
