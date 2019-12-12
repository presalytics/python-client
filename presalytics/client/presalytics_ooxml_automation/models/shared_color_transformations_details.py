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


class SharedColorTransformationsDetails(object):
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
        'color_transformation_attributes': 'object',
        'solid_fills_id': 'str',
        'parent_solid_fill': 'object',
        'id': 'str',
        'date_created': 'datetime',
        'user_created': 'str',
        'date_modified': 'datetime',
        'user_modified': 'str'
    }

    attribute_map = {
        'name': 'name',
        'color_transformation_attributes': 'colorTransformationAttributes',
        'solid_fills_id': 'solidFillsId',
        'parent_solid_fill': 'parentSolidFill',
        'id': 'id',
        'date_created': 'dateCreated',
        'user_created': 'userCreated',
        'date_modified': 'dateModified',
        'user_modified': 'userModified'
    }

    def __init__(self, name=None, color_transformation_attributes=None, solid_fills_id=None, parent_solid_fill=None, id=None, date_created=None, user_created=None, date_modified=None, user_modified=None, local_vars_configuration=None):  # noqa: E501
        """SharedColorTransformationsDetails - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._color_transformation_attributes = None
        self._solid_fills_id = None
        self._parent_solid_fill = None
        self._id = None
        self._date_created = None
        self._user_created = None
        self._date_modified = None
        self._user_modified = None
        self.discriminator = None

        self.name = name
        self.color_transformation_attributes = color_transformation_attributes
        self.solid_fills_id = solid_fills_id
        if parent_solid_fill is not None:
            self.parent_solid_fill = parent_solid_fill
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
        """Gets the name of this SharedColorTransformationsDetails.  # noqa: E501


        :return: The name of this SharedColorTransformationsDetails.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SharedColorTransformationsDetails.


        :param name: The name of this SharedColorTransformationsDetails.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def color_transformation_attributes(self):
        """Gets the color_transformation_attributes of this SharedColorTransformationsDetails.  # noqa: E501


        :return: The color_transformation_attributes of this SharedColorTransformationsDetails.  # noqa: E501
        :rtype: object
        """
        return self._color_transformation_attributes

    @color_transformation_attributes.setter
    def color_transformation_attributes(self, color_transformation_attributes):
        """Sets the color_transformation_attributes of this SharedColorTransformationsDetails.


        :param color_transformation_attributes: The color_transformation_attributes of this SharedColorTransformationsDetails.  # noqa: E501
        :type: object
        """

        self._color_transformation_attributes = color_transformation_attributes

    @property
    def solid_fills_id(self):
        """Gets the solid_fills_id of this SharedColorTransformationsDetails.  # noqa: E501


        :return: The solid_fills_id of this SharedColorTransformationsDetails.  # noqa: E501
        :rtype: str
        """
        return self._solid_fills_id

    @solid_fills_id.setter
    def solid_fills_id(self, solid_fills_id):
        """Sets the solid_fills_id of this SharedColorTransformationsDetails.


        :param solid_fills_id: The solid_fills_id of this SharedColorTransformationsDetails.  # noqa: E501
        :type: str
        """

        self._solid_fills_id = solid_fills_id

    @property
    def parent_solid_fill(self):
        """Gets the parent_solid_fill of this SharedColorTransformationsDetails.  # noqa: E501


        :return: The parent_solid_fill of this SharedColorTransformationsDetails.  # noqa: E501
        :rtype: object
        """
        return self._parent_solid_fill

    @parent_solid_fill.setter
    def parent_solid_fill(self, parent_solid_fill):
        """Sets the parent_solid_fill of this SharedColorTransformationsDetails.


        :param parent_solid_fill: The parent_solid_fill of this SharedColorTransformationsDetails.  # noqa: E501
        :type: object
        """

        self._parent_solid_fill = parent_solid_fill

    @property
    def id(self):
        """Gets the id of this SharedColorTransformationsDetails.  # noqa: E501


        :return: The id of this SharedColorTransformationsDetails.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SharedColorTransformationsDetails.


        :param id: The id of this SharedColorTransformationsDetails.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def date_created(self):
        """Gets the date_created of this SharedColorTransformationsDetails.  # noqa: E501


        :return: The date_created of this SharedColorTransformationsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """Sets the date_created of this SharedColorTransformationsDetails.


        :param date_created: The date_created of this SharedColorTransformationsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_created = date_created

    @property
    def user_created(self):
        """Gets the user_created of this SharedColorTransformationsDetails.  # noqa: E501


        :return: The user_created of this SharedColorTransformationsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_created

    @user_created.setter
    def user_created(self, user_created):
        """Sets the user_created of this SharedColorTransformationsDetails.


        :param user_created: The user_created of this SharedColorTransformationsDetails.  # noqa: E501
        :type: str
        """

        self._user_created = user_created

    @property
    def date_modified(self):
        """Gets the date_modified of this SharedColorTransformationsDetails.  # noqa: E501


        :return: The date_modified of this SharedColorTransformationsDetails.  # noqa: E501
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """Sets the date_modified of this SharedColorTransformationsDetails.


        :param date_modified: The date_modified of this SharedColorTransformationsDetails.  # noqa: E501
        :type: datetime
        """

        self._date_modified = date_modified

    @property
    def user_modified(self):
        """Gets the user_modified of this SharedColorTransformationsDetails.  # noqa: E501


        :return: The user_modified of this SharedColorTransformationsDetails.  # noqa: E501
        :rtype: str
        """
        return self._user_modified

    @user_modified.setter
    def user_modified(self, user_modified):
        """Sets the user_modified of this SharedColorTransformationsDetails.


        :param user_modified: The user_modified of this SharedColorTransformationsDetails.  # noqa: E501
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
        if not isinstance(other, SharedColorTransformationsDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SharedColorTransformationsDetails):
            return True

        return self.to_dict() != other.to_dict()
