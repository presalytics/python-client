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


class BaseModel(object):
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
        'updated_by': 'str'
    }

    attribute_map = {
        'created_at': 'created_at',
        'created_by': 'created_by',
        'id': 'id',
        'updated_at': 'updated_at',
        'updated_by': 'updated_by'
    }

    def __init__(self, created_at=None, created_by=None, id=None, updated_at=None, updated_by=None, local_vars_configuration=None):  # noqa: E501
        """BaseModel - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._created_at = None
        self._created_by = None
        self._id = None
        self._updated_at = None
        self._updated_by = None
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

    @property
    def created_at(self):
        """Gets the created_at of this BaseModel.  # noqa: E501


        :return: The created_at of this BaseModel.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this BaseModel.


        :param created_at: The created_at of this BaseModel.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this BaseModel.  # noqa: E501


        :return: The created_by of this BaseModel.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this BaseModel.


        :param created_by: The created_by of this BaseModel.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def id(self):
        """Gets the id of this BaseModel.  # noqa: E501


        :return: The id of this BaseModel.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BaseModel.


        :param id: The id of this BaseModel.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def updated_at(self):
        """Gets the updated_at of this BaseModel.  # noqa: E501


        :return: The updated_at of this BaseModel.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this BaseModel.


        :param updated_at: The updated_at of this BaseModel.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def updated_by(self):
        """Gets the updated_by of this BaseModel.  # noqa: E501


        :return: The updated_by of this BaseModel.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this BaseModel.


        :param updated_by: The updated_by of this BaseModel.  # noqa: E501
        :type: str
        """

        self._updated_by = updated_by

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
        if not isinstance(other, BaseModel):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BaseModel):
            return True

        return self.to_dict() != other.to_dict()
