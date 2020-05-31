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


class StoryOutlineHistory(object):
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
        'created_at': 'datetime',
        'created_by': 'str',
        'id': 'str',
        'updated_at': 'datetime',
        'updated_by': 'str',
        'collaborator_user_id': 'str',
        'outline': 'str',
        'revision_number': 'int',
        'story_id': 'str'
    }

    attribute_map = {
        'created_at': 'created_at',
        'created_by': 'created_by',
        'id': 'id',
        'updated_at': 'updated_at',
        'updated_by': 'updated_by',
        'collaborator_user_id': 'collaborator_user_id',
        'outline': 'outline',
        'revision_number': 'revision_number',
        'story_id': 'story_id'
    }

    def __init__(self, created_at=None, created_by=None, id=None, updated_at=None, updated_by=None, collaborator_user_id=None, outline=None, revision_number=None, story_id=None):  # noqa: E501
        """StoryOutlineHistory - a model defined in OpenAPI"""  # noqa: E501

        self._created_at = None
        self._created_by = None
        self._id = None
        self._updated_at = None
        self._updated_by = None
        self._collaborator_user_id = None
        self._outline = None
        self._revision_number = None
        self._story_id = None
        self.discriminator = None

        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if id is not None:
            self.id = id
        if updated_at is not None:
            self.updated_at = updated_at
        if updated_by is not None:
            self.updated_by = updated_by
        if collaborator_user_id is not None:
            self.collaborator_user_id = collaborator_user_id
        if outline is not None:
            self.outline = outline
        if revision_number is not None:
            self.revision_number = revision_number
        if story_id is not None:
            self.story_id = story_id

    @property
    def created_at(self):
        """Gets the created_at of this StoryOutlineHistory.  # noqa: E501


        :return: The created_at of this StoryOutlineHistory.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this StoryOutlineHistory.


        :param created_at: The created_at of this StoryOutlineHistory.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this StoryOutlineHistory.  # noqa: E501


        :return: The created_by of this StoryOutlineHistory.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this StoryOutlineHistory.


        :param created_by: The created_by of this StoryOutlineHistory.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def id(self):
        """Gets the id of this StoryOutlineHistory.  # noqa: E501


        :return: The id of this StoryOutlineHistory.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this StoryOutlineHistory.


        :param id: The id of this StoryOutlineHistory.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def updated_at(self):
        """Gets the updated_at of this StoryOutlineHistory.  # noqa: E501


        :return: The updated_at of this StoryOutlineHistory.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this StoryOutlineHistory.


        :param updated_at: The updated_at of this StoryOutlineHistory.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def updated_by(self):
        """Gets the updated_by of this StoryOutlineHistory.  # noqa: E501


        :return: The updated_by of this StoryOutlineHistory.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this StoryOutlineHistory.


        :param updated_by: The updated_by of this StoryOutlineHistory.  # noqa: E501
        :type: str
        """

        self._updated_by = updated_by

    @property
    def collaborator_user_id(self):
        """Gets the collaborator_user_id of this StoryOutlineHistory.  # noqa: E501


        :return: The collaborator_user_id of this StoryOutlineHistory.  # noqa: E501
        :rtype: str
        """
        return self._collaborator_user_id

    @collaborator_user_id.setter
    def collaborator_user_id(self, collaborator_user_id):
        """Sets the collaborator_user_id of this StoryOutlineHistory.


        :param collaborator_user_id: The collaborator_user_id of this StoryOutlineHistory.  # noqa: E501
        :type: str
        """

        self._collaborator_user_id = collaborator_user_id

    @property
    def outline(self):
        """Gets the outline of this StoryOutlineHistory.  # noqa: E501


        :return: The outline of this StoryOutlineHistory.  # noqa: E501
        :rtype: str
        """
        return self._outline

    @outline.setter
    def outline(self, outline):
        """Sets the outline of this StoryOutlineHistory.


        :param outline: The outline of this StoryOutlineHistory.  # noqa: E501
        :type: str
        """

        self._outline = outline

    @property
    def revision_number(self):
        """Gets the revision_number of this StoryOutlineHistory.  # noqa: E501


        :return: The revision_number of this StoryOutlineHistory.  # noqa: E501
        :rtype: int
        """
        return self._revision_number

    @revision_number.setter
    def revision_number(self, revision_number):
        """Sets the revision_number of this StoryOutlineHistory.


        :param revision_number: The revision_number of this StoryOutlineHistory.  # noqa: E501
        :type: int
        """

        self._revision_number = revision_number

    @property
    def story_id(self):
        """Gets the story_id of this StoryOutlineHistory.  # noqa: E501


        :return: The story_id of this StoryOutlineHistory.  # noqa: E501
        :rtype: str
        """
        return self._story_id

    @story_id.setter
    def story_id(self, story_id):
        """Sets the story_id of this StoryOutlineHistory.


        :param story_id: The story_id of this StoryOutlineHistory.  # noqa: E501
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
        if not isinstance(other, StoryOutlineHistory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
