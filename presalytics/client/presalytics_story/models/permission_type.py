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


class PermissionType(object):
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
        'created_at': 'datetime',
        'created_by': 'str',
        'id': 'str',
        'updated_at': 'datetime',
        'updated_by': 'str',
        'can_add_collaborators': 'bool',
        'can_delete': 'bool',
        'can_edit': 'bool',
        'can_view': 'bool',
        'name': 'str'
    }

    attribute_map = {
        'created_at': 'created_at',
        'created_by': 'created_by',
        'id': 'id',
        'updated_at': 'updated_at',
        'updated_by': 'updated_by',
        'can_add_collaborators': 'can_add_collaborators',
        'can_delete': 'can_delete',
        'can_edit': 'can_edit',
        'can_view': 'can_view',
        'name': 'name'
    }

    def __init__(self, created_at=None, created_by=None, id=None, updated_at=None, updated_by=None, can_add_collaborators=None, can_delete=None, can_edit=None, can_view=None, name=None):  # noqa: E501
        """PermissionType - a model defined in OpenAPI"""  # noqa: E501

        self._created_at = None
        self._created_by = None
        self._id = None
        self._updated_at = None
        self._updated_by = None
        self._can_add_collaborators = None
        self._can_delete = None
        self._can_edit = None
        self._can_view = None
        self._name = None
        self.discriminator = None

        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if id is not None:
            self.id = id
        if updated_at is not None:
            self.updated_at = updated_at
        if updated_by is not None:
            self.updated_by = updated_by
        if can_add_collaborators is not None:
            self.can_add_collaborators = can_add_collaborators
        if can_delete is not None:
            self.can_delete = can_delete
        if can_edit is not None:
            self.can_edit = can_edit
        if can_view is not None:
            self.can_view = can_view
        if name is not None:
            self.name = name

    @property
    def created_at(self):
        """Gets the created_at of this PermissionType.  # noqa: E501


        :return: The created_at of this PermissionType.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this PermissionType.


        :param created_at: The created_at of this PermissionType.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this PermissionType.  # noqa: E501


        :return: The created_by of this PermissionType.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this PermissionType.


        :param created_by: The created_by of this PermissionType.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def id(self):
        """Gets the id of this PermissionType.  # noqa: E501


        :return: The id of this PermissionType.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PermissionType.


        :param id: The id of this PermissionType.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def updated_at(self):
        """Gets the updated_at of this PermissionType.  # noqa: E501


        :return: The updated_at of this PermissionType.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this PermissionType.


        :param updated_at: The updated_at of this PermissionType.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def updated_by(self):
        """Gets the updated_by of this PermissionType.  # noqa: E501


        :return: The updated_by of this PermissionType.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this PermissionType.


        :param updated_by: The updated_by of this PermissionType.  # noqa: E501
        :type: str
        """

        self._updated_by = updated_by

    @property
    def can_add_collaborators(self):
        """Gets the can_add_collaborators of this PermissionType.  # noqa: E501


        :return: The can_add_collaborators of this PermissionType.  # noqa: E501
        :rtype: bool
        """
        return self._can_add_collaborators

    @can_add_collaborators.setter
    def can_add_collaborators(self, can_add_collaborators):
        """Sets the can_add_collaborators of this PermissionType.


        :param can_add_collaborators: The can_add_collaborators of this PermissionType.  # noqa: E501
        :type: bool
        """

        self._can_add_collaborators = can_add_collaborators

    @property
    def can_delete(self):
        """Gets the can_delete of this PermissionType.  # noqa: E501


        :return: The can_delete of this PermissionType.  # noqa: E501
        :rtype: bool
        """
        return self._can_delete

    @can_delete.setter
    def can_delete(self, can_delete):
        """Sets the can_delete of this PermissionType.


        :param can_delete: The can_delete of this PermissionType.  # noqa: E501
        :type: bool
        """

        self._can_delete = can_delete

    @property
    def can_edit(self):
        """Gets the can_edit of this PermissionType.  # noqa: E501


        :return: The can_edit of this PermissionType.  # noqa: E501
        :rtype: bool
        """
        return self._can_edit

    @can_edit.setter
    def can_edit(self, can_edit):
        """Sets the can_edit of this PermissionType.


        :param can_edit: The can_edit of this PermissionType.  # noqa: E501
        :type: bool
        """

        self._can_edit = can_edit

    @property
    def can_view(self):
        """Gets the can_view of this PermissionType.  # noqa: E501


        :return: The can_view of this PermissionType.  # noqa: E501
        :rtype: bool
        """
        return self._can_view

    @can_view.setter
    def can_view(self, can_view):
        """Sets the can_view of this PermissionType.


        :param can_view: The can_view of this PermissionType.  # noqa: E501
        :type: bool
        """

        self._can_view = can_view

    @property
    def name(self):
        """Gets the name of this PermissionType.  # noqa: E501


        :return: The name of this PermissionType.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PermissionType.


        :param name: The name of this PermissionType.  # noqa: E501
        :type: str
        """

        self._name = name

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
        if not isinstance(other, PermissionType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
