# MIT License
#
# Copyright (C) 2024 The Little Hackers.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import annotations

import logging
import re
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from thelittlehackers.constant.contact import ContactName
from thelittlehackers.constant.privacy import Visibility
from thelittlehackers.constant.regex import REGEX_PATTERN_EMAIL_ADDRESS
from thelittlehackers.constant.regex import REGEX_PATTERN_PHONE_NUMBER


class InvalidContactException(ValueError):
    """
    Indicate the value of a contact doesn't comply with the type of this
    contact.
    """


class Contact(BaseModel):
    """
    Represent a contact information, such as an e-mail address, a phone
    numbers, the Uniform Resource Locator (URL) of a website.
    """
    REGEX_EMAIL_ADDRESS = re.compile(REGEX_PATTERN_EMAIL_ADDRESS)
    REGEX_PHONE_NUMBER = re.compile(REGEX_PATTERN_PHONE_NUMBER)

    __CONTACT_NAME_REGEX_MAPPING = {
        ContactName.EMAIL: REGEX_EMAIL_ADDRESS,
        ContactName.PHONE: REGEX_PHONE_NUMBER,
    }

    is_primary: Optional[bool] = Field(
        False,
        description="Specify whether this contact information is the primary contact for "
                    "this type of contact information.",
        frozen=False
    )

    is_verified: Optional[bool] = Field(
        False,
        description="Specify whether this contact information has been verified, i.e., it "
                    "has been grabbed from a trusted Social Networking Service (SNS), or "
                    "through a challenge/response process.",
        frozen=False,
    )

    property_name: ContactName = Field(
        ...,
        description="The name (type) of this contact information.",
        frozen=True
    )

    property_value: str = Field(
        ...,
        description="A string representation of the value associated to the contact "
                    "information.",
        frozen=True
    )

    visibility: Optional[Visibility] = Field(
        Visibility.PRIVATE,
        description="The visibility of this contact information to other users.",
        frozen=False
    )

    def __eq__(self, other):
        """
        Check whether this contact information to the one passed to this
        function.

        Two instances are equivalent when they are of the same type and they
        have the same value.


        :param other: an instance `Contact`.


        :return: `True` if this contact information corresponds to the
            contact information passed to this function; `False` otherwise.
        """
        return self.__property_name == other.__property_name \
            and self.__property_value == other.__property_value

    def __str__(self):
        """
        Return a nicely printable string representation of this contact
        information:

            [ name:string, value:string, is_primary:boolean, is_verified:boolean ]


        :return: a string of the array representation of this contact
            information.
        """
        return str([
            str(self.property_name),
            self.property_value,
            self.is_primary,
            self.is_verified
        ])

    @classmethod
    def assert_contact_value(
            cls,
            property_name: ContactName,
            property_value: str
    ) -> None:
        """
        Check that the contact value is valid.


        :param property_name: The contact information's type.

        :param property_value: The contact's value, such as for instance
            `+84.8272170781`, the formatted value for a telephone number
            property.


        :raise InvalidContactException: If the value of the contact doesn't
            comply with the type of this contact.

        :raise ValueError: If no regular expression mapping is defined for the
            given property name.  Please, contact the developers.
        """
        regex = cls.__CONTACT_NAME_REGEX_MAPPING.get(property_name)
        if regex is None:
            raise ValueError(
                f"No regex mapping found for contact type \"{property_name}\""
            )

        if not cls.__CONTACT_NAME_REGEX_MAPPING[property_name].match(property_value):
            raise cls.InvalidContactException(
                f"Invalid value \"{property_value}\" for contact type \"{property_name}\". "
                f"Expected format does not match."
            )

    # @staticmethod
    # def from_json(payload: Collection | None) -> Contact | None:
    #     """
    #     Convert a JSON-like dictionary representing contact information into
    #     an instance of ``Contact``.
    #
    #     This method interprets the provided dictionary and converts it into a
    #     ``Contact`` object, extracting the contact type, value, and optional
    #     attributes such as whether the contact is primary or verified.
    #
    #
    #     :param payload: A dictionary representing the contact information in
    #         the format:
    #
    #         ```json
    #         [ type:ContactName, value:string, [is_primary:boolean, [is_verified:boolean]] ]
    #         ```
    #
    #         Note: ``payload`` can also be ``None``, in which case the method
    #             returns ``None``.
    #
    #
    #     :return: An instance ``Contact``, or ``None`` if ``payload`` is ``None``.
    #
    #
    #     :raise TypeError: If the provided payload is not a list, a dictionary,
    #         or a tuple.
    #
    #     :raise ValueError: If the provided type of this contact information
    #         is not a string representation of an item of the enumeration
    #         ``ContactName``.
    #     """
    #     if payload is None:
    #         return None
    #
    #     if not isinstance(payload, Collection):
    #         raise TypeError(
    #             f"Expected an object of type Sized for payload, got \"{type(payload).__name__}\""
    #         )
    #
    #     contact_element_number = len(payload)
    #     if contact_element_number < 2 or contact_element_number > 4:
    #         raise ValueError("Invalid contact information format")
    #
    #     # Unpack the contact information with default values for optional fields.
    #     property_name, property_value = payload[:2]
    #     is_primary, is_verified = (
    #         list(payload[2:]) + [None] * (4 - contact_element_number)
    #     )
    #
    #     # Convert string to ContactName enum and ensure it's valid.
    #     try:
    #         contact_name_enum = ContactName(property_name)
    #     except ValueError as exception:
    #         raise ValueError(f"Invalid contact type \"{property_name}\"") from exception
    #
    #     # Convert string values to booleans where necessary
    #     is_primary_bool = is_primary and string_utils.string_to_boolean(is_primary, strict=True)
    #     is_verified_bool = is_verified and string_utils.string_to_boolean(is_verified, strict=True)
    #
    #     return Contact(
    #         contact_name_enum,
    #         property_value,
    #         is_primary=is_primary_bool,
    #         is_verified=is_verified_bool
    #     )

    # @staticmethod
    # def from_object(obj):
    #     """
    #     Convert an object representing a contact information to an instance
    #     ``Contact``.
    #
    #
    #     :param obj: an object containing the following attributes:
    #
    #         - ``name`` (required): An item of the enumeration ``ContactName``
    #           representing the type of this contact information.
    #
    #         - ``value`` (required): The string representation of this contact
    #           information.
    #
    #         - ``is_primary`` (optional): Indicate whether this contact property is
    #           the first to be used to contact the entity that this contact
    #           information corresponds to.  There is only one primary contact
    #           property for a given property name (e.g., ``EMAIL``, ``PHONE``,
    #           ``WEBSITE``).
    #
    #         - ``is_verified`` (optional): indicate whether this contact information
    #           has been verified, whether it has been grabbed from a trusted Social
    #           Networking Service (SNS), or whether through a challenge/response
    #           process.
    #
    #
    #     :raise ValueError: If the value of this contact information is null.
    #     """
    #     return obj if isinstance(obj, Contact) \
    #         else Contact(
    #             ContactName(obj.property_name),
    #             obj.property_value,
    #             is_primary=obj.is_primary and string_utils.string_to_boolean(obj.is_primary, strict=True),
    #             is_verified=obj.is_verified and string_utils.string_to_boolean(obj.is_verified, strict=True))

    @classmethod
    def from_string(
            cls,
            property_value: str,
            is_primary: bool | None = None,
            is_verified: bool | None = False,
            visibility: Visibility | None = None
    ) -> Contact:
        """
        Create a ``Contact`` object based on a given contact value string.

        This method attempts to determine the type of contact information (e.g.,
        email, phone, website) from the provided `property_value` string by
        matching it against predefined patterns.  If a match is found, it
        returns a `Contact` object initialized with the corresponding contact
        type and the specified attributes.


        :param property_value: A string representing the contact value (e.g.,
            an email address, phone number, or website URL).

        :param is_primary; Indicate whether this contact property is the
            primary method for contacting the entity. Only one primary contact
            is allowed per contact type (e.g., ``EMAIL``, ``PHONE``).
            Defaults to ``False``.

        :param is_verified; Indicate whether this contact information has been
            verified, either through a trusted Social Networking Service (SNS)
            or via a challenge/response process.  Defaults to ``False``.

        :param visibility: Optional; specifies the visibility of this contact
            information to other users. If not provided, defaults to
            `Visibility.PUBLIC`.


        :return: A `Contact` object representing the contact type and value,
            with the specified attributes.


        :raise InvalidContactException: If the ``property_value`` does not
            match any recognized contact type, this exception is raised.
        """
        for property_name, regex in cls.__CONTACT_NAME_REGEX_MAPPING.items():
            if regex.match(property_value):
                return Contact(
                    is_primary=is_primary,
                    is_verified=is_verified,
                    property_name=property_name,
                    property_value=property_value,
                    visibility=visibility
                )
        else:
            raise cls.InvalidContactException(
                f"Unsupported contact information \"{property_value}\""
            )

    @field_validator('property_value', mode='before')
    @classmethod
    def validate_property_value(cls, value: str, values: dict) -> str:
        """
        Validate the property value based on the property name, and convert it
        to lowercase.


        :param value: A string representation of the value associated to a
            contact information.

        :param values: A dictionary of the field values, used to access
            the ``property_name`` field.


        :return: The validated lowercase value.


        :raise ValueError: If the property_value does not match the
            expected format for the specified ``property_name`` field.
        """
        property_name = values.get('property_name')
        if property_name is None:
            raise ValueError("`property_name` must be set before validating `property_value`.")

        # Force to lowercase.
        lowercase_value = value.lower()
        if lowercase_value != value:
            logging.warning(
                f"The property value \"{value}\" contains uppercase letters.  Converting it "
                f"to lowercase: \"{lowercase_value}\"."
            )

        # Validate the `property_value` against the appropriate regex.
        cls.assert_contact_value(property_name, lowercase_value)

        return lowercase_value
