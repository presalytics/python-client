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

from presalytics.client.presalytics_ooxml_automation.configuration import Configuration


class ChartRowCol(object):
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
        'type_id': 'int',
        'row_name': 'str',
        'row_qualifed_assy': 'str',
        'col_name': 'str',
        'col_qualified_assy': 'str',
        'id': 'str'
    }

    attribute_map = {
        'type_id': 'typeId',
        'row_name': 'rowName',
        'row_qualifed_assy': 'rowQualifedAssy',
        'col_name': 'colName',
        'col_qualified_assy': 'colQualifiedAssy',
        'id': 'id'
    }

    def __init__(self, type_id=None, row_name=None, row_qualifed_assy=None, col_name=None, col_qualified_assy=None, id=None, local_vars_configuration=None):  # noqa: E501
        """ChartRowCol - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._type_id = None
        self._row_name = None
        self._row_qualifed_assy = None
        self._col_name = None
        self._col_qualified_assy = None
        self._id = None
        self.discriminator = None

        if type_id is not None:
            self.type_id = type_id
        self.row_name = row_name
        self.row_qualifed_assy = row_qualifed_assy
        self.col_name = col_name
        self.col_qualified_assy = col_qualified_assy
        if id is not None:
            self.id = id

    @property
    def type_id(self):
        """Gets the type_id of this ChartRowCol.  # noqa: E501


        :return: The type_id of this ChartRowCol.  # noqa: E501
        :rtype: int
        """
        return self._type_id

    @type_id.setter
    def type_id(self, type_id):
        """Sets the type_id of this ChartRowCol.


        :param type_id: The type_id of this ChartRowCol.  # noqa: E501
        :type: int
        """

        self._type_id = type_id

    @property
    def row_name(self):
        """Gets the row_name of this ChartRowCol.  # noqa: E501


        :return: The row_name of this ChartRowCol.  # noqa: E501
        :rtype: str
        """
        return self._row_name

    @row_name.setter
    def row_name(self, row_name):
        """Sets the row_name of this ChartRowCol.


        :param row_name: The row_name of this ChartRowCol.  # noqa: E501
        :type: str
        """

        self._row_name = row_name

    @property
    def row_qualifed_assy(self):
        """Gets the row_qualifed_assy of this ChartRowCol.  # noqa: E501


        :return: The row_qualifed_assy of this ChartRowCol.  # noqa: E501
        :rtype: str
        """
        return self._row_qualifed_assy

    @row_qualifed_assy.setter
    def row_qualifed_assy(self, row_qualifed_assy):
        """Sets the row_qualifed_assy of this ChartRowCol.


        :param row_qualifed_assy: The row_qualifed_assy of this ChartRowCol.  # noqa: E501
        :type: str
        """

        self._row_qualifed_assy = row_qualifed_assy

    @property
    def col_name(self):
        """Gets the col_name of this ChartRowCol.  # noqa: E501


        :return: The col_name of this ChartRowCol.  # noqa: E501
        :rtype: str
        """
        return self._col_name

    @col_name.setter
    def col_name(self, col_name):
        """Sets the col_name of this ChartRowCol.


        :param col_name: The col_name of this ChartRowCol.  # noqa: E501
        :type: str
        """

        self._col_name = col_name

    @property
    def col_qualified_assy(self):
        """Gets the col_qualified_assy of this ChartRowCol.  # noqa: E501


        :return: The col_qualified_assy of this ChartRowCol.  # noqa: E501
        :rtype: str
        """
        return self._col_qualified_assy

    @col_qualified_assy.setter
    def col_qualified_assy(self, col_qualified_assy):
        """Sets the col_qualified_assy of this ChartRowCol.


        :param col_qualified_assy: The col_qualified_assy of this ChartRowCol.  # noqa: E501
        :type: str
        """

        self._col_qualified_assy = col_qualified_assy

    @property
    def id(self):
        """Gets the id of this ChartRowCol.  # noqa: E501


        :return: The id of this ChartRowCol.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ChartRowCol.


        :param id: The id of this ChartRowCol.  # noqa: E501
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
        if not isinstance(other, ChartRowCol):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChartRowCol):
            return True

        return self.to_dict() != other.to_dict()
