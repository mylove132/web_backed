import logging
from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class ExternalAPIException(APIException):
    status_code = status.HTTP_200_OK

    def __init__(self, *args, **kwargs):
        super(ExternalAPIException, self).__init__(*args, **kwargs)
        logger.error("External API error: %s" % self)


class ProductNotExist(ExternalAPIException):
    default_code = 1


class FileNotExist(ExternalAPIException):
    default_code = 2


class PackageNotExist(ExternalAPIException):
    default_code = 3


class GroupNotExist(ExternalAPIException):
    default_code = 4


class ItemNotExist(ExternalAPIException):
    default_code = 5