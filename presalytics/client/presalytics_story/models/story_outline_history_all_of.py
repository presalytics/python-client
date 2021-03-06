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


class StoryOutlineHistoryAllOf(object):
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
        'collaborator_user_id': 'str',
        'outline': 'str',
        'revision_number': 'int',
        'story_id': 'str'
    }

    attribute_map = {
        'collaborator_user_id': 'collaborator_user_id',
        'outline': 'outline',
        'revision_number': 'revision_number',
        'story_id': 'story_id'
    }

    def __init__(self, collaborator_user_id=None, outline=None, revision_number=None, story_id=None):  # noqa: E501
        """StoryOutlineHistoryAllOf - a model defined in OpenAPI"""  # noqa: E501

        self._collaborator_user_id = None
        self._outline = None
        self._revision_number = None
        self._story_id = None
        self.discriminator = None

        if collaborator_user_id is not None:
            self.collaborator_user_id = collaborator_user_id
        if outline is not None:
            self.outline = outline
        if revision_number is not None:
            self.revision_number = revision_number
        if story_id is not None:
            self.story_id = story_id

    @property
    def collaborator_user_id(self):
        """Gets the collaborator_user_id of this StoryOutlineHistoryAllOf.  # noqa: E501


        :return: The collaborator_user_id of this StoryOutlineHistoryAllOf.  # noqa: E501
        :rtype: str
        """
        return self._collaborator_user_id

    @collaborator_user_id.setter
    def collaborator_user_id(self, collaborator_user_id):
        """Sets the collaborator_user_id of this StoryOutlineHistoryAllOf.


        :param collaborator_user_id: The collaborator_user_id of this StoryOutlineHistoryAllOf.  # noqa: E501
        :type: str
        """

        self._collaborator_user_id = collaborator_user_id

    @property
    def outline(self):
        """Gets the outline of this StoryOutlineHistoryAllOf.  # noqa: E501


        :return: The outline of this StoryOutlineHistoryAllOf.  # noqa: E501
        :rtype: str
        """
        return self._outline

    @outline.setter
    def outline(self, outline):
        """Sets the outline of this StoryOutlineHistoryAllOf.


        :param outline: The outline of this StoryOutlineHistoryAllOf.  # noqa: E501
        :type: str
        """

        self._outline = outline

    @property
    def revision_number(self):
        """Gets the revision_number of this StoryOutlineHistoryAllOf.  # noqa: E501


        :return: The revision_number of this StoryOutlineHistoryAllOf.  # noqa: E501
        :rtype: int
        """
        return self._revision_number

    @revision_number.setter
    def revision_number(self, revision_number):
        """Sets the revision_number of this StoryOutlineHistoryAllOf.


        :param revision_number: The revision_number of this StoryOutlineHistoryAllOf.  # noqa: E501
        :type: int
        """

        self._revision_number = revision_number

    @property
    def story_id(self):
        """Gets the story_id of this StoryOutlineHistoryAllOf.  # noqa: E501


        :return: The story_id of this StoryOutlineHistoryAllOf.  # noqa: E501
        :rtype: str
        """
        return self._story_id

    @story_id.setter
    def story_id(self, story_id):
        """Sets the story_id of this StoryOutlineHistoryAllOf.


        :param story_id: The story_id of this StoryOutlineHistoryAllOf.  # noqa: E501
        :type: str
        """

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
        if not isinstance(other, StoryOutlineHistoryAllOf):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
