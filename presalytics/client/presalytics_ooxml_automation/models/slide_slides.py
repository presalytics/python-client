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


class SlideSlides(object):
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
        'document_id': 'str',
        'number': 'int',
        'ooxml_id': 'int',
        'svg_blob_url': 'str',
        'slide_document_url': 'str',
        'base_element_blob_url': 'str',
        'changed_base_element_blob_url': 'str',
        'package_uri': 'str',
        'name': 'str',
        'id': 'str'
    }

    attribute_map = {
        'document_id': 'documentId',
        'number': 'number',
        'ooxml_id': 'ooxmlId',
        'svg_blob_url': 'svgBlobUrl',
        'slide_document_url': 'slideDocumentUrl',
        'base_element_blob_url': 'baseElementBlobUrl',
        'changed_base_element_blob_url': 'changedBaseElementBlobUrl',
        'package_uri': 'packageUri',
        'name': 'name',
        'id': 'id'
    }

    def __init__(self, document_id=None, number=None, ooxml_id=None, svg_blob_url=None, slide_document_url=None, base_element_blob_url=None, changed_base_element_blob_url=None, package_uri=None, name=None, id=None):  # noqa: E501
        """SlideSlides - a model defined in OpenAPI"""  # noqa: E501

        self._document_id = None
        self._number = None
        self._ooxml_id = None
        self._svg_blob_url = None
        self._slide_document_url = None
        self._base_element_blob_url = None
        self._changed_base_element_blob_url = None
        self._package_uri = None
        self._name = None
        self._id = None
        self.discriminator = None

        self.document_id = document_id
        if number is not None:
            self.number = number
        if ooxml_id is not None:
            self.ooxml_id = ooxml_id
        self.svg_blob_url = svg_blob_url
        self.slide_document_url = slide_document_url
        self.base_element_blob_url = base_element_blob_url
        self.changed_base_element_blob_url = changed_base_element_blob_url
        self.package_uri = package_uri
        self.name = name
        if id is not None:
            self.id = id

    @property
    def document_id(self):
        """Gets the document_id of this SlideSlides.  # noqa: E501


        :return: The document_id of this SlideSlides.  # noqa: E501
        :rtype: str
        """
        return self._document_id

    @document_id.setter
    def document_id(self, document_id):
        """Sets the document_id of this SlideSlides.


        :param document_id: The document_id of this SlideSlides.  # noqa: E501
        :type: str
        """

        self._document_id = document_id

    @property
    def number(self):
        """Gets the number of this SlideSlides.  # noqa: E501


        :return: The number of this SlideSlides.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this SlideSlides.


        :param number: The number of this SlideSlides.  # noqa: E501
        :type: int
        """

        self._number = number

    @property
    def ooxml_id(self):
        """Gets the ooxml_id of this SlideSlides.  # noqa: E501


        :return: The ooxml_id of this SlideSlides.  # noqa: E501
        :rtype: int
        """
        return self._ooxml_id

    @ooxml_id.setter
    def ooxml_id(self, ooxml_id):
        """Sets the ooxml_id of this SlideSlides.


        :param ooxml_id: The ooxml_id of this SlideSlides.  # noqa: E501
        :type: int
        """

        self._ooxml_id = ooxml_id

    @property
    def svg_blob_url(self):
        """Gets the svg_blob_url of this SlideSlides.  # noqa: E501


        :return: The svg_blob_url of this SlideSlides.  # noqa: E501
        :rtype: str
        """
        return self._svg_blob_url

    @svg_blob_url.setter
    def svg_blob_url(self, svg_blob_url):
        """Sets the svg_blob_url of this SlideSlides.


        :param svg_blob_url: The svg_blob_url of this SlideSlides.  # noqa: E501
        :type: str
        """

        self._svg_blob_url = svg_blob_url

    @property
    def slide_document_url(self):
        """Gets the slide_document_url of this SlideSlides.  # noqa: E501


        :return: The slide_document_url of this SlideSlides.  # noqa: E501
        :rtype: str
        """
        return self._slide_document_url

    @slide_document_url.setter
    def slide_document_url(self, slide_document_url):
        """Sets the slide_document_url of this SlideSlides.


        :param slide_document_url: The slide_document_url of this SlideSlides.  # noqa: E501
        :type: str
        """

        self._slide_document_url = slide_document_url

    @property
    def base_element_blob_url(self):
        """Gets the base_element_blob_url of this SlideSlides.  # noqa: E501


        :return: The base_element_blob_url of this SlideSlides.  # noqa: E501
        :rtype: str
        """
        return self._base_element_blob_url

    @base_element_blob_url.setter
    def base_element_blob_url(self, base_element_blob_url):
        """Sets the base_element_blob_url of this SlideSlides.


        :param base_element_blob_url: The base_element_blob_url of this SlideSlides.  # noqa: E501
        :type: str
        """

        self._base_element_blob_url = base_element_blob_url

    @property
    def changed_base_element_blob_url(self):
        """Gets the changed_base_element_blob_url of this SlideSlides.  # noqa: E501


        :return: The changed_base_element_blob_url of this SlideSlides.  # noqa: E501
        :rtype: str
        """
        return self._changed_base_element_blob_url

    @changed_base_element_blob_url.setter
    def changed_base_element_blob_url(self, changed_base_element_blob_url):
        """Sets the changed_base_element_blob_url of this SlideSlides.


        :param changed_base_element_blob_url: The changed_base_element_blob_url of this SlideSlides.  # noqa: E501
        :type: str
        """

        self._changed_base_element_blob_url = changed_base_element_blob_url

    @property
    def package_uri(self):
        """Gets the package_uri of this SlideSlides.  # noqa: E501


        :return: The package_uri of this SlideSlides.  # noqa: E501
        :rtype: str
        """
        return self._package_uri

    @package_uri.setter
    def package_uri(self, package_uri):
        """Sets the package_uri of this SlideSlides.


        :param package_uri: The package_uri of this SlideSlides.  # noqa: E501
        :type: str
        """

        self._package_uri = package_uri

    @property
    def name(self):
        """Gets the name of this SlideSlides.  # noqa: E501


        :return: The name of this SlideSlides.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SlideSlides.


        :param name: The name of this SlideSlides.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def id(self):
        """Gets the id of this SlideSlides.  # noqa: E501


        :return: The id of this SlideSlides.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SlideSlides.


        :param id: The id of this SlideSlides.  # noqa: E501
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
        if not isinstance(other, SlideSlides):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
