# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- `string_to_email_address` is typed to return `str | None` when
  `strict` is `False`, and `str` otherwise.

### Fixed
- `is_valid_email_address`, and therefore `string_to_email_address`,
  check the whole string: a string that only starts with a valid email
  address (e.g., "jane@example.com, john@example.com") is no longer
  considered valid.
- Remove the statements of `string_to_date`, `string_to_decimal`,
  `string_to_integer`, `string_to_locale`, `string_to_time`,
  `string_to_timestamp`, `string_to_uuid`, and `string_to_version` that
  built an error message without raising it.  These functions keep
  returning `None` for `None` or an empty string, even when `strict` is
  `True`, as their callers rely on it; this is now documented and
  tested.
- `string_to_mac_address` returns a tuple of six strings of two
  hexadecimal digits (e.g., `('01', '23', '45', '67', '89', 'AB')`), as
  its documentation states, instead of a tuple of lists of characters
  (e.g., `(['0', '1'], ['2', '3'], ...)`).
- `string_to_date` returns the date part of a `datetime.datetime`
  instead of the `datetime.datetime` itself.

## [1.4.1] - 2026-10-12
### Changed
- Replace the libraries `unidecode` (GPLv2+) and `normality` (which
  depends on `text-unidecode`, Artistic License or GPLv2+) with the
  library `anyascii` (ISC).
- `string_to_keywords` transliterates any Unicode character, whatever
  its script, to lowercase ASCII, as its documentation states.  Latin
  letters that don't decompose into a base letter and diacritics are now
  transliterated too (e.g., "Đặng" returns `dang` instead of `đang`,
  "Straße" returns `strasse` instead of `straße`).  Keywords previously
  stored by an application need to be rebuilt.
- `normalize_key` always returns a lowercase string (it returned
  uppercase letters for CJK and Korean scripts).

## [1.4.0] - 2026-10-08
### Added
- `Version.from_pyproject` reads the version declared in the `[project]`
  table (PEP 621), and falls back to the `[tool.poetry]` table when the
  project doesn't declare its version in `[project]`.
### Fixed
- The attribute `country_code` of `Country` is required: it defaulted to
  `None`.

## [1.3.0] - 2026-07-30
### Changed
- Rename `LoggingLevelLiteral` with `LogLevelLiteral`, `LOGGING_LEVEL`
  with `LOG_LEVEL`, and `LOGGING_LEVEL_LITERAL_STRINGS` with
  `LOG_LEVEL_LITERAL_STRINGS`.

## [1.2.4] - 2026-05-14
### Added
- Function to format a duration using a human-readable approximate time 
  unit.

## [1.2.3] - 2026-04-10
### Added
- Support for parsing version strings with missing minor and/or patch 
  components (e.g., 1, 1.2).
### Changed
- Update semantic versioning regular expression to accept: `major`, 
  `major.minor`, `major.minor.patch`.
- Missing minor and patch components now default to 0 when constructing 
  a Version instance.
### Fixed
- Prevent parsing errors when handling version strings without explicit 
  minor or patch values.

## [1.2.2] - 2026-03-25
### Added
- Add JSON serializers for classes `Locale` and `Country`.

## [1.2.1] - 2026-03-20
### Changed
- Rename function `normalize_names_codes_mapping` with 
  `normalize_mapping_keys`.

## [1.2.0] - 2026-03-04
### Changed
- Rename enumeration `EntityStatus` with `EntityState`.

## [1.1.0] - 2025-09-25
### Added
- Rename modules `constants` and `models`.

## [1.0.17] - 2025-09-22
### Added
- Function to format phone numbers to E.164.

## [1.0.16] - 2025-09-07
### Fixed
- Misspelled `Country` object's  attribute `__country_code` instead of 
  `country_code`.

## [1.0.15] - 2025-05-23
### Changed
- Remove the constant `DEFAULT_DIRECTORY_DEPTH`.

## [1.0.14] - 2025-04-10
### Added
- Add the base error class `TheLittleHackersBaseError`.

## [1.0.13] - 2025-04-08
### Added
- Add the module `file_utils`.

## [1.0.12] - 2025-02-19
### Added
- Add the member `DRAFT` to the enumeration `EntityStatus`.

## [1.0.8] - 2025-01-13
### Changed
- Define the values of the enumeration `ContactName` members as 
  uppercase strings.

## [1.0.8] - 2025-01-13
### Added
- Add the field `property_parameters` to the model `ContactName`.

## [1.0.7] - 2025-01-13
### Added
- Document the members of the enumeration `ContactName`.

## [1.0.6] - 2025-01-11
### Changed
- Load the specified class when found in the module (to prevent 
  partially initialized module).

## [1.0.5] - 2025-01-06
### Added
- Add the members `FAILED` and `SUCCEEDED` to the enumeration 
  `EntityStatus`.

## [1.0.4] - 2025-01-04
### Changed
- Refactor the `Country` class to a Pydantic model.

## [1.0.3] - 2024-12-14
### Added
- Add the members `ACCEPTED` and `REJECTED` to the enumeration 
  `EntityStatus`.

## [1.0.2] - 2024-12-13
### Changed
- Refactor the `Version` class to a Pydantic model.

## [1.0.1] - 2024-09-23
### Added
- Parse the version from `pyproject.toml` file.

## [1.0.0] - 2024-04-19
### Added
- Initial import.
