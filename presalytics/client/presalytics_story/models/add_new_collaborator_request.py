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


class AddNewCollaboratorRequest(object):
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
        'collaborator_type': 'str',
        'user_email': 'str',
        'user_id': 'str'
    }

    attribute_map = {
        'collaborator_type': 'collaborator_type',
        'user_email': 'user_email',
        'user_id': 'user_id'
    }

    def __init__(self, collaborator_type=None, user_email=None, user_id=None):  # noqa: E501
        """AddNewCollaboratorRequest - a model defined in OpenAPI"""  # noqa: E501

        self._collaborator_type = None
        self._user_email = None
        self._user_id = None
        self.discriminator = None

        if collaborator_type is not None:
            self.collaborator_type = collaborator_type
        if user_email is not None:
            self.user_email = user_email
        if user_id is not None:
            self.user_id = user_id

    @property
    def collaborator_type(self):
        """Gets the collaborator_type of this AddNewCollaboratorRequest.  # noqa: E501


        :return: The collaborator_type of this AddNewCollaboratorRequest.  # noqa: E501
        :rtype: str
        """
        return self._collaborator_type

    @collaborator_type.setter
    def collaborator_type(self, collaborator_type):
        """Sets the collaborator_type of this AddNewCollaboratorRequest.


        :param collaborator_type: The collaborator_type of this AddNewCollaboratorRequest.  # noqa: E501
        :type: str
        """

        self._collaborator_type = collaborator_type

    @property
    def user_email(self):
        """Gets the user_email of this AddNewCollaboratorRequest.  # noqa: E501


        :return: The user_email of this AddNewCollaboratorRequest.  # noqa: E501
        :rtype: str
        """
        return self._user_email

    @user_email.setter
    def user_email(self, user_email):
        """Sets the user_email of this AddNewCollaboratorRequest.


        :param user_email: The user_email of this AddNewCollaboratorRequest.  # noqa: E501
        :type: str
        """

        self._user_email = user_email

    @property
    def user_id(self):
        """Gets the user_id of this AddNewCollaboratorRequest.  # noqa: E501


        :return: The user_id of this AddNewCollaboratorRequest.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this AddNewCollaboratorRequest.


        :param user_id: The user_id of this AddNewCollaboratorRequest.  # noqa: E501
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
        if not isinstance(other, AddNewCollaboratorRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
