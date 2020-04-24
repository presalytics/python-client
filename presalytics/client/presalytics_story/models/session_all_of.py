# coding: utf-8

"""
    Story

    This API is the main entry point for creating, editing and publishing analytics throught the Presalytics API  # noqa: E501

    The version of the OpenAPI document: 0.3.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from presalytics.client.presalytics_story.configuration import Configuration


class SessionAllOf(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'collaborator_id': 'str',
        'outline_revision': 'int',
        'host': 'str'
    }

    attribute_map = {
        'collaborator_id': 'collaborator_id',
        'outline_revision': 'outline_revision',
        'host': 'host'
    }

    def __init__(self, collaborator_id=None, outline_revision=None, host=None, local_vars_configuration=None):  # noqa: E501
        """SessionAllOf - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._collaborator_id = None
        self._outline_revision = None
        self._host = None
        self.discriminator = None

        if collaborator_id is not None:
            self.collaborator_id = collaborator_id
        if outline_revision is not None:
            self.outline_revision = outline_revision
        if host is not None:
            self.host = host

    @property
    def collaborator_id(self):
        """Gets the collaborator_id of this SessionAllOf.  # noqa: E501


        :return: The collaborator_id of this SessionAllOf.  # noqa: E501
        :rtype: str
        """
        return self._collaborator_id

    @collaborator_id.setter
    def collaborator_id(self, collaborator_id):
        """Sets the collaborator_id of this SessionAllOf.


        :param collaborator_id: The collaborator_id of this SessionAllOf.  # noqa: E501
        :type: str
        """

        self._collaborator_id = collaborator_id

    @property
    def outline_revision(self):
        """Gets the outline_revision of this SessionAllOf.  # noqa: E501


        :return: The outline_revision of this SessionAllOf.  # noqa: E501
        :rtype: int
        """
        return self._outline_revision

    @outline_revision.setter
    def outline_revision(self, outline_revision):
        """Sets the outline_revision of this SessionAllOf.


        :param outline_revision: The outline_revision of this SessionAllOf.  # noqa: E501
        :type: int
        """

        self._outline_revision = outline_revision

    @property
    def host(self):
        """Gets the host of this SessionAllOf.  # noqa: E501


        :return: The host of this SessionAllOf.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this SessionAllOf.


        :param host: The host of this SessionAllOf.  # noqa: E501
        :type: str
        """

        self._host = host

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SessionAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SessionAllOf):
            return True

        return self.to_dict() != other.to_dict()