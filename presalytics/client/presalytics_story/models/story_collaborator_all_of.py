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

from presalytics_story.configuration import Configuration


class StoryCollaboratorAllOf(object):
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
        'email': 'str',
        'name': 'str',
        'permission_type': 'PermissionType',
        'permission_type_id': 'str',
        'story_id': 'str',
        'user_id': 'str'
    }

    attribute_map = {
        'email': 'email',
        'name': 'name',
        'permission_type': 'permission_type',
        'permission_type_id': 'permission_type_id',
        'story_id': 'story_id',
        'user_id': 'user_id'
    }

    def __init__(self, email=None, name=None, permission_type=None, permission_type_id=None, story_id=None, user_id=None, local_vars_configuration=None):  # noqa: E501
        """StoryCollaboratorAllOf - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._email = None
        self._name = None
        self._permission_type = None
        self._permission_type_id = None
        self._story_id = None
        self._user_id = None
        self.discriminator = None

        if email is not None:
            self.email = email
        if name is not None:
            self.name = name
        if permission_type is not None:
            self.permission_type = permission_type
        if permission_type_id is not None:
            self.permission_type_id = permission_type_id
        if story_id is not None:
            self.story_id = story_id
        if user_id is not None:
            self.user_id = user_id

    @property
    def email(self):
        """Gets the email of this StoryCollaboratorAllOf.  # noqa: E501


        :return: The email of this StoryCollaboratorAllOf.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this StoryCollaboratorAllOf.


        :param email: The email of this StoryCollaboratorAllOf.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def name(self):
        """Gets the name of this StoryCollaboratorAllOf.  # noqa: E501


        :return: The name of this StoryCollaboratorAllOf.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this StoryCollaboratorAllOf.


        :param name: The name of this StoryCollaboratorAllOf.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def permission_type(self):
        """Gets the permission_type of this StoryCollaboratorAllOf.  # noqa: E501


        :return: The permission_type of this StoryCollaboratorAllOf.  # noqa: E501
        :rtype: PermissionType
        """
        return self._permission_type

    @permission_type.setter
    def permission_type(self, permission_type):
        """Sets the permission_type of this StoryCollaboratorAllOf.


        :param permission_type: The permission_type of this StoryCollaboratorAllOf.  # noqa: E501
        :type: PermissionType
        """

        self._permission_type = permission_type

    @property
    def permission_type_id(self):
        """Gets the permission_type_id of this StoryCollaboratorAllOf.  # noqa: E501


        :return: The permission_type_id of this StoryCollaboratorAllOf.  # noqa: E501
        :rtype: str
        """
        return self._permission_type_id

    @permission_type_id.setter
    def permission_type_id(self, permission_type_id):
        """Sets the permission_type_id of this StoryCollaboratorAllOf.


        :param permission_type_id: The permission_type_id of this StoryCollaboratorAllOf.  # noqa: E501
        :type: str
        """

        self._permission_type_id = permission_type_id

    @property
    def story_id(self):
        """Gets the story_id of this StoryCollaboratorAllOf.  # noqa: E501


        :return: The story_id of this StoryCollaboratorAllOf.  # noqa: E501
        :rtype: str
        """
        return self._story_id

    @story_id.setter
    def story_id(self, story_id):
        """Sets the story_id of this StoryCollaboratorAllOf.


        :param story_id: The story_id of this StoryCollaboratorAllOf.  # noqa: E501
        :type: str
        """

        self._story_id = story_id

    @property
    def user_id(self):
        """Gets the user_id of this StoryCollaboratorAllOf.  # noqa: E501


        :return: The user_id of this StoryCollaboratorAllOf.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this StoryCollaboratorAllOf.


        :param user_id: The user_id of this StoryCollaboratorAllOf.  # noqa: E501
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
        if not isinstance(other, StoryCollaboratorAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StoryCollaboratorAllOf):
            return True

        return self.to_dict() != other.to_dict()
