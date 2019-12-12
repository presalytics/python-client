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


class SlideGraphicsDetails(object):
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
        'group_elements_id': 'str',
        'group_element': 'object',
        'name': 'str',
        'ooxml_id': 'int',
        'graphic_type_id': 'int',
        'height': 'int',
        'width': 'int',
        'x_offset': 'int',
        'y_offset': 'int',
        'table': 'object',
        'chart': 'object',
        'smart_art': 'object',
        'picture': 'object',
        'id': 'str',
        'date_created': 'datetime',
        'user_created': 'str',
        'date_modified': 'datetime',
        'user_modified': 'str'
    }

    attribute_map = {
        'group_elements_id': 'groupElementsId',
        'group_element': 'groupElement',
        'name': 'name',
        'ooxml_id': 'ooxmlId',
        'graphic_type_id': 'graphicTypeId',
        'height': 'height',
        'width': 'width',
        'x_offset': 'xOffset',
        'y_offset': 'yOffset',
        'table': 'table',
        'chart': 'chart',
        'smart_art': 'smartArt',
        'picture': 'picture',
        'id': 'id',
        'date_created': 'dateCreated',
        'user_created': 'userCreated',
        'date_modified': 'dateModified',
        'user_modified': 'userModified'
    }

    def __init__(self, group_elements_id=None, group_element=None, name=None, ooxml_id=None, graphic_type_id=None, height=None, width=None, x_offset=None, y_offset=None, table=None, chart=None, smart_art=None, picture=None, id=None, date_created=None, user_created=None, date_modified=None, user_modified=None, local_vars_configuration=None):  # noqa: E501
        """SlideGraphicsDetails - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._group_elements_id = None
        self._group_element = None
        self._name = None
        self._ooxml_id = None
        self._graphic_type_id = None
        self._height = None
        self._width = None
        self._x_offset = None
        self._y_offset = None
        self._table = None
        self._chart = None
        self._smart_art = None
        self._picture = None
        self._id = None
        self._date_created = None
        self._user_created = None
        self._date_modified = None
        self._user_modified = None
        self.discriminator = None

        self.group_elements_id = group_elements_id
        if group_element is not None:
            self.group_element = group_element
        self.name = name
        if ooxml_id is not None:
            self.ooxml_id = ooxml_id
        if graphic_type_id is not None:
            self.graphic_type_id = graphic_type_id
        if height is not None:
            self.height = height
        if width is not None:
            self.width = width
        if x_offset is not None:
            self.x_offset = x_offset
        if y_offset is not None:
            self.y_offset = y_offset
        if table is not None:
            self.table = table
        if chart is not None:
            self.chart = chart
        if smart_art is not None:
            self.smart_art = smart_art
        if picture is not None:
            self.picture = picture
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
    def group_elements_id(self):
        """Gets the group_elements_id of this SlideGraphicsDetails.  # noqa: E501

        Foreign key to the GroupElements object  # noqa: E501

        :return: The group_elements_id of this SlideGraphicsDetails.  # noqa: E501
        :rtype: str
        """
        return self._group_elements_id

    @group_elements_id.setter
    def group_elements_id(self, group_elements_id):
        """Sets the group_elements_id of this SlideGraphicsDetails.

        Foreign key to the GroupElements object  # noqa: E501

        :param group_elements_id: The group_elements_id of this SlideGraphicsDetails.  # noqa: E501
        :type: str
        """

        self._group_elements_id = group_elements_id

    @property
    def group_element(self):
        """Gets the group_element of this SlideGraphicsDetails.  # noqa: E501


        :return: The group_element of this SlideGraphicsDetails.  # noqa: E501
        :rtype: object
        """
        return self._group_element

    @group_element.setter
    def group_element(self, group_element):
        """Sets the group_element of this SlideGraphicsDetails.


        :param group_element: The group_element of this SlideGraphicsDetails.  # noqa: E501
        :type: object
        """

        self._group_element = group_element

    @property
    def name(self):
        """Gets the name of this SlideGraphicsDetails.  # noqa: E501


        :return: The name of this SlideGraphicsDetails.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SlideGraphicsDetails.


        :param name: The name of this SlideGraphicsDetails.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def ooxml_id(self):
        """Gets the ooxml_id of this SlideGraphicsDetails.  # noqa: E501


        :return: The ooxml_id of this SlideGraphicsDetails.  # noqa: E501
        :rtype: int
        """
        return self._ooxml_id

    @ooxml_id.setter
    def ooxml_id(self, ooxml_id):
        """Sets the ooxml_id of this SlideGraphicsDetails.


        :param ooxml_id: The ooxml_id of this SlideGraphicsDetails.  # noqa: E501
        :type: int
        """

        self._ooxml_id = ooxml_id

    @property
    def graphic_type_id(self):
        """Gets the graphic_type_id of this SlideGraphicsDetails.  # noqa: E501


        :return: The graphic_type_id of this SlideGraphicsDetails.  # noqa: E501
        :rtype: int
        """
        return self._graphic_type_id

    @graphic_type_id.setter
    def graphic_type_id(self, graphic_type_id):
        """Sets the graphic_type_id of this SlideGraphicsDetails.


        :param graphic_type_id: The graphic_type_id of this SlideGraphicsDetails.  # noqa: E501
        :type: int
        """

        self._graphic_type_id = graphic_type_id

    @property
    def height(self):
        """Gets the height of this SlideGraphicsDetails.  # noqa: E501


        :return: The height of this SlideGraphicsDetails.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this SlideGraphicsDetails.


        :param height: The height of this SlideGraphicsDetails.  # noqa: E501
        :type: int
        """

        self._height = height

    @property
    def width(self):
        """Gets the width of this SlideGraphicsDetails.  # noqa: E501


        :return: The width of this SlideGraphicsDetails.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this SlideGraphicsDetails.


        :param width: The width of this SlideGraphicsDetails.  # noqa: E501
        :type: int
        """

        self._width = width

    @property
    def x_offset(self):
        """Gets the x_offset of this SlideGraphicsDetails.  # noqa: E501


        :return: The x_offset of this SlideGraphicsDetails.  # noqa: E501
        :rtype: int
        """
        return self._x_offset

    @x_offset.setter
    def x_offset(self, x_offset):
        """Sets the x_offset of this SlideGraphicsDetails.


        :param x_offset: The x_offset of this SlideGraphicsDetails.  # noqa: E501
        :type: int
        """

        self._x_offset = x_offset

    @property
    def y_offset(self):
        """Gets the y_offset of this SlideGraphicsDetails.  # noqa: E501


        :return: The y_offset of this SlideGraphicsDetails.  # noqa: E501
        :rtype: int
        """
        return self._y_offset

    @y_offset.setter
    def y_offset(self, y_offset):
        """Sets the y_offset of this SlideGraphicsDetails.


        :param y_offset: The y_offset of this SlideGraphicsDetails.  # noqa: E501
        :type: int
        """

        self._y_offset = y_offset

    @property
    def table(self):
        """Gets the table of this SlideGraphicsDetails.  # noqa: E501


        :return: The table of this SlideGraphicsDetails.  # noqa: E501
        :rtype: object
        """
        return self._table

    @table.setter
    def table(self, table):
        """Sets the table of this SlideGraphicsDetails.


        :param table: The table of this SlideGraphicsDetails.  # noqa: E501
        :type: object
        """

        self._table = table

    @property
    def chart(self):
        """Gets the chart of this SlideGraphicsDetails.  # noqa: E501


        :return: The chart of this SlideGraphicsDetails.  # noqa: E501
        :rtype: object
        """
        return self._chart

    @chart.setter
    def chart(self, chart):
        """Sets the chart of this SlideGraphicsDetails.


        :param chart: The chart of this SlideGraphicsDetails.  # noqa: E501
        :type: object
        """

        self._chart = chart

    @property
    def smart_art(self):
        """Gets the smart_art of this SlideGraphicsDetails.  # noqa: E501


        :return: The smart_art of this SlideGraphicsDetails.  # noqa: E501
        :rtype: object
        """
        return self._smart_art

    @smart_art.setter
    def smart_art(self, smart_art):
        """Sets the smart_art of this SlideGraphicsDetails.


        :param smart_art: The smart_art of this SlideGraphicsDetails.  # noqa: E501
        :type: object
        """

        self._smart_art = smart_art

    @property
    def picture(self):
        """Gets the picture of this SlideGraphicsDetails.  # noqa: E501


        :return: The picture of this SlideGraphicsDetails.  # noqa: E501
        :rtype: object
        """
        return self._picture

    @picture.setter
    def picture(self, picture):
        """Sets the picture of this SlideGraphicsDetails.


        :param picture: The picture of this SlideGraphicsDetails.  # noqa: E501
        :type: object
        """

        self._picture = picture

    @property
    def id(self):
        """Gets the id of this SlideGraphicsDetails.  # noqa: E501


        :return: The id of this SlideGraphicsDetails.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SlideGraphicsDetails.


        :param id: The id of this SlideGraphicsDetails.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def date_created(self):
        """Gets the date_created of this SlideGraphicsDetails.  # noqa: E501


        :return: The date_created of this SlideGraphicsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """Sets the date_created of this SlideGraphicsDetails.


        :param date_created: The date_created of this SlideGraphicsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_created = date_created

    @property
    def user_created(self):
        """Gets the user_created of this SlideGraphicsDetails.  # noqa: E501


        :return: The user_created of this SlideGraphicsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_created

    @user_created.setter
    def user_created(self, user_created):
        """Sets the user_created of this SlideGraphicsDetails.


        :param user_created: The user_created of this SlideGraphicsDetails.  # noqa: E501
        :type: str
        """

        self._user_created = user_created

    @property
    def date_modified(self):
        """Gets the date_modified of this SlideGraphicsDetails.  # noqa: E501


        :return: The date_modified of this SlideGraphicsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """Sets the date_modified of this SlideGraphicsDetails.


        :param date_modified: The date_modified of this SlideGraphicsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_modified = date_modified

    @property
    def user_modified(self):
        """Gets the user_modified of this SlideGraphicsDetails.  # noqa: E501


        :return: The user_modified of this SlideGraphicsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_modified

    @user_modified.setter
    def user_modified(self, user_modified):
        """Sets the user_modified of this SlideGraphicsDetails.


        :param user_modified: The user_modified of this SlideGraphicsDetails.  # noqa: E501
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
        if not isinstance(other, SlideGraphicsDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SlideGraphicsDetails):
            return True

        return self.to_dict() != other.to_dict()