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


class RequiredParametersToCreateAView(object):
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
        'page_number': 'int',
        'start_time': 'datetime',
        'end_time': 'datetime',
        'active_m_secs': 'int',
        'additional': 'str'
    }

    attribute_map = {
        'page_number': 'pageNumber',
        'start_time': 'startTime',
        'end_time': 'endTime',
        'active_m_secs': 'activeMSecs',
        'additional': 'additional'
    }

    def __init__(self, page_number=None, start_time=None, end_time=None, active_m_secs=None, additional=None, local_vars_configuration=None):  # noqa: E501
        """RequiredParametersToCreateAView - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._page_number = None
        self._start_time = None
        self._end_time = None
        self._active_m_secs = None
        self._additional = None
        self.discriminator = None

        self.page_number = page_number
        self.start_time = start_time
        self.end_time = end_time
        if active_m_secs is not None:
            self.active_m_secs = active_m_secs
        if additional is not None:
            self.additional = additional

    @property
    def page_number(self):
        """Gets the page_number of this RequiredParametersToCreateAView.  # noqa: E501


        :return: The page_number of this RequiredParametersToCreateAView.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this RequiredParametersToCreateAView.


        :param page_number: The page_number of this RequiredParametersToCreateAView.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and page_number is None:  # noqa: E501
            raise ValueError("Invalid value for `page_number`, must not be `None`")  # noqa: E501

        self._page_number = page_number

    @property
    def start_time(self):
        """Gets the start_time of this RequiredParametersToCreateAView.  # noqa: E501


        :return: The start_time of this RequiredParametersToCreateAView.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this RequiredParametersToCreateAView.


        :param start_time: The start_time of this RequiredParametersToCreateAView.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and start_time is None:  # noqa: E501
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this RequiredParametersToCreateAView.  # noqa: E501


        :return: The end_time of this RequiredParametersToCreateAView.  # noqa: E501
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this RequiredParametersToCreateAView.


        :param end_time: The end_time of this RequiredParametersToCreateAView.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and end_time is None:  # noqa: E501
            raise ValueError("Invalid value for `end_time`, must not be `None`")  # noqa: E501

        self._end_time = end_time

    @property
    def active_m_secs(self):
        """Gets the active_m_secs of this RequiredParametersToCreateAView.  # noqa: E501


        :return: The active_m_secs of this RequiredParametersToCreateAView.  # noqa: E501
        :rtype: int
        """
        return self._active_m_secs

    @active_m_secs.setter
    def active_m_secs(self, active_m_secs):
        """Sets the active_m_secs of this RequiredParametersToCreateAView.


        :param active_m_secs: The active_m_secs of this RequiredParametersToCreateAView.  # noqa: E501
        :type: int
        """

        self._active_m_secs = active_m_secs

    @property
    def additional(self):
        """Gets the additional of this RequiredParametersToCreateAView.  # noqa: E501


        :return: The additional of this RequiredParametersToCreateAView.  # noqa: E501
        :rtype: str
        """
        return self._additional

    @additional.setter
    def additional(self, additional):
        """Sets the additional of this RequiredParametersToCreateAView.


        :param additional: The additional of this RequiredParametersToCreateAView.  # noqa: E501
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
        if not isinstance(other, RequiredParametersToCreateAView):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RequiredParametersToCreateAView):
            return True

        return self.to_dict() != other.to_dict()
