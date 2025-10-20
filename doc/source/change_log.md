# Change Log

## 1.0.5 (2025-10-20)

This is a patch release that propagates a fix for references index constraint
where indices in references were erroneously assumed to be positive integers.

## 1.0.4 (2025-04-29)

We propagate the changes and fixes for V3.0.2; please refer to:
* https://github.com/aas-core-works/aas-core-meta/pull/335
* https://github.com/aas-core-works/aas-core-meta/pull/341
* https://github.com/aas-core-works/aas-core-meta/pull/343
* https://github.com/aas-core-works/aas-core-meta/pull/353
* https://github.com/aas-core-works/aas-core-meta/pull/365
* https://github.com/aas-core-works/aas-core-meta/pull/368 

## 1.0.3 (2024-04-16)

The `dataSpecification` field in `EmbeddedDataSpecification` is made
optional, according to the book.

## 1.0.2 (2024-03-23)

In this patch version, we propagate the fix from abnf-to-regex related
to maximum qualifiers which had been mistakenly represented as exact
repetition before.

## 1.0.1 (2024-03-13)

This patch release brings about the fix for patterns concerning dates and
date-times with zone offset `14:00` which previously allowed for
a concatenation without a plus sign.

## 1.0.0 (2024-02-02)

This is the first stable release. The release candidates stood
the test of time, so we are now confident to publish a stable
version.

## 1.0.0-rc5 (2023-11-09)

* Fix error message in xmlization on XML declaration (#25)

  When we encountered XML declarations, we threw exceptions with
  uninformative messages. Namely, we expect the reader to be moved to the
  content, but most users omitted to read that in the documentation.

  We refine the error message for this particular situation, and hint at
  `MoveToContent` method on the reader.

## 1.0.0-rc4 (2023-09-08)

* Update to aas-core-meta, codegen, testgen 4d7e59e, f3d9538, 
  9b43de2e (#22)

  This propagates the following fixes from aas-core-meta and
  aas-core-codegen:
  * 281 and 280 in aas-core-meta which fix invariants AASc-3a-010 and 
    AASd-131, respectively.
  * 399 in aas-core-codegen which makes the visitation methods
    `Visit` and `Transform` in the abstract visitors and transformers
    virtual. This is necessary so that the implementors can override
    them, *e.g.*, for updating the current path to the visited object.

## 1.0.0-rc3 (2023-06-28)

* Report unexpected text in XML sequences (#19)
* Update to aas-core-meta, codegen, testgen 44756fb, e2b793f, 
  bf3720d7 (#18)
  * This is an important patch propagating in particular the following
    fixes which affected the constraints and their documentation:
  * Pull requests in aas-core-meta 271, 272 and 273 which
    affect the nullability checks in constraints,
  * Pull request in aas-core-meta 275 which affects
    the documentation of many constraints.

## 1.0.0-rc2 (2023-03-24)

* Refactor unwrapper from enhancer (#12)
* Updates to latest aas-core-meta, codegen and testgen

## 1.0.0-rc1

This is the first public version.
