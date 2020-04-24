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

from presalytics.client.presalytics_story.configuration import Configuration


class ViewAllOf(object):
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
        'session_id': 'str',
        'start_time': 'datetime',
        'end_time': 'datetime',
        'active_msecs': 'int',
        'total_msecs': 'int',
        'additional': 'str'
    }

    attribute_map = {
        'session_id': 'session_id',
        'start_time': 'start_time',
        'end_time': 'end_time',
        'active_msecs': 'active_msecs',
        'total_msecs': 'total_msecs',
        'additional': 'additional'
    }

    def __init__(self, session_id=None, start_time=None, end_time=None, active_msecs=None, total_msecs=None, additional=None, local_vars_configuration=None):  # noqa: E501
        """ViewAllOf - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._session_id = None
        self._start_time = None
        self._end_time = None
        self._active_msecs = None
        self._total_msecs = None
        self._additional = None
        self.discriminator = None

        if session_id is not None:
            self.session_id = session_id
        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if active_msecs is not None:
            self.active_msecs = active_msecs
        if total_msecs is not None:
            self.total_msecs = total_msecs
        if additional is not None:
            self.additional = additional

    @property
    def session_id(self):
        """Gets the session_id of this ViewAllOf.  # noqa: E501


        :return: The session_id of this ViewAllOf.  # noqa: E501
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """Sets the session_id of this ViewAllOf.


        :param session_id: The session_id of this ViewAllOf.  # noqa: E501
        :type: str
        """

        self._session_id = session_id

    @property
    def start_time(self):
        """Gets the start_time of this ViewAllOf.  # noqa: E501


        :return: The start_time of this ViewAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this ViewAllOf.


        :param start_time: The start_time of this ViewAllOf.  # noqa: E501
        :type: datetime
        """

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this ViewAllOf.  # noqa: E501


        :return: The end_time of this ViewAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this ViewAllOf.


        :param end_time: The end_time of this ViewAllOf.  # noqa: E501
        :type: datetime
        """

        self._end_time = end_time

    @property
    def active_msecs(self):
        """Gets the active_msecs of this ViewAllOf.  # noqa: E501


        :return: The active_msecs of this ViewAllOf.  # noqa: E501
        :rtype: int
        """
        return self._active_msecs

    @active_msecs.setter
    def active_msecs(self, active_msecs):
        """Sets the active_msecs of this ViewAllOf.


        :param active_msecs: The active_msecs of this ViewAllOf.  # noqa: E501
        :type: int
        """

        self._active_msecs = active_msecs

    @property
    def total_msecs(self):
        """Gets the total_msecs of this ViewAllOf.  # noqa: E501


        :return: The total_msecs of this ViewAllOf.  # noqa: E501
        :rtype: int
        """
        return self._total_msecs

    @total_msecs.setter
    def total_msecs(self, total_msecs):
        """Sets the total_msecs of this ViewAllOf.


        :param total_msecs: The total_msecs of this ViewAllOf.  # noqa: E501
        :type: int
        """

        self._total_msecs = total_msecs

    @property
    def additional(self):
        """Gets the additional of this ViewAllOf.  # noqa: E501


        :return: The additional of this ViewAllOf.  # noqa: E501
        :rtype: str
        """
        return self._additional

    @additional.setter
    def additional(self, additional):
        """Sets the additional of this ViewAllOf.


        :param additional: The additional of this ViewAllOf.  # noqa: E501
        :type: str
        """

        self._additional = additional

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
        if not isinstance(other, ViewAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ViewAllOf):
            return True

        return self.to_dict() != other.to_dict()
