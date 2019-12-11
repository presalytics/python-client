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

from presalytics_ooxml_automation.configuration import Configuration


class SharedGradientFills(object):
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
        'fill_map_id': 'str',
        'angle': 'int',
        'rotate_with_shape': 'bool',
        'is_path': 'bool',
        'path_type': 'str',
        'id': 'str'
    }

    attribute_map = {
        'fill_map_id': 'fillMapId',
        'angle': 'angle',
        'rotate_with_shape': 'rotateWithShape',
        'is_path': 'isPath',
        'path_type': 'pathType',
        'id': 'id'
    }

    def __init__(self, fill_map_id=None, angle=None, rotate_with_shape=None, is_path=None, path_type=None, id=None, local_vars_configuration=None):  # noqa: E501
        """SharedGradientFills - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._fill_map_id = None
        self._angle = None
        self._rotate_with_shape = None
        self._is_path = None
        self._path_type = None
        self._id = None
        self.discriminator = None

        self.fill_map_id = fill_map_id
        self.angle = angle
        if rotate_with_shape is not None:
            self.rotate_with_shape = rotate_with_shape
        if is_path is not None:
            self.is_path = is_path
        self.path_type = path_type
        if id is not None:
            self.id = id

    @property
    def fill_map_id(self):
        """Gets the fill_map_id of this SharedGradientFills.  # noqa: E501


        :return: The fill_map_id of this SharedGradientFills.  # noqa: E501
        :rtype: str
        """
        return self._fill_map_id

    @fill_map_id.setter
    def fill_map_id(self, fill_map_id):
        """Sets the fill_map_id of this SharedGradientFills.


        :param fill_map_id: The fill_map_id of this SharedGradientFills.  # noqa: E501
        :type: str
        """

        self._fill_map_id = fill_map_id

    @property
    def angle(self):
        """Gets the angle of this SharedGradientFills.  # noqa: E501


        :return: The angle of this SharedGradientFills.  # noqa: E501
        :rtype: int
        """
        return self._angle

    @angle.setter
    def angle(self, angle):
        """Sets the angle of this SharedGradientFills.


        :param angle: The angle of this SharedGradientFills.  # noqa: E501
        :type: int
        """

        self._angle = angle

    @property
    def rotate_with_shape(self):
        """Gets the rotate_with_shape of this SharedGradientFills.  # noqa: E501


        :return: The rotate_with_shape of this SharedGradientFills.  # noqa: E501
        :rtype: bool
        """
        return self._rotate_with_shape

    @rotate_with_shape.setter
    def rotate_with_shape(self, rotate_with_shape):
        """Sets the rotate_with_shape of this SharedGradientFills.


        :param rotate_with_shape: The rotate_with_shape of this SharedGradientFills.  # noqa: E501
        :type: bool
        """

        self._rotate_with_shape = rotate_with_shape

    @property
    def is_path(self):
        """Gets the is_path of this SharedGradientFills.  # noqa: E501


        :return: The is_path of this SharedGradientFills.  # noqa: E501
        :rtype: bool
        """
        return self._is_path

    @is_path.setter
    def is_path(self, is_path):
        """Sets the is_path of this SharedGradientFills.


        :param is_path: The is_path of this SharedGradientFills.  # noqa: E501
        :type: bool
        """

        self._is_path = is_path

    @property
    def path_type(self):
        """Gets the path_type of this SharedGradientFills.  # noqa: E501


        :return: The path_type of this SharedGradientFills.  # noqa: E501
        :rtype: str
        """
        return self._path_type

    @path_type.setter
    def path_type(self, path_type):
        """Sets the path_type of this SharedGradientFills.


        :param path_type: The path_type of this SharedGradientFills.  # noqa: E501
        :type: str
        """

        self._path_type = path_type

    @property
    def id(self):
        """Gets the id of this SharedGradientFills.  # noqa: E501


        :return: The id of this SharedGradientFills.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SharedGradientFills.


        :param id: The id of this SharedGradientFills.  # noqa: E501
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
        if not isinstance(other, SharedGradientFills):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SharedGradientFills):
            return True

        return self.to_dict() != other.to_dict()
