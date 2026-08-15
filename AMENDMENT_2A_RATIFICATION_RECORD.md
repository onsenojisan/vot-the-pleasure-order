# Amendment 2A — Ratification Record

Status: **activates 2A when this record is public and the adopted commit is preserved in repository history**
Author approval date: 2026-08-15
Record date: 2026-08-15

## Adopted Text

```text
file: AMENDMENT_2A_GOVERNANCE_RULES.md
immutable Git commit: b0dff095919295acbaaf1811a29d63736632d429
Git blob ID: b5a574fbce4458422a823c6a715c2b9cbd2e4b16
canonical repository-blob SHA-256: d5b0f88a95bd373636a9f489bd814fb267a7564d061d76a8acdb966d3b0117f1
```

The SHA-256 is over the UTF-8, LF-terminated bytes stored in the Git blob.
Windows checkouts may convert LF to CRLF and therefore produce a different
working-tree byte hash without changing the adopted repository content. The Git
blob ID is the direct cross-check for the committed object.

The author approved the staged 2A/2B architecture and directed its
implementation on 2026-08-15. The commit above contains the approved 2A text,
the unfilled 2B template and the associated routing updates.

This record activates only the prospective governance rules in 2A. It does not:

- designate a target dataset;
- assert target-outcome blindness for any study;
- activate the 2B template;
- ratify candidate model parameters, priors, power targets, margins or seeds;
- change the frozen v0.2 preregistration or Amendment 1;
- upgrade any VOT evidence or claim.

Each future study must provide its own affirmative blindness statement and
complete 2B annex before target-outcome inspection. Without it, the permitted
result remains `NO AMENDMENT 2 VERDICT`.

## Verification And Preservation

The publishing merge must preserve the adopted commit as an ancestor of the
default branch. A squash that replaces that commit does not satisfy this record.
Verify with:

```powershell
git merge-base --is-ancestor b0dff095919295acbaaf1811a29d63736632d429 origin/main
git show b0dff095919295acbaaf1811a29d63736632d429:AMENDMENT_2A_GOVERNANCE_RULES.md
git rev-parse b0dff095919295acbaaf1811a29d63736632d429:AMENDMENT_2A_GOVERNANCE_RULES.md
```

The final command must return `b5a574fbce4458422a823c6a715c2b9cbd2e4b16`.

Any later 2A edit requires a new version, new content hash and new ratification
record. This record never floats with `main`.
