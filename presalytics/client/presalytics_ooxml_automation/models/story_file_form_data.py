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


class StoryFileFormData(object):
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
        'file': 'file',
        'story_id': 'str'
    }

    attribute_map = {
        'file': 'file',
        'story_id': 'storyId'
    }

    def __init__(self, file=None, story_id=None):  # noqa: E501
        """StoryFileFormData - a model defined in OpenAPI"""  # noqa: E501

        self._file = None
        self._story_id = None
        self.discriminator = None

        self.file = file
        self.story_id = story_id

    @property
    def file(self):
        """Gets the file of this StoryFileFormData.  # noqa: E501

        The file to upload.  Must be of type .pptx, ppt  # noqa: E501

        :return: The file of this StoryFileFormData.  # noqa: E501
        :rtype: file
        """
        return self._file

    @file.setter
    def file(self, file):
        """Sets the file of this StoryFileFormData.

        The file to upload.  Must be of type .pptx, ppt  # noqa: E501

        :param file: The file of this StoryFileFormData.  # noqa: E501
        :type: file
        """
        if file is None:
            raise ValueError("Invalid value for `file`, must not be `None`")  # noqa: E501

        self._file = file

    @property
    def story_id(self):
        """Gets the story_id of this StoryFileFormData.  # noqa: E501

        The story_id of the document being uploaded.  # noqa: E501

        :return: The story_id of this StoryFileFormData.  # noqa: E501
        :rtype: str
        """
        return self._story_id

    @story_id.setter
    def story_id(self, story_id):
        """Sets the story_id of this StoryFileFormData.

        The story_id of the document being uploaded.  # noqa: E501

        :param story_id: The story_id of this StoryFileFormData.  # noqa: E501
        :type: str
        """
        if story_id is None:
            raise ValueError("Invalid value for `story_id`, must not be `None`")  # noqa: E501

        self._story_id = story_id

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
        if not isinstance(other, StoryFileFormData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
