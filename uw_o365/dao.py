import logging
import os
import re
from os.path import abspath, dirname
from restclients_core.dao import DAO


class O365_DAO(DAO):
    def service_name(self):
        return 'o365'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def _edit_mock_response(self, method, url, headers, body, response):
        if "POST" == method or "PUT" == method:
            if response.status != 400:
                path = "%s/resources/%s/file%s.%s" % (
                    abspath(dirname(__file__)), self.service_name(),
                    url, method)
                path = re.sub('[\?|<>=:*,;+&"@$]', '_', path)

                try:
                    handle = open(path)
                    response.data = handle.read()
                    response.status = 200
                except IOError:
                    response.status = 404
        elif "DELETE" == method:
            response.status = 200
