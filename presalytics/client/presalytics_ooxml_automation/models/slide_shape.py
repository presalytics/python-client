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


class SlideShape(object):
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
        'height': 'int',
        'width': 'int',
        'x_offset': 'int',
        'y_offset': 'int',
        'group_elements_id': 'str',
        'ooxml_id': 'int',
        'svg_blob_url': 'str',
        'preset_type_id': 'str',
        'free_form_path_xml': 'str',
        'is_theme_fill': 'bool',
        'is_theme_effect': 'bool',
        'is_theme_line': 'bool',
        'flip_horizontal': 'bool',
        'flip_vertical': 'bool',
        'rotation': 'int',
        'hidden': 'bool',
        'id': 'str'
    }

    attribute_map = {
        'height': 'height',
        'width': 'width',
        'x_offset': 'xOffset',
        'y_offset': 'yOffset',
        'group_elements_id': 'groupElementsId',
        'ooxml_id': 'ooxmlId',
        'svg_blob_url': 'svgBlobUrl',
        'preset_type_id': 'presetTypeId',
        'free_form_path_xml': 'freeFormPathXml',
        'is_theme_fill': 'isThemeFill',
        'is_theme_effect': 'isThemeEffect',
        'is_theme_line': 'isThemeLine',
        'flip_horizontal': 'flipHorizontal',
        'flip_vertical': 'flipVertical',
        'rotation': 'rotation',
        'hidden': 'hidden',
        'id': 'id'
    }

    def __init__(self, height=None, width=None, x_offset=None, y_offset=None, group_elements_id=None, ooxml_id=None, svg_blob_url=None, preset_type_id=None, free_form_path_xml=None, is_theme_fill=None, is_theme_effect=None, is_theme_line=None, flip_horizontal=None, flip_vertical=None, rotation=None, hidden=None, id=None, local_vars_configuration=None):  # noqa: E501
        """SlideShape - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._height = None
        self._width = None
        self._x_offset = None
        self._y_offset = None
        self._group_elements_id = None
        self._ooxml_id = None
        self._svg_blob_url = None
        self._preset_type_id = None
        self._free_form_path_xml = None
        self._is_theme_fill = None
        self._is_theme_effect = None
        self._is_theme_line = None
        self._flip_horizontal = None
        self._flip_vertical = None
        self._rotation = None
        self._hidden = None
        self._id = None
        self.discriminator = None

        if height is not None:
            self.height = height
        if width is not None:
            self.width = width
        if x_offset is not None:
            self.x_offset = x_offset
        if y_offset is not None:
            self.y_offset = y_offset
        self.group_elements_id = group_elements_id
        if ooxml_id is not None:
            self.ooxml_id = ooxml_id
        self.svg_blob_url = svg_blob_url
        self.preset_type_id = preset_type_id
        self.free_form_path_xml = free_form_path_xml
        if is_theme_fill is not None:
            self.is_theme_fill = is_theme_fill
        if is_theme_effect is not None:
            self.is_theme_effect = is_theme_effect
        if is_theme_line is not None:
            self.is_theme_line = is_theme_line
        if flip_horizontal is not None:
            self.flip_horizontal = flip_horizontal
        if flip_vertical is not None:
            self.flip_vertical = flip_vertical
        if rotation is not None:
            self.rotation = rotation
        if hidden is not None:
            self.hidden = hidden
        if id is not None:
            self.id = id

    @property
    def height(self):
        """Gets the height of this SlideShape.  # noqa: E501


        :return: The height of this SlideShape.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this SlideShape.


        :param height: The height of this SlideShape.  # noqa: E501
        :type: int
        """

        self._height = height

    @property
    def width(self):
        """Gets the width of this SlideShape.  # noqa: E501


        :return: The width of this SlideShape.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this SlideShape.


        :param width: The width of this SlideShape.  # noqa: E501
        :type: int
        """

        self._width = width

    @property
    def x_offset(self):
        """Gets the x_offset of this SlideShape.  # noqa: E501


        :return: The x_offset of this SlideShape.  # noqa: E501
        :rtype: int
        """
        return self._x_offset

    @x_offset.setter
    def x_offset(self, x_offset):
        """Sets the x_offset of this SlideShape.


        :param x_offset: The x_offset of this SlideShape.  # noqa: E501
        :type: int
        """

        self._x_offset = x_offset

    @property
    def y_offset(self):
        """Gets the y_offset of this SlideShape.  # noqa: E501


        :return: The y_offset of this SlideShape.  # noqa: E501
        :rtype: int
        """
        return self._y_offset

    @y_offset.setter
    def y_offset(self, y_offset):
        """Sets the y_offset of this SlideShape.


        :param y_offset: The y_offset of this SlideShape.  # noqa: E501
        :type: int
        """

        self._y_offset = y_offset

    @property
    def group_elements_id(self):
        """Gets the group_elements_id of this SlideShape.  # noqa: E501


        :return: The group_elements_id of this SlideShape.  # noqa: E501
        :rtype: str
        """
        return self._group_elements_id

    @group_elements_id.setter
    def group_elements_id(self, group_elements_id):
        """Sets the group_elements_id of this SlideShape.


        :param group_elements_id: The group_elements_id of this SlideShape.  # noqa: E501
        :type: str
        """

        self._group_elements_id = group_elements_id

    @property
    def ooxml_id(self):
        """Gets the ooxml_id of this SlideShape.  # noqa: E501


        :return: The ooxml_id of this SlideShape.  # noqa: E501
        :rtype: int
        """
        return self._ooxml_id

    @ooxml_id.setter
    def ooxml_id(self, ooxml_id):
        """Sets the ooxml_id of this SlideShape.


        :param ooxml_id: The ooxml_id of this SlideShape.  # noqa: E501
        :type: int
        """

        self._ooxml_id = ooxml_id

    @property
    def svg_blob_url(self):
        """Gets the svg_blob_url of this SlideShape.  # noqa: E501


        :return: The svg_blob_url of this SlideShape.  # noqa: E501
        :rtype: str
        """
        return self._svg_blob_url

    @svg_blob_url.setter
    def svg_blob_url(self, svg_blob_url):
        """Sets the svg_blob_url of this SlideShape.


        :param svg_blob_url: The svg_blob_url of this SlideShape.  # noqa: E501
        :type: str
        """

        self._svg_blob_url = svg_blob_url

    @property
    def preset_type_id(self):
        """Gets the preset_type_id of this SlideShape.  # noqa: E501


        :return: The preset_type_id of this SlideShape.  # noqa: E501
        :rtype: str
        """
        return self._preset_type_id

    @preset_type_id.setter
    def preset_type_id(self, preset_type_id):
        """Sets the preset_type_id of this SlideShape.


        :param preset_type_id: The preset_type_id of this SlideShape.  # noqa: E501
        :type: str
        """

        self._preset_type_id = preset_type_id

    @property
    def free_form_path_xml(self):
        """Gets the free_form_path_xml of this SlideShape.  # noqa: E501


        :return: The free_form_path_xml of this SlideShape.  # noqa: E501
        :rtype: str
        """
        return self._free_form_path_xml

    @free_form_path_xml.setter
    def free_form_path_xml(self, free_form_path_xml):
        """Sets the free_form_path_xml of this SlideShape.


        :param free_form_path_xml: The free_form_path_xml of this SlideShape.  # noqa: E501
        :type: str
        """

        self._free_form_path_xml = free_form_path_xml

    @property
    def is_theme_fill(self):
        """Gets the is_theme_fill of this SlideShape.  # noqa: E501


        :return: The is_theme_fill of this SlideShape.  # noqa: E501
        :rtype: bool
        """
        return self._is_theme_fill

    @is_theme_fill.setter
    def is_theme_fill(self, is_theme_fill):
        """Sets the is_theme_fill of this SlideShape.


        :param is_theme_fill: The is_theme_fill of this SlideShape.  # noqa: E501
        :type: bool
        """

        self._is_theme_fill = is_theme_fill

    @property
    def is_theme_effect(self):
        """Gets the is_theme_effect of this SlideShape.  # noqa: E501


        :return: The is_theme_effect of this SlideShape.  # noqa: E501
        :rtype: bool
        """
        return self._is_theme_effect

    @is_theme_effect.setter
    def is_theme_effect(self, is_theme_effect):
        """Sets the is_theme_effect of this SlideShape.


        :param is_theme_effect: The is_theme_effect of this SlideShape.  # noqa: E501
        :type: bool
        """

        self._is_theme_effect = is_theme_effect

    @property
    def is_theme_line(self):
        """Gets the is_theme_line of this SlideShape.  # noqa: E501


        :return: The is_theme_line of this SlideShape.  # noqa: E501
        :rtype: bool
        """
        return self._is_theme_line

    @is_theme_line.setter
    def is_theme_line(self, is_theme_line):
        """Sets the is_theme_line of this SlideShape.


        :param is_theme_line: The is_theme_line of this SlideShape.  # noqa: E501
        :type: bool
        """

        self._is_theme_line = is_theme_line

    @property
    def flip_horizontal(self):
        """Gets the flip_horizontal of this SlideShape.  # noqa: E501


        :return: The flip_horizontal of this SlideShape.  # noqa: E501
        :rtype: bool
        """
        return self._flip_horizontal

    @flip_horizontal.setter
    def flip_horizontal(self, flip_horizontal):
        """Sets the flip_horizontal of this SlideShape.


        :param flip_horizontal: The flip_horizontal of this SlideShape.  # noqa: E501
        :type: bool
        """

        self._flip_horizontal = flip_horizontal

    @property
    def flip_vertical(self):
        """Gets the flip_vertical of this SlideShape.  # noqa: E501


        :return: The flip_vertical of this SlideShape.  # noqa: E501
        :rtype: bool
        """
        return self._flip_vertical

    @flip_vertical.setter
    def flip_vertical(self, flip_vertical):
        """Sets the flip_vertical of this SlideShape.


        :param flip_vertical: The flip_vertical of this SlideShape.  # noqa: E501
        :type: bool
        """

        self._flip_vertical = flip_vertical

    @property
    def rotation(self):
        """Gets the rotation of this SlideShape.  # noqa: E501


        :return: The rotation of this SlideShape.  # noqa: E501
        :rtype: int
        """
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        """Sets the rotation of this SlideShape.


        :param rotation: The rotation of this SlideShape.  # noqa: E501
        :type: int
        """

        self._rotation = rotation

    @property
    def hidden(self):
        """Gets the hidden of this SlideShape.  # noqa: E501


        :return: The hidden of this SlideShape.  # noqa: E501
        :rtype: bool
        """
        return self._hidden

    @hidden.setter
    def hidden(self, hidden):
        """Sets the hidden of this SlideShape.


        :param hidden: The hidden of this SlideShape.  # noqa: E501
        :type: bool
        """

        self._hidden = hidden

    @property
    def id(self):
        """Gets the id of this SlideShape.  # noqa: E501


        :return: The id of this SlideShape.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SlideShape.


        :param id: The id of this SlideShape.  # noqa: E501
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
        if not isinstance(other, SlideShape):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SlideShape):
            return True

        return self.to_dict() != other.to_dict()
