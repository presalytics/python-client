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


class SlideShapeTrees(object):
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
        'slide_id': 'str',
        'group_element_id': 'str',
        'hidden': 'bool',
        'title': 'str',
        'ooxml_id': 'int',
        'svg_blob_url': 'str',
        'id': 'str'
    }

    attribute_map = {
        'slide_id': 'slideId',
        'group_element_id': 'groupElementId',
        'hidden': 'hidden',
        'title': 'title',
        'ooxml_id': 'ooxmlId',
        'svg_blob_url': 'svgBlobUrl',
        'id': 'id'
    }

    def __init__(self, slide_id=None, group_element_id=None, hidden=None, title=None, ooxml_id=None, svg_blob_url=None, id=None, local_vars_configuration=None):  # noqa: E501
        """SlideShapeTrees - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._slide_id = None
        self._group_element_id = None
        self._hidden = None
        self._title = None
        self._ooxml_id = None
        self._svg_blob_url = None
        self._id = None
        self.discriminator = None

        self.slide_id = slide_id
        self.group_element_id = group_element_id
        if hidden is not None:
            self.hidden = hidden
        self.title = title
        if ooxml_id is not None:
            self.ooxml_id = ooxml_id
        self.svg_blob_url = svg_blob_url
        if id is not None:
            self.id = id

    @property
    def slide_id(self):
        """Gets the slide_id of this SlideShapeTrees.  # noqa: E501


        :return: The slide_id of this SlideShapeTrees.  # noqa: E501
        :rtype: str
        """
        return self._slide_id

    @slide_id.setter
    def slide_id(self, slide_id):
        """Sets the slide_id of this SlideShapeTrees.


        :param slide_id: The slide_id of this SlideShapeTrees.  # noqa: E501
        :type: str
        """

        self._slide_id = slide_id

    @property
    def group_element_id(self):
        """Gets the group_element_id of this SlideShapeTrees.  # noqa: E501


        :return: The group_element_id of this SlideShapeTrees.  # noqa: E501
        :rtype: str
        """
        return self._group_element_id

    @group_element_id.setter
    def group_element_id(self, group_element_id):
        """Sets the group_element_id of this SlideShapeTrees.


        :param group_element_id: The group_element_id of this SlideShapeTrees.  # noqa: E501
        :type: str
        """

        self._group_element_id = group_element_id

    @property
    def hidden(self):
        """Gets the hidden of this SlideShapeTrees.  # noqa: E501


        :return: The hidden of this SlideShapeTrees.  # noqa: E501
        :rtype: bool
        """
        return self._hidden

    @hidden.setter
    def hidden(self, hidden):
        """Sets the hidden of this SlideShapeTrees.


        :param hidden: The hidden of this SlideShapeTrees.  # noqa: E501
        :type: bool
        """

        self._hidden = hidden

    @property
    def title(self):
        """Gets the title of this SlideShapeTrees.  # noqa: E501


        :return: The title of this SlideShapeTrees.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this SlideShapeTrees.


        :param title: The title of this SlideShapeTrees.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def ooxml_id(self):
        """Gets the ooxml_id of this SlideShapeTrees.  # noqa: E501


        :return: The ooxml_id of this SlideShapeTrees.  # noqa: E501
        :rtype: int
        """
        return self._ooxml_id

    @ooxml_id.setter
    def ooxml_id(self, ooxml_id):
        """Sets the ooxml_id of this SlideShapeTrees.


        :param ooxml_id: The ooxml_id of this SlideShapeTrees.  # noqa: E501
        :type: int
        """

        self._ooxml_id = ooxml_id

    @property
    def svg_blob_url(self):
        """Gets the svg_blob_url of this SlideShapeTrees.  # noqa: E501


        :return: The svg_blob_url of this SlideShapeTrees.  # noqa: E501
        :rtype: str
        """
        return self._svg_blob_url

    @svg_blob_url.setter
    def svg_blob_url(self, svg_blob_url):
        """Sets the svg_blob_url of this SlideShapeTrees.


        :param svg_blob_url: The svg_blob_url of this SlideShapeTrees.  # noqa: E501
        :type: str
        """

        self._svg_blob_url = svg_blob_url

    @property
    def id(self):
        """Gets the id of this SlideShapeTrees.  # noqa: E501


        :return: The id of this SlideShapeTrees.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SlideShapeTrees.


        :param id: The id of this SlideShapeTrees.  # noqa: E501
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
        if not isinstance(other, SlideShapeTrees):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SlideShapeTrees):
            return True

        return self.to_dict() != other.to_dict()
