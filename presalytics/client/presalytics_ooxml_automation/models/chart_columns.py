# coding: utf-8

"""
    OOXML Automation

    This API helps users convert Excel and Powerpoint documents into rich, live dashboards and stories.  # noqa: E501

    The version of the OpenAPI document: 0.1.0-no-tags
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class ChartColumns(object):
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
        'name': 'str',
        'index': 'int',
        'axis_id': 'str',
        'column_collection_id': 'str',
        'id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'index': 'index',
        'axis_id': 'axisId',
        'column_collection_id': 'columnCollectionId',
        'id': 'id'
    }

    def __init__(self, name=None, index=None, axis_id=None, column_collection_id=None, id=None):  # noqa: E501
        """ChartColumns - a model defined in OpenAPI"""  # noqa: E501

        self._name = None
        self._index = None
        self._axis_id = None
        self._column_collection_id = None
        self._id = None
        self.discriminator = None

        self.name = name
        if index is not None:
            self.index = index
        self.axis_id = axis_id
        self.column_collection_id = column_collection_id
        if id is not None:
            self.id = id

    @property
    def name(self):
        """Gets the name of this ChartColumns.  # noqa: E501


        :return: The name of this ChartColumns.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ChartColumns.


        :param name: The name of this ChartColumns.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def index(self):
        """Gets the index of this ChartColumns.  # noqa: E501


        :return: The index of this ChartColumns.  # noqa: E501
        :rtype: int
        """
        return self._index

    @index.setter
    def index(self, index):
        """Sets the index of this ChartColumns.


        :param index: The index of this ChartColumns.  # noqa: E501
        :type: int
        """

        self._index = index

    @property
    def axis_id(self):
        """Gets the axis_id of this ChartColumns.  # noqa: E501


        :return: The axis_id of this ChartColumns.  # noqa: E501
        :rtype: str
        """
        return self._axis_id

    @axis_id.setter
    def axis_id(self, axis_id):
        """Sets the axis_id of this ChartColumns.


        :param axis_id: The axis_id of this ChartColumns.  # noqa: E501
        :type: str
        """

        self._axis_id = axis_id

    @property
    def column_collection_id(self):
        """Gets the column_collection_id of this ChartColumns.  # noqa: E501


        :return: The column_collection_id of this ChartColumns.  # noqa: E501
        :rtype: str
        """
        return self._column_collection_id

    @column_collection_id.setter
    def column_collection_id(self, column_collection_id):
        """Sets the column_collection_id of this ChartColumns.


        :param column_collection_id: The column_collection_id of this ChartColumns.  # noqa: E501
        :type: str
        """

        self._column_collection_id = column_collection_id

    @property
    def id(self):
        """Gets the id of this ChartColumns.  # noqa: E501


        :return: The id of this ChartColumns.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ChartColumns.


        :param id: The id of this ChartColumns.  # noqa: E501
        :type: str
        """

        self._id = id

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
        if not isinstance(other, ChartColumns):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
