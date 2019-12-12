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


class ChartDataPointsDetails(object):
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
        'value': 'float',
        'column_id': 'str',
        'column': 'object',
        'row_id': 'str',
        'row': 'object',
        'chart_data_id': 'str',
        'chart_data': 'object',
        'id': 'str',
        'date_created': 'datetime',
        'user_created': 'str',
        'date_modified': 'datetime',
        'user_modified': 'str'
    }

    attribute_map = {
        'value': 'value',
        'column_id': 'columnId',
        'column': 'column',
        'row_id': 'rowId',
        'row': 'row',
        'chart_data_id': 'chartDataId',
        'chart_data': 'chartData',
        'id': 'id',
        'date_created': 'dateCreated',
        'user_created': 'userCreated',
        'date_modified': 'dateModified',
        'user_modified': 'userModified'
    }

    def __init__(self, value=None, column_id=None, column=None, row_id=None, row=None, chart_data_id=None, chart_data=None, id=None, date_created=None, user_created=None, date_modified=None, user_modified=None, local_vars_configuration=None):  # noqa: E501
        """ChartDataPointsDetails - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._value = None
        self._column_id = None
        self._column = None
        self._row_id = None
        self._row = None
        self._chart_data_id = None
        self._chart_data = None
        self._id = None
        self._date_created = None
        self._user_created = None
        self._date_modified = None
        self._user_modified = None
        self.discriminator = None

        if value is not None:
            self.value = value
        self.column_id = column_id
        if column is not None:
            self.column = column
        self.row_id = row_id
        if row is not None:
            self.row = row
        self.chart_data_id = chart_data_id
        if chart_data is not None:
            self.chart_data = chart_data
        if id is not None:
            self.id = id
        if date_created is not None:
            self.date_created = date_created
        if user_created is not None:
            self.user_created = user_created
        if date_modified is not None:
            self.date_modified = date_modified
        if user_modified is not None:
            self.user_modified = user_modified

    @property
    def value(self):
        """Gets the value of this ChartDataPointsDetails.  # noqa: E501


        :return: The value of this ChartDataPointsDetails.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this ChartDataPointsDetails.


        :param value: The value of this ChartDataPointsDetails.  # noqa: E501
        :type: float
        """

        self._value = value

    @property
    def column_id(self):
        """Gets the column_id of this ChartDataPointsDetails.  # noqa: E501


        :return: The column_id of this ChartDataPointsDetails.  # noqa: E501
        :rtype: str
        """
        return self._column_id

    @column_id.setter
    def column_id(self, column_id):
        """Sets the column_id of this ChartDataPointsDetails.


        :param column_id: The column_id of this ChartDataPointsDetails.  # noqa: E501
        :type: str
        """

        self._column_id = column_id

    @property
    def column(self):
        """Gets the column of this ChartDataPointsDetails.  # noqa: E501


        :return: The column of this ChartDataPointsDetails.  # noqa: E501
        :rtype: object
        """
        return self._column

    @column.setter
    def column(self, column):
        """Sets the column of this ChartDataPointsDetails.


        :param column: The column of this ChartDataPointsDetails.  # noqa: E501
        :type: object
        """

        self._column = column

    @property
    def row_id(self):
        """Gets the row_id of this ChartDataPointsDetails.  # noqa: E501


        :return: The row_id of this ChartDataPointsDetails.  # noqa: E501
        :rtype: str
        """
        return self._row_id

    @row_id.setter
    def row_id(self, row_id):
        """Sets the row_id of this ChartDataPointsDetails.


        :param row_id: The row_id of this ChartDataPointsDetails.  # noqa: E501
        :type: str
        """

        self._row_id = row_id

    @property
    def row(self):
        """Gets the row of this ChartDataPointsDetails.  # noqa: E501


        :return: The row of this ChartDataPointsDetails.  # noqa: E501
        :rtype: object
        """
        return self._row

    @row.setter
    def row(self, row):
        """Sets the row of this ChartDataPointsDetails.


        :param row: The row of this ChartDataPointsDetails.  # noqa: E501
        :type: object
        """

        self._row = row

    @property
    def chart_data_id(self):
        """Gets the chart_data_id of this ChartDataPointsDetails.  # noqa: E501


        :return: The chart_data_id of this ChartDataPointsDetails.  # noqa: E501
        :rtype: str
        """
        return self._chart_data_id

    @chart_data_id.setter
    def chart_data_id(self, chart_data_id):
        """Sets the chart_data_id of this ChartDataPointsDetails.


        :param chart_data_id: The chart_data_id of this ChartDataPointsDetails.  # noqa: E501
        :type: str
        """

        self._chart_data_id = chart_data_id

    @property
    def chart_data(self):
        """Gets the chart_data of this ChartDataPointsDetails.  # noqa: E501


        :return: The chart_data of this ChartDataPointsDetails.  # noqa: E501
        :rtype: object
        """
        return self._chart_data

    @chart_data.setter
    def chart_data(self, chart_data):
        """Sets the chart_data of this ChartDataPointsDetails.


        :param chart_data: The chart_data of this ChartDataPointsDetails.  # noqa: E501
        :type: object
        """

        self._chart_data = chart_data

    @property
    def id(self):
        """Gets the id of this ChartDataPointsDetails.  # noqa: E501


        :return: The id of this ChartDataPointsDetails.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ChartDataPointsDetails.


        :param id: The id of this ChartDataPointsDetails.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def date_created(self):
        """Gets the date_created of this ChartDataPointsDetails.  # noqa: E501


        :return: The date_created of this ChartDataPointsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """Sets the date_created of this ChartDataPointsDetails.


        :param date_created: The date_created of this ChartDataPointsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_created = date_created

    @property
    def user_created(self):
        """Gets the user_created of this ChartDataPointsDetails.  # noqa: E501


        :return: The user_created of this ChartDataPointsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_created

    @user_created.setter
    def user_created(self, user_created):
        """Sets the user_created of this ChartDataPointsDetails.


        :param user_created: The user_created of this ChartDataPointsDetails.  # noqa: E501
        :type: str
        """

        self._user_created = user_created

    @property
    def date_modified(self):
        """Gets the date_modified of this ChartDataPointsDetails.  # noqa: E501


        :return: The date_modified of this ChartDataPointsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """Sets the date_modified of this ChartDataPointsDetails.


        :param date_modified: The date_modified of this ChartDataPointsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_modified = date_modified

    @property
    def user_modified(self):
        """Gets the user_modified of this ChartDataPointsDetails.  # noqa: E501


        :return: The user_modified of this ChartDataPointsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_modified

    @user_modified.setter
    def user_modified(self, user_modified):
        """Sets the user_modified of this ChartDataPointsDetails.


        :param user_modified: The user_modified of this ChartDataPointsDetails.  # noqa: E501
        :type: str
        """

        self._user_modified = user_modified

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
        if not isinstance(other, ChartDataPointsDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChartDataPointsDetails):
            return True

        return self.to_dict() != other.to_dict()
