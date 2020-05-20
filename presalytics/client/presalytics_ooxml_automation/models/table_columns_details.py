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


class TableColumnsDetails(object):
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
        'index': 'int',
        'width': 'int',
        'table_id': 'str',
        'table': 'TableTablesDetails',
        'cells': 'list[TableCellsDetails]',
        'id': 'str',
        'date_created': 'datetime',
        'user_created': 'str',
        'date_modified': 'datetime',
        'user_modified': 'str'
    }

    attribute_map = {
        'index': 'index',
        'width': 'width',
        'table_id': 'tableId',
        'table': 'table',
        'cells': 'cells',
        'id': 'id',
        'date_created': 'dateCreated',
        'user_created': 'userCreated',
        'date_modified': 'dateModified',
        'user_modified': 'userModified'
    }

    def __init__(self, index=None, width=None, table_id=None, table=None, cells=None, id=None, date_created=None, user_created=None, date_modified=None, user_modified=None):  # noqa: E501
        """TableColumnsDetails - a model defined in OpenAPI"""  # noqa: E501

        self._index = None
        self._width = None
        self._table_id = None
        self._table = None
        self._cells = None
        self._id = None
        self._date_created = None
        self._user_created = None
        self._date_modified = None
        self._user_modified = None
        self.discriminator = None

        if index is not None:
            self.index = index
        if width is not None:
            self.width = width
        self.table_id = table_id
        if table is not None:
            self.table = table
        self.cells = cells
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
    def index(self):
        """Gets the index of this TableColumnsDetails.  # noqa: E501


        :return: The index of this TableColumnsDetails.  # noqa: E501
        :rtype: int
        """
        return self._index

    @index.setter
    def index(self, index):
        """Sets the index of this TableColumnsDetails.


        :param index: The index of this TableColumnsDetails.  # noqa: E501
        :type: int
        """

        self._index = index

    @property
    def width(self):
        """Gets the width of this TableColumnsDetails.  # noqa: E501


        :return: The width of this TableColumnsDetails.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this TableColumnsDetails.


        :param width: The width of this TableColumnsDetails.  # noqa: E501
        :type: int
        """

        self._width = width

    @property
    def table_id(self):
        """Gets the table_id of this TableColumnsDetails.  # noqa: E501


        :return: The table_id of this TableColumnsDetails.  # noqa: E501
        :rtype: str
        """
        return self._table_id

    @table_id.setter
    def table_id(self, table_id):
        """Sets the table_id of this TableColumnsDetails.


        :param table_id: The table_id of this TableColumnsDetails.  # noqa: E501
        :type: str
        """

        self._table_id = table_id

    @property
    def table(self):
        """Gets the table of this TableColumnsDetails.  # noqa: E501


        :return: The table of this TableColumnsDetails.  # noqa: E501
        :rtype: TableTablesDetails
        """
        return self._table

    @table.setter
    def table(self, table):
        """Sets the table of this TableColumnsDetails.


        :param table: The table of this TableColumnsDetails.  # noqa: E501
        :type: TableTablesDetails
        """

        self._table = table

    @property
    def cells(self):
        """Gets the cells of this TableColumnsDetails.  # noqa: E501


        :return: The cells of this TableColumnsDetails.  # noqa: E501
        :rtype: list[TableCellsDetails]
        """
        return self._cells

    @cells.setter
    def cells(self, cells):
        """Sets the cells of this TableColumnsDetails.


        :param cells: The cells of this TableColumnsDetails.  # noqa: E501
        :type: list[TableCellsDetails]
        """

        self._cells = cells

    @property
    def id(self):
        """Gets the id of this TableColumnsDetails.  # noqa: E501


        :return: The id of this TableColumnsDetails.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this TableColumnsDetails.


        :param id: The id of this TableColumnsDetails.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def date_created(self):
        """Gets the date_created of this TableColumnsDetails.  # noqa: E501


        :return: The date_created of this TableColumnsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """Sets the date_created of this TableColumnsDetails.


        :param date_created: The date_created of this TableColumnsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_created = date_created

    @property
    def user_created(self):
        """Gets the user_created of this TableColumnsDetails.  # noqa: E501


        :return: The user_created of this TableColumnsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_created

    @user_created.setter
    def user_created(self, user_created):
        """Sets the user_created of this TableColumnsDetails.


        :param user_created: The user_created of this TableColumnsDetails.  # noqa: E501
        :type: str
        """

        self._user_created = user_created

    @property
    def date_modified(self):
        """Gets the date_modified of this TableColumnsDetails.  # noqa: E501


        :return: The date_modified of this TableColumnsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """Sets the date_modified of this TableColumnsDetails.


        :param date_modified: The date_modified of this TableColumnsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_modified = date_modified

    @property
    def user_modified(self):
        """Gets the user_modified of this TableColumnsDetails.  # noqa: E501


        :return: The user_modified of this TableColumnsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_modified

    @user_modified.setter
    def user_modified(self, user_modified):
        """Sets the user_modified of this TableColumnsDetails.


        :param user_modified: The user_modified of this TableColumnsDetails.  # noqa: E501
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
        if not isinstance(other, TableColumnsDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
