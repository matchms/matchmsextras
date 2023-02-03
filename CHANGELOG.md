# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2023-02-03

### Changed

- removed network creation functions which have meanwhile been incorporated in matchms
- switch default id fieldname form "spectrumid" to "spectrum_id" (matchms > 0.14.0)
- adapt test to new Scores object design (matchms > 0.18.0)

## [0.3.0] - 2021-12-19

### Added

- `allowed_difference` argument for pubchem search to include known, common mass differences into the pubchem search (e.g. water or NH4) to compensate missing adduct information [#12](https://github.com/matchms/matchmsextras/pull/12)

### Changed

- exchange print against logging statements in pubchem search [#12](https://github.com/matchms/matchmsextras/pull/12)
- raise needed matchms version to newest version 0.11.0 which includes logging [#12](https://github.com/matchms/matchmsextras/pull/12)


## [0.2.3] - 2021-07-15

## Fixed

- Minor bug with string to float conversion for pubchem provided mass [#9](https://github.com/matchms/matchmsextras/pull/9)

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

[Unreleased]: https://github.com/matchms/matchmsextras/compare/0.4.0...HEAD
[0.4.0]: https://github.com/matchms/matchmsextras/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/matchms/matchmsextras/compare/0.2.3...0.3.0
[0.2.3]: https://github.com/matchms/matchmsextras/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/matchms/matchmsextras/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/matchms/matchmsextras/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/matchms/matchmsextras/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/matchms/matchmsextras/releases/tag/0.1.0
