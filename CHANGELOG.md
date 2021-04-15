# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.2] - 2021-04-15

## Added

- Option to do PubChem search on both parent mass estimate and precursor_mz [#8](https://github.com/matchms/matchmsextras/pull/8)

## [0.2.1] - 2021-02-24

### Added

- Split network creation into `create_network` and `create_network_asymmetric` [#5](https://github.com/matchms/matchmsextras/pull/5)
- Refactored `dilate_cluster` [#5](https://github.com/matchms/matchmsextras/pull/5)
- Add `extract_networking_metadata` [#6](https://github.com/matchms/matchmsextras/pull/6)

## [0.2.0] - 2021-02-24

### Added

- Tests for `create_network` [#3](https://github.com/matchms/matchmsextras/pull/3)

### Changed

- Refactored `create_network` function to work with queries != references [#3](https://github.com/matchms/matchmsextras/pull/3)

## [0.1.0] - 2021-02-16

### Added

- This is the initial version mostly taken from https://github.com/iomega/spec2vec_gnps_data_analysis

[Unreleased]: https://github.com/matchms/matchmsextras/compare/0.2.2...HEAD
[0.2.1]: https://github.com/matchms/matchmsextras/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/matchms/matchmsextras/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/matchms/matchmsextras/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/matchms/matchmsextras/releases/tag/0.1.0
