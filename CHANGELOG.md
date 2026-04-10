# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.3] - 2026-04-10
### Add
- Support for parsing version strings with missing minor and/or patch components (e.g., 1, 1.2)
### Changed
- Update semantic versioning regular expression to accept: major, major.minor, major.minor.patch
- Missing minor and patch components now default to 0 when constructing a Version instance.
### Fixed
- Prevent parsing errors when handling version strings without explicit minor or patch values.

## [1.2.2] - 2026-03-25
### Added
- Add JSON serializers for classes `Locale` and `Country`

## [1.2.1] - 2026-03-20
### Changed
- Rename function `normalize_names_codes_mapping` with `normalize_mapping_keys`

## [1.2.0] - 2026-03-04
### Changed
- Rename enumeration `EntityStatus` with `EntityState`

## [1.1.0] - 2025-09-25
### Added
- Rename modules `constants` and `models`

## [1.0.17] - 2025-09-22
### Added
- Function to format phone numbers to E.164

## [1.0.16] - 2025-09-07
### Fixed
- Misspelled `Country` object's  attribute `__country_code` instead of `country_code`

## [1.0.15] - 2025-05-23
### Changed
- Remove the constant `DEFAULT_DIRECTORY_DEPTH`

## [1.0.14] - 2025-04-10
### Added
- Add the base error class `TheLittleHackersBaseError`

## [1.0.13] - 2025-04-08
### Added
- Add the module `file_utils`

## [1.0.12] - 2025-02-19
### Added
- Add the member `DRAFT` to the enumeration `EntityStatus`

## [1.0.8] - 2025-01-13
### Changed
- Define the values of the enumeration `ContactName` members as uppercase strings

## [1.0.8] - 2025-01-13
### Added
- Add the field `property_parameters` to the model `ContactName`

## [1.0.7] - 2025-01-13
### Added
- Document the members of the enumeration `ContactName`

## [1.0.6] - 2025-01-11
### Changed
- Load the specified class when found in the module (to prevent partially initialized module)

## [1.0.5] - 2025-01-06
### Added
- Add the members `FAILED` and `SUCCEEDED` to the enumeration `EntityStatus`

## [1.0.4] - 2025-01-04
### Changed
- Refactor the `Country` class to a Pydantic model

## [1.0.3] - 2024-12-14
### Added
- Add the members `ACCEPTED` and `REJECTED` to the enumeration `EntityStatus`

## [1.0.2] - 2024-12-13
### Changed
- Refactor the `Version` class to a Pydantic model

## [1.0.1] - 2024-09-23
### Added
- Parse the version from `pyproject.toml` file

## [1.0.0] - 2024-04-19
### Added
- Initial import
