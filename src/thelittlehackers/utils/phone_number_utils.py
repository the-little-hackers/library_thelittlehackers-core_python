# Copyright (C) 2025 TendKid.  All rights reserved.
#
# This software is the confidential and proprietary information of
# TendKid or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with TendKid.
#
# TENDKID MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  TENDKID SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from enum import StrEnum
from enum import auto

import phonenumbers
from loguru import logger
from phonenumbers.phonenumberutil import NumberParseException
from thelittlehackers.model.country import Country


class PhoneNumberUtilsErrorCode(StrEnum):
    INVALID_PHONE_NUMBER = auto()


class InvalidPhoneNumberException(BaseException):
    """
    Exception raised when an invalid phone number is supplied.
    """
    def __init__(self, phone_number: str):
        """
        Initialize the exception with the offending phone number.


        :param phone_number: The invalid phone number that triggered the
            exception.
        """
        super().__init__(
            f"The string supplied \"{phone_number}\" doesn't not seem to be a phone number",
            PhoneNumberUtilsErrorCode.INVALID_PHONE_NUMBER
        )


def format_phone_number_to_e164(
        phone_number: str,
        country: Country
) -> str:
    """
    Parse and format a phone number into the E.164 international format.


    :param phone_number: The raw phone number string to be validated and
        formatted.

    :param country: The country used to provide the default region for
        parsing.


    :return: The phone number formatted in E.164 format (e.g.,
        '+14155552671').


    :raise InvalidPhoneNumberException: If the input string is not a valid
        phone number.
    """
    # Parse the phone number (no region hint, must be international).
    try:
        phone_number_object = phonenumbers.parse(phone_number, region=None)
        return phonenumbers.format_number(phone_number_object, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:  # The phone number is not international.
        pass

    # Format the national phone number into an international phone number.
    try:
        phone_number_object = phonenumbers.parse(phone_number, region=country.to_string())
        return phonenumbers.format_number(phone_number_object, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException as exception:
        logger.error(exception)
        raise InvalidPhoneNumberException(phone_number)


def is_strict_international_format(phone_number: str) -> bool:
    """
    Check if a phone number string is in a valid international format.


    :param phone_number: The phone number string to validate.


    :return: ``True`` if the phone number is in international format,
        ``False`` otherwise.
    """
    try:
        phonenumbers.parse(phone_number, region=None)
        return True
    except phonenumbers.NumberParseException:
        return False