# Public / Private Boundary

This document defines the intended boundary between this public repository, Zenodo archives, and private/internal working repositories.

For the current public reading order, see [Reader Guide](READER_GUIDE.md). For the global current status, see [Current Status](CURRENT_STATUS.md).

## Public Repository Role

This public repository is intended for stable public-facing materials, including:

- public routing and citation metadata;
- links to archived Zenodo records;
- public claim boundaries;
- public-facing definition summaries;
- empirical-readiness summaries;
- public routing and archival labels.

Public materials should be concise, reviewed, and separated from internal reasoning before publication.

## Zenodo Archive Role

Zenodo is the authoritative archive for fixed release packages.

For each published package, Zenodo should hold the release files, such as PDFs, zip packages, manifests, QA audits, checksums, and metadata. The public GitHub repository may link to those records, but it does not need to duplicate the full archive.

Primary L4 structural-proxy Zenodo record:

```text
https://zenodo.org/records/20728608
https://doi.org/10.5281/zenodo.20728608
```

For the full public record index, see [Zenodo Records](ZENODO_RECORDS.md).

## Private/Internal Repository Role

Private/internal repositories are for work that is not ready to function as public source material, including:

- drafts;
- generated outputs;
- audit notes;
- internal consistency work;
- unresolved reasoning;
- source inventories;
- implementation planning;
- private review trails;
- raw caches or large intermediate files.

The private/internal `kai-order-theory` repository remains an internal working space. It should not be made public as-is and should not be used as the public source for the current Zenodo record.

## Transfer Boundary

Private/internal files should not be copied into this public repository as-is.

Material from private/internal work may be used only after it is rewritten and reviewed as public-facing material. That rewrite should remove internal reasoning, unresolved drafts, audit trail details, private source inventories, and implementation planning that do not belong in a public home repository.

Public materials should preserve the claim boundary. The current archived record supports L4 rule-conditional D2+ structural-proxy support only. It should not be presented as direct theory proof, direct pleasure/suffering measurement, direct Omega/O-M-A validation, or causal identification.
