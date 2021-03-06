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


class View(object):
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
        'active_msecs': 'int',
        'additional': 'str',
        'end_time': 'datetime',
        'page_number': 'int',
        'session_id': 'str',
        'start_time': 'datetime',
        'total_msecs': 'int'
    }

    attribute_map = {
        'created_at': 'created_at',
        'created_by': 'created_by',
        'id': 'id',
        'updated_at': 'updated_at',
        'updated_by': 'updated_by',
        'active_msecs': 'active_msecs',
        'additional': 'additional',
        'end_time': 'end_time',
        'page_number': 'page_number',
        'session_id': 'session_id',
        'start_time': 'start_time',
        'total_msecs': 'total_msecs'
    }

    def __init__(self, created_at=None, created_by=None, id=None, updated_at=None, updated_by=None, active_msecs=None, additional=None, end_time=None, page_number=None, session_id=None, start_time=None, total_msecs=None):  # noqa: E501
        """View - a model defined in OpenAPI"""  # noqa: E501

        self._created_at = None
        self._created_by = None
        self._id = None
        self._updated_at = None
        self._updated_by = None
        self._active_msecs = None
        self._additional = None
        self._end_time = None
        self._page_number = None
        self._session_id = None
        self._start_time = None
        self._total_msecs = None
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
        if active_msecs is not None:
            self.active_msecs = active_msecs
        if additional is not None:
            self.additional = additional
        if end_time is not None:
            self.end_time = end_time
        if page_number is not None:
            self.page_number = page_number
        if session_id is not None:
            self.session_id = session_id
        if start_time is not None:
            self.start_time = start_time
        if total_msecs is not None:
            self.total_msecs = total_msecs

    @property
    def created_at(self):
        """Gets the created_at of this View.  # noqa: E501


        :return: The created_at of this View.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this View.


        :param created_at: The created_at of this View.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this View.  # noqa: E501


        :return: The created_by of this View.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this View.


        :param created_by: The created_by of this View.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def id(self):
        """Gets the id of this View.  # noqa: E501


        :return: The id of this View.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this View.


        :param id: The id of this View.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def updated_at(self):
        """Gets the updated_at of this View.  # noqa: E501


        :return: The updated_at of this View.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this View.


        :param updated_at: The updated_at of this View.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def updated_by(self):
        """Gets the updated_by of this View.  # noqa: E501


        :return: The updated_by of this View.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this View.


        :param updated_by: The updated_by of this View.  # noqa: E501
        :type: str
        """

        self._updated_by = updated_by

    @property
    def active_msecs(self):
        """Gets the active_msecs of this View.  # noqa: E501


        :return: The active_msecs of this View.  # noqa: E501
        :rtype: int
        """
        return self._active_msecs

    @active_msecs.setter
    def active_msecs(self, active_msecs):
        """Sets the active_msecs of this View.


        :param active_msecs: The active_msecs of this View.  # noqa: E501
        :type: int
        """

        self._active_msecs = active_msecs

    @property
    def additional(self):
        """Gets the additional of this View.  # noqa: E501


        :return: The additional of this View.  # noqa: E501
        :rtype: str
        """
        return self._additional

    @additional.setter
    def additional(self, additional):
        """Sets the additional of this View.


        :param additional: The additional of this View.  # noqa: E501
        :type: str
        """

        self._additional = additional

    @property
    def end_time(self):
        """Gets the end_time of this View.  # noqa: E501


        :return: The end_time of this View.  # noqa: E501
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this View.


        :param end_time: The end_time of this View.  # noqa: E501
        :type: datetime
        """

        self._end_time = end_time

    @property
    def page_number(self):
        """Gets the page_number of this View.  # noqa: E501


        :return: The page_number of this View.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this View.


        :param page_number: The page_number of this View.  # noqa: E501
        :type: int
        """

        self._page_number = page_number

    @property
    def session_id(self):
        """Gets the session_id of this View.  # noqa: E501


        :return: The session_id of this View.  # noqa: E501
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """Sets the session_id of this View.


        :param session_id: The session_id of this View.  # noqa: E501
        :type: str
        """

        self._session_id = session_id

    @property
    def start_time(self):
        """Gets the start_time of this View.  # noqa: E501


        :return: The start_time of this View.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this View.


        :param start_time: The start_time of this View.  # noqa: E501
        :type: datetime
        """

        self._start_time = start_time

    @property
    def total_msecs(self):
        """Gets the total_msecs of this View.  # noqa: E501


        :return: The total_msecs of this View.  # noqa: E501
        :rtype: int
        """
        return self._total_msecs

    @total_msecs.setter
    def total_msecs(self, total_msecs):
        """Sets the total_msecs of this View.


        :param total_msecs: The total_msecs of this View.  # noqa: E501
        :type: int
        """

        self._total_msecs = total_msecs

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
        if not isinstance(other, View):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
