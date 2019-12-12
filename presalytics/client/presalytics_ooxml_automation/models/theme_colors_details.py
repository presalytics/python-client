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


class ThemeColorsDetails(object):
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
        'theme': 'object',
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
        'id': 'str',
        'date_created': 'datetime',
        'user_created': 'str',
        'date_modified': 'datetime',
        'user_modified': 'str'
    }

    attribute_map = {
        'name': 'name',
        'theme_id': 'themeId',
        'theme': 'theme',
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
        'id': 'id',
        'date_created': 'dateCreated',
        'user_created': 'userCreated',
        'date_modified': 'dateModified',
        'user_modified': 'userModified'
    }

    def __init__(self, name=None, theme_id=None, theme=None, accent1=None, accent2=None, accent3=None, accent4=None, accent5=None, accent6=None, light1=None, light2=None, dark1=None, dark2=None, hyperlink=None, followed_hyperlink=None, id=None, date_created=None, user_created=None, date_modified=None, user_modified=None, local_vars_configuration=None):  # noqa: E501
        """ThemeColorsDetails - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._theme_id = None
        self._theme = None
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
        self._date_created = None
        self._user_created = None
        self._date_modified = None
        self._user_modified = None
        self.discriminator = None

        self.name = name
        self.theme_id = theme_id
        if theme is not None:
            self.theme = theme
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
        if date_created is not None:
            self.date_created = date_created
        if user_created is not None:
            self.user_created = user_created
        if date_modified is not None:
            self.date_modified = date_modified
        if user_modified is not None:
            self.user_modified = user_modified

    @property
    def name(self):
        """Gets the name of this ThemeColorsDetails.  # noqa: E501


        :return: The name of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ThemeColorsDetails.


        :param name: The name of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def theme_id(self):
        """Gets the theme_id of this ThemeColorsDetails.  # noqa: E501


        :return: The theme_id of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._theme_id

    @theme_id.setter
    def theme_id(self, theme_id):
        """Sets the theme_id of this ThemeColorsDetails.


        :param theme_id: The theme_id of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._theme_id = theme_id

    @property
    def theme(self):
        """Gets the theme of this ThemeColorsDetails.  # noqa: E501


        :return: The theme of this ThemeColorsDetails.  # noqa: E501
        :rtype: object
        """
        return self._theme

    @theme.setter
    def theme(self, theme):
        """Sets the theme of this ThemeColorsDetails.


        :param theme: The theme of this ThemeColorsDetails.  # noqa: E501
        :type: object
        """

        self._theme = theme

    @property
    def accent1(self):
        """Gets the accent1 of this ThemeColorsDetails.  # noqa: E501


        :return: The accent1 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._accent1

    @accent1.setter
    def accent1(self, accent1):
        """Sets the accent1 of this ThemeColorsDetails.


        :param accent1: The accent1 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._accent1 = accent1

    @property
    def accent2(self):
        """Gets the accent2 of this ThemeColorsDetails.  # noqa: E501


        :return: The accent2 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._accent2

    @accent2.setter
    def accent2(self, accent2):
        """Sets the accent2 of this ThemeColorsDetails.


        :param accent2: The accent2 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._accent2 = accent2

    @property
    def accent3(self):
        """Gets the accent3 of this ThemeColorsDetails.  # noqa: E501


        :return: The accent3 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._accent3

    @accent3.setter
    def accent3(self, accent3):
        """Sets the accent3 of this ThemeColorsDetails.


        :param accent3: The accent3 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._accent3 = accent3

    @property
    def accent4(self):
        """Gets the accent4 of this ThemeColorsDetails.  # noqa: E501


        :return: The accent4 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._accent4

    @accent4.setter
    def accent4(self, accent4):
        """Sets the accent4 of this ThemeColorsDetails.


        :param accent4: The accent4 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._accent4 = accent4

    @property
    def accent5(self):
        """Gets the accent5 of this ThemeColorsDetails.  # noqa: E501


        :return: The accent5 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._accent5

    @accent5.setter
    def accent5(self, accent5):
        """Sets the accent5 of this ThemeColorsDetails.


        :param accent5: The accent5 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._accent5 = accent5

    @property
    def accent6(self):
        """Gets the accent6 of this ThemeColorsDetails.  # noqa: E501


        :return: The accent6 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._accent6

    @accent6.setter
    def accent6(self, accent6):
        """Sets the accent6 of this ThemeColorsDetails.


        :param accent6: The accent6 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._accent6 = accent6

    @property
    def light1(self):
        """Gets the light1 of this ThemeColorsDetails.  # noqa: E501


        :return: The light1 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._light1

    @light1.setter
    def light1(self, light1):
        """Sets the light1 of this ThemeColorsDetails.


        :param light1: The light1 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._light1 = light1

    @property
    def light2(self):
        """Gets the light2 of this ThemeColorsDetails.  # noqa: E501


        :return: The light2 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._light2

    @light2.setter
    def light2(self, light2):
        """Sets the light2 of this ThemeColorsDetails.


        :param light2: The light2 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._light2 = light2

    @property
    def dark1(self):
        """Gets the dark1 of this ThemeColorsDetails.  # noqa: E501


        :return: The dark1 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._dark1

    @dark1.setter
    def dark1(self, dark1):
        """Sets the dark1 of this ThemeColorsDetails.


        :param dark1: The dark1 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._dark1 = dark1

    @property
    def dark2(self):
        """Gets the dark2 of this ThemeColorsDetails.  # noqa: E501


        :return: The dark2 of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._dark2

    @dark2.setter
    def dark2(self, dark2):
        """Sets the dark2 of this ThemeColorsDetails.


        :param dark2: The dark2 of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._dark2 = dark2

    @property
    def hyperlink(self):
        """Gets the hyperlink of this ThemeColorsDetails.  # noqa: E501


        :return: The hyperlink of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, hyperlink):
        """Sets the hyperlink of this ThemeColorsDetails.


        :param hyperlink: The hyperlink of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._hyperlink = hyperlink

    @property
    def followed_hyperlink(self):
        """Gets the followed_hyperlink of this ThemeColorsDetails.  # noqa: E501


        :return: The followed_hyperlink of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._followed_hyperlink

    @followed_hyperlink.setter
    def followed_hyperlink(self, followed_hyperlink):
        """Sets the followed_hyperlink of this ThemeColorsDetails.


        :param followed_hyperlink: The followed_hyperlink of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._followed_hyperlink = followed_hyperlink

    @property
    def id(self):
        """Gets the id of this ThemeColorsDetails.  # noqa: E501


        :return: The id of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ThemeColorsDetails.


        :param id: The id of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def date_created(self):
        """Gets the date_created of this ThemeColorsDetails.  # noqa: E501


        :return: The date_created of this ThemeColorsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """Sets the date_created of this ThemeColorsDetails.


        :param date_created: The date_created of this ThemeColorsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_created = date_created

    @property
    def user_created(self):
        """Gets the user_created of this ThemeColorsDetails.  # noqa: E501


        :return: The user_created of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_created

    @user_created.setter
    def user_created(self, user_created):
        """Sets the user_created of this ThemeColorsDetails.


        :param user_created: The user_created of this ThemeColorsDetails.  # noqa: E501
        :type: str
        """

        self._user_created = user_created

    @property
    def date_modified(self):
        """Gets the date_modified of this ThemeColorsDetails.  # noqa: E501


        :return: The date_modified of this ThemeColorsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """Sets the date_modified of this ThemeColorsDetails.


        :param date_modified: The date_modified of this ThemeColorsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_modified = date_modified

    @property
    def user_modified(self):
        """Gets the user_modified of this ThemeColorsDetails.  # noqa: E501


        :return: The user_modified of this ThemeColorsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_modified

    @user_modified.setter
    def user_modified(self, user_modified):
        """Sets the user_modified of this ThemeColorsDetails.


        :param user_modified: The user_modified of this ThemeColorsDetails.  # noqa: E501
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
        if not isinstance(other, ThemeColorsDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ThemeColorsDetails):
            return True

        return self.to_dict() != other.to_dict()
