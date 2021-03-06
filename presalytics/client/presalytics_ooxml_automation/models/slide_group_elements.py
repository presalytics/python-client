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


class SlideGroupElements(object):
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
        'shape_tree_id': 'str',
        'parent_group_element_id': 'str',
        'group_element_type_id': 'int',
        'group_element_type_pk': 'str',
        'ultimate_parent_shape_tree_id': 'str',
        'id': 'str'
    }

    attribute_map = {
        'shape_tree_id': 'shapeTreeId',
        'parent_group_element_id': 'parentGroupElementId',
        'group_element_type_id': 'groupElementTypeId',
        'group_element_type_pk': 'groupElementTypePk',
        'ultimate_parent_shape_tree_id': 'ultimateParentShapeTreeId',
        'id': 'id'
    }

    def __init__(self, shape_tree_id=None, parent_group_element_id=None, group_element_type_id=None, group_element_type_pk=None, ultimate_parent_shape_tree_id=None, id=None):  # noqa: E501
        """SlideGroupElements - a model defined in OpenAPI"""  # noqa: E501

        self._shape_tree_id = None
        self._parent_group_element_id = None
        self._group_element_type_id = None
        self._group_element_type_pk = None
        self._ultimate_parent_shape_tree_id = None
        self._id = None
        self.discriminator = None

        self.shape_tree_id = shape_tree_id
        self.parent_group_element_id = parent_group_element_id
        if group_element_type_id is not None:
            self.group_element_type_id = group_element_type_id
        self.group_element_type_pk = group_element_type_pk
        self.ultimate_parent_shape_tree_id = ultimate_parent_shape_tree_id
        if id is not None:
            self.id = id

    @property
    def shape_tree_id(self):
        """Gets the shape_tree_id of this SlideGroupElements.  # noqa: E501


        :return: The shape_tree_id of this SlideGroupElements.  # noqa: E501
        :rtype: str
        """
        return self._shape_tree_id

    @shape_tree_id.setter
    def shape_tree_id(self, shape_tree_id):
        """Sets the shape_tree_id of this SlideGroupElements.


        :param shape_tree_id: The shape_tree_id of this SlideGroupElements.  # noqa: E501
        :type: str
        """

        self._shape_tree_id = shape_tree_id

    @property
    def parent_group_element_id(self):
        """Gets the parent_group_element_id of this SlideGroupElements.  # noqa: E501


        :return: The parent_group_element_id of this SlideGroupElements.  # noqa: E501
        :rtype: str
        """
        return self._parent_group_element_id

    @parent_group_element_id.setter
    def parent_group_element_id(self, parent_group_element_id):
        """Sets the parent_group_element_id of this SlideGroupElements.


        :param parent_group_element_id: The parent_group_element_id of this SlideGroupElements.  # noqa: E501
        :type: str
        """

        self._parent_group_element_id = parent_group_element_id

    @property
    def group_element_type_id(self):
        """Gets the group_element_type_id of this SlideGroupElements.  # noqa: E501


        :return: The group_element_type_id of this SlideGroupElements.  # noqa: E501
        :rtype: int
        """
        return self._group_element_type_id

    @group_element_type_id.setter
    def group_element_type_id(self, group_element_type_id):
        """Sets the group_element_type_id of this SlideGroupElements.


        :param group_element_type_id: The group_element_type_id of this SlideGroupElements.  # noqa: E501
        :type: int
        """

        self._group_element_type_id = group_element_type_id

    @property
    def group_element_type_pk(self):
        """Gets the group_element_type_pk of this SlideGroupElements.  # noqa: E501


        :return: The group_element_type_pk of this SlideGroupElements.  # noqa: E501
        :rtype: str
        """
        return self._group_element_type_pk

    @group_element_type_pk.setter
    def group_element_type_pk(self, group_element_type_pk):
        """Sets the group_element_type_pk of this SlideGroupElements.


        :param group_element_type_pk: The group_element_type_pk of this SlideGroupElements.  # noqa: E501
        :type: str
        """

        self._group_element_type_pk = group_element_type_pk

    @property
    def ultimate_parent_shape_tree_id(self):
        """Gets the ultimate_parent_shape_tree_id of this SlideGroupElements.  # noqa: E501


        :return: The ultimate_parent_shape_tree_id of this SlideGroupElements.  # noqa: E501
        :rtype: str
        """
        return self._ultimate_parent_shape_tree_id

    @ultimate_parent_shape_tree_id.setter
    def ultimate_parent_shape_tree_id(self, ultimate_parent_shape_tree_id):
        """Sets the ultimate_parent_shape_tree_id of this SlideGroupElements.


        :param ultimate_parent_shape_tree_id: The ultimate_parent_shape_tree_id of this SlideGroupElements.  # noqa: E501
        :type: str
        """

        self._ultimate_parent_shape_tree_id = ultimate_parent_shape_tree_id

    @property
    def id(self):
        """Gets the id of this SlideGroupElements.  # noqa: E501


        :return: The id of this SlideGroupElements.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SlideGroupElements.


        :param id: The id of this SlideGroupElements.  # noqa: E501
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
        if not isinstance(other, SlideGroupElements):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
