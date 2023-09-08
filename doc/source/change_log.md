# Change Log

## 1.0.0-rc4

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

## 1.0.0-rc3

* Report unexpected text in XML sequences (#19)
* Update to aas-core-meta, codegen, testgen 44756fb, e2b793f, 
  bf3720d7 (#18)
  * This is an important patch propagating in particular the following
    fixes which affected the constraints and their documentation:
  * Pull requests in aas-core-meta 271, 272 and 273 which
    affect the nullability checks in constraints,
  * Pull request in aas-core-meta 275 which affects
    the documentation of many constraints.

## 1.0.0-rc2

* Refactor unwrapper from enhancer (#12)
* Updates to latest aas-core-meta, codegen and testgen

## 1.0.0-rc1

This is the first public version.
