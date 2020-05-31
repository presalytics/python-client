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


class ModifyInactiveCollaborator(object):
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
        'action': 'str',
        'lead_id': 'int',
        'user_id': 'str'
    }

    attribute_map = {
        'action': 'action',
        'lead_id': 'lead_id',
        'user_id': 'user_id'
    }

    def __init__(self, action=None, lead_id=None, user_id=None):  # noqa: E501
        """ModifyInactiveCollaborator - a model defined in OpenAPI"""  # noqa: E501

        self._action = None
        self._lead_id = None
        self._user_id = None
        self.discriminator = None

        if action is not None:
            self.action = action
        if lead_id is not None:
            self.lead_id = lead_id
        if user_id is not None:
            self.user_id = user_id

    @property
    def action(self):
        """Gets the action of this ModifyInactiveCollaborator.  # noqa: E501


        :return: The action of this ModifyInactiveCollaborator.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this ModifyInactiveCollaborator.


        :param action: The action of this ModifyInactiveCollaborator.  # noqa: E501
        :type: str
        """

        self._action = action

    @property
    def lead_id(self):
        """Gets the lead_id of this ModifyInactiveCollaborator.  # noqa: E501


        :return: The lead_id of this ModifyInactiveCollaborator.  # noqa: E501
        :rtype: int
        """
        return self._lead_id

    @lead_id.setter
    def lead_id(self, lead_id):
        """Sets the lead_id of this ModifyInactiveCollaborator.


        :param lead_id: The lead_id of this ModifyInactiveCollaborator.  # noqa: E501
        :type: int
        """

        self._lead_id = lead_id

    @property
    def user_id(self):
        """Gets the user_id of this ModifyInactiveCollaborator.  # noqa: E501


        :return: The user_id of this ModifyInactiveCollaborator.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this ModifyInactiveCollaborator.


        :param user_id: The user_id of this ModifyInactiveCollaborator.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

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
        if not isinstance(other, ModifyInactiveCollaborator):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
