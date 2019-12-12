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


class ThemeColors(object):
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
        'theme_id': 'str',
        'accent1': 'str',
        'accent2': 'str',
        'accent3': 'str',
        'accent4': 'str',
        'accent5': 'str',
        'accent6': 'str',
        'light1': 'str',
        'light2': 'str',
        'dark1': 'str',
        'dark2': 'str',
        'hyperlink': 'str',
        'followed_hyperlink': 'str',
        'id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'theme_id': 'themeId',
        'accent1': 'accent1',
        'accent2': 'accent2',
        'accent3': 'accent3',
        'accent4': 'accent4',
        'accent5': 'accent5',
        'accent6': 'accent6',
        'light1': 'light1',
        'light2': 'light2',
        'dark1': 'dark1',
        'dark2': 'dark2',
        'hyperlink': 'hyperlink',
        'followed_hyperlink': 'followedHyperlink',
        'id': 'id'
    }

    def __init__(self, name=None, theme_id=None, accent1=None, accent2=None, accent3=None, accent4=None, accent5=None, accent6=None, light1=None, light2=None, dark1=None, dark2=None, hyperlink=None, followed_hyperlink=None, id=None, local_vars_configuration=None):  # noqa: E501
        """ThemeColors - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._theme_id = None
        self._accent1 = None
        self._accent2 = None
        self._accent3 = None
        self._accent4 = None
        self._accent5 = None
        self._accent6 = None
        self._light1 = None
        self._light2 = None
        self._dark1 = None
        self._dark2 = None
        self._hyperlink = None
        self._followed_hyperlink = None
        self._id = None
        self.discriminator = None

        self.name = name
        self.theme_id = theme_id
        self.accent1 = accent1
        self.accent2 = accent2
        self.accent3 = accent3
        self.accent4 = accent4
        self.accent5 = accent5
        self.accent6 = accent6
        self.light1 = light1
        self.light2 = light2
        self.dark1 = dark1
        self.dark2 = dark2
        self.hyperlink = hyperlink
        self.followed_hyperlink = followed_hyperlink
        if id is not None:
            self.id = id

    @property
    def name(self):
        """Gets the name of this ThemeColors.  # noqa: E501


        :return: The name of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ThemeColors.


        :param name: The name of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def theme_id(self):
        """Gets the theme_id of this ThemeColors.  # noqa: E501


        :return: The theme_id of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._theme_id

    @theme_id.setter
    def theme_id(self, theme_id):
        """Sets the theme_id of this ThemeColors.


        :param theme_id: The theme_id of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._theme_id = theme_id

    @property
    def accent1(self):
        """Gets the accent1 of this ThemeColors.  # noqa: E501


        :return: The accent1 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._accent1

    @accent1.setter
    def accent1(self, accent1):
        """Sets the accent1 of this ThemeColors.


        :param accent1: The accent1 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._accent1 = accent1

    @property
    def accent2(self):
        """Gets the accent2 of this ThemeColors.  # noqa: E501


        :return: The accent2 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._accent2

    @accent2.setter
    def accent2(self, accent2):
        """Sets the accent2 of this ThemeColors.


        :param accent2: The accent2 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._accent2 = accent2

    @property
    def accent3(self):
        """Gets the accent3 of this ThemeColors.  # noqa: E501


        :return: The accent3 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._accent3

    @accent3.setter
    def accent3(self, accent3):
        """Sets the accent3 of this ThemeColors.


        :param accent3: The accent3 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._accent3 = accent3

    @property
    def accent4(self):
        """Gets the accent4 of this ThemeColors.  # noqa: E501


        :return: The accent4 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._accent4

    @accent4.setter
    def accent4(self, accent4):
        """Sets the accent4 of this ThemeColors.


        :param accent4: The accent4 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._accent4 = accent4

    @property
    def accent5(self):
        """Gets the accent5 of this ThemeColors.  # noqa: E501


        :return: The accent5 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._accent5

    @accent5.setter
    def accent5(self, accent5):
        """Sets the accent5 of this ThemeColors.


        :param accent5: The accent5 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._accent5 = accent5

    @property
    def accent6(self):
        """Gets the accent6 of this ThemeColors.  # noqa: E501


        :return: The accent6 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._accent6

    @accent6.setter
    def accent6(self, accent6):
        """Sets the accent6 of this ThemeColors.


        :param accent6: The accent6 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._accent6 = accent6

    @property
    def light1(self):
        """Gets the light1 of this ThemeColors.  # noqa: E501


        :return: The light1 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._light1

    @light1.setter
    def light1(self, light1):
        """Sets the light1 of this ThemeColors.


        :param light1: The light1 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._light1 = light1

    @property
    def light2(self):
        """Gets the light2 of this ThemeColors.  # noqa: E501


        :return: The light2 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._light2

    @light2.setter
    def light2(self, light2):
        """Sets the light2 of this ThemeColors.


        :param light2: The light2 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._light2 = light2

    @property
    def dark1(self):
        """Gets the dark1 of this ThemeColors.  # noqa: E501


        :return: The dark1 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._dark1

    @dark1.setter
    def dark1(self, dark1):
        """Sets the dark1 of this ThemeColors.


        :param dark1: The dark1 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._dark1 = dark1

    @property
    def dark2(self):
        """Gets the dark2 of this ThemeColors.  # noqa: E501


        :return: The dark2 of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._dark2

    @dark2.setter
    def dark2(self, dark2):
        """Sets the dark2 of this ThemeColors.


        :param dark2: The dark2 of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._dark2 = dark2

    @property
    def hyperlink(self):
        """Gets the hyperlink of this ThemeColors.  # noqa: E501


        :return: The hyperlink of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, hyperlink):
        """Sets the hyperlink of this ThemeColors.


        :param hyperlink: The hyperlink of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._hyperlink = hyperlink

    @property
    def followed_hyperlink(self):
        """Gets the followed_hyperlink of this ThemeColors.  # noqa: E501


        :return: The followed_hyperlink of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._followed_hyperlink

    @followed_hyperlink.setter
    def followed_hyperlink(self, followed_hyperlink):
        """Sets the followed_hyperlink of this ThemeColors.


        :param followed_hyperlink: The followed_hyperlink of this ThemeColors.  # noqa: E501
        :type: str
        """

        self._followed_hyperlink = followed_hyperlink

    @property
    def id(self):
        """Gets the id of this ThemeColors.  # noqa: E501


        :return: The id of this ThemeColors.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ThemeColors.


        :param id: The id of this ThemeColors.  # noqa: E501
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
        if not isinstance(other, ThemeColors):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ThemeColors):
            return True

        return self.to_dict() != other.to_dict()