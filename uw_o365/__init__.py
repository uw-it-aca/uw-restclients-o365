"""
This is the interface for interacting with Office 365 web services.
"""
from commonconf import settings
from uw_o365.dao import O365_DAO
from restclients_core.exceptions import DataFailureException
try:
    from urllib import quote, unquote, urlencode
except:
    from urllib.parse import quote, unquote, urlencode
from urllib3 import PoolManager
import warnings
from json import loads as json_loads
from json import dumps as json_dumps
import re


DEFAULT_PAGINATION = 0


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


class O365(object):
    """
    The O365 Management API
    """

    _api_version = '1.6'

    def __init__(self, *args, **kwargs):
        pass

    def get_resource(self, path, params=None):
        """
        O365 GET method. Return representation of the requested resource.
        """
        url = '%s%s' % (path, self._param_list(params))
        headers = {
            'Accept': 'application/json;odata=minimalmetadata'
        }

        response = O365_DAO().getURL(self._url(url), headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json_loads(response.data)

    def post_resource(self, path, body=None, json=None):
        """
        O365 POST method.
        """
        url = '%s%s' % (path, self._param_list())
        headers = {
            'Accept': 'application/json;odata=minimalmetadata'
        }

        if json:
            headers['Content-Type'] = 'application/json'
            body = json_dumps(json)

        response = O365_DAO().postURL(self._url(url), headers, body)

        if not (response.status == 200 or response.status == 201 or
                response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json_loads(response.data)

    def patch_resource(self, path, body=None, json=None):
        """
        O365 PATCH method.
        """
        url = '%s%s' % (path, self._param_list())
        headers = {
            'Accept': 'application/json;odata=minimalmetadata'
        }

        if json:
            headers['Content-Type'] = 'application/json'
            body = json_dumps(json)

        response = O365_DAO().patchURL(self._url(url), headers, body)

        if not (response.status == 200 or response.status == 201 or
                response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json_loads(response.data) if len(response.data) else {}

    def user_principal(self, netid, domain='test'):
        return '%s@%s' % (netid, getattr(settings,
                                         'RESTCLIENTS_O365_PRINCIPLE_DOMAIAN',
                                         domain))

    def _url(self, url):
        return '/%s%s' % (
            getattr(settings, 'RESTCLIENTS_O365_TENANT', 'test'), url)

    def _param_list(self, params=None):
        query_string = [urlencode({'api-version': self._api_version})]
        if params:
            try:
                items = params.iteritems()
            except:
                items = params.items()

            for key, val in items:
                if isinstance(val, list):
                    query_string.extend(
                        [urlencode({"%s[]" % key: str(v)}) for v in val])
                else:
                    query_string.append(urlencode({key: str(val)}))

        return "?%s" % "&".join(query_string)
