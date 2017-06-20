from restclients_core.util.decorators import use_mock
from uw_o365.dao import O365_DAO

fdao_o365_override = use_mock(O365_DAO())
