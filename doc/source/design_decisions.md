# Design Decisions

We explain a couple of design decisions and trade-offs we deliberately made during the development of the SDK.
These are our opinions — you may or may not agree, which is totally OK as there are always more than one way to do things and do them well.

However, the decisions elaborated here are not meant to convince you. 
We want to give you insight about why we did certain things, and why we didn't implement them in some other way.  

## Aggregations as Lists instead of Dictionaries

We decided to implement all the aggregations in the meta-model as [System.Collections.Generic.List] instead of [System.Collections.Generic.Dictionary].

[System.Collections.Generic.List]: https://docs.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1
[System.Collections.Generic.Dictionary]: https://docs.microsoft.com/en-us/dotnet/api/system.collections.generic.dictionary-2?view=net-6.0

Some structures just "scream" for a dictionary, such as `SubmodelElements` property in a [Submodel].
The submodel elements need to be unique w.r.t. their ID-shorts.
So why didn't we model them as dictionaries, where keys are ID-shorts?

[Submodel]: api/AasCore.Aas3_0.Submodel.yml

There are multiple reasons:

* "There are only two hard things in Computer Science: cache invalidation and naming things" (see [this StackExchange]).
  For example, the key in the dictionary and the `IdShort` property of the submodel element need to be always in sync.
  Keeping such things in sync can be hard.
* When de-serializing, you need to hash on all the key/value pairs.
  In many situations, you do not perform any look-ups, but want to read the whole environment only once, and act upon it.
  Hashing would have wasted computational resources.
* You may want to index on more things than `IdShort`.
  For example, retrieving submodel elements by their `SemanticId` is almost equally important.
* The order of the key/value pairs in a dictionary might not follow the order in the underlying serialized file.
  For example, if [System.Collections.HashTable] is used, the order is random.
  This would make the round-trip de-serialization 🠒 serialization non-deterministic.
* Generating code based on dictionaries would have incurred additional complexity in [aas-core-meta] and [aas-core-codegen] as we would need to capture indexing in our machine-readable meta-models.

[this StackExchange]: https://skeptics.stackexchange.com/questions/19836/has-phil-karlton-ever-said-there-are-only-two-hard-things-in-computer-science
[System.Collections.HashTable]: https://docs.microsoft.com/en-us/dotnet/api/system.collections.hashtable
[aas-core-meta]: https://github.com/aas-core-works/aas-core-meta/
[aas-core-codegen]: https://github.com/aas-core-works/aas-core-codegen/

We therefore leave indexing (and syncing of the indices) to the user instead of pre-maturely providing a basic index on one of the features.

## No Parent ⟷ Child Associations

We did not model the parent ⟷ child relations between the model elements for similar reasons why we did not implement dictionaries.
Namely, keeping the associations in sync is hard.
While you might have clear parent ⟷ child relationship when you deserialize an environment, this relationship becomes less clear when you start re-using objects between environments.

Moreover, you need to sync the parent when an instance associated as its child is deleted.
The complexity of this sync becomes hard (and computationally costly) as your object tree grows.
And what if you re-assign the instance to multiple parents?

For example, an instance of [Submodel] may appear in multiple instances of [Environment].
Which environment is the parent?

[Environment]: api/AasCore.Aas3_0.Environment.yml

Multiple solutions are possible, and they depend on the application domain.
In some cases, where you deal with static data, a simple dictionary parent 🠒 child is sufficient.
In other cases, more involved data structures and updating strategies are needed.

As we did not want to prejudice the SDK for a particular application domain, we left out parent ⟷ child associations.

We indeed discussed a couple of concrete solutions, but failed to find a unifying approach which would satisfy multiple scenarios.
Please [create an issue] if you would like to discuss this point further.

[create an issue]: https://github.com/aas-core-works/aas-core3.0-csharp/issues/new/choose

## Values as Strings

As you can see, say, in [Property] class, the `Value` property holds strings.
This is indeed intentional though it might seem a bit outlandish.

[Propery]: api/AasCore.Aas3_0.Property.yml

You have to bear in mind that the lexical space of [XML basic data types], which we use to encode values in such properties, is large, and larger than C# primitive types.

[XML basic data types]: https://www.w3.org/TR/xmlschema-2/

For example, `xs:double`'s can have an arbitrary prefix of zeros (`001234` is a valid `xs:double`).

For another example, `xs:decimal` allows for an arbitrary size and precision.
In C#, [System.Decimal] is probably our best bet, but it has a fixed precision.
It might well be that our application domain requires more precision than [System.Decimal]!

[System.Decimal]: https://docs.microsoft.com/en-us/dotnet/api/system.decimal

Writing code for a setting where various systems interoperate with mixed application domains is difficult.
We wanted to stick to the specification, which mandates [XML basic data types], and thus leave the parsing of values up to the users.
Thus, we do not restrict the domain where our SDK can be used.
The users will know the best what precision and form they need.

## No AAS Registry

An AAS Registry is considered an external dependency, since it requires network requests.
We left it out-of-scope on purpose as this SDK focuses on the data exchange.
Further aas-core projects will work on an AAS registry.

One important consequence of leaving out the registry is that some constraints in the meta-model can not be enforced, as we do not know how to resolve the references.

The full list of omitted constraints is available in [the code of aas-core-meta].

[the code of aas-core-meta]: https://github.com/aas-core-works/aas-core-meta/blob/931b355682c4a7b84a2fb94932cf09bcf7ce9a1f/aas_core_meta/v3rc2.py#L4

## Build Your Own Abstraction on Top

We intentionally kept the API surface of the SDK minimal.
The idea was to give you basic building blocks which you can use to construct more complex structures.

For example, [LINQ] in conjunction with `Descend` method of [IClass] allows for powerful queries.

[LINQ]: https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/
[IClass]: api/AasCore.Aas3_0.IClass.yml

An implementation of [AbstractVisitor] or [AbstractTransformer] allows you to write converters to other formats.
They give you a pre-structured code which you merely need to fill in, thus reducing your mental overhead. 

[AbstractVisitor]: api/AasCore.Aas3_0.Visitation.AbstractVisitor.yml
[AbstractTransformer]: api/AasCore.Aas3_0.Visitation.AbstractTransformer-1.yml

## Maintainability *versus* Performance

We chose to sacrifice the performance for maintainability of the code.
In particular, we decided to generate the code automatically using [aas-core-codegen].

This imposed certain suboptimal spots in the code.
For example, the constraints are automatically transpiled.
A lot of constraints could have been optimized, but we are stuck with their representation in Python and the way they are translated into C#.

We believe that this is a valid trade-off at the moment.
At the moment, the meta-model changes too frequently to manually come up with the changes in an SDK without sacrificing the correctness.

As more critical applications and domains in the AAS space arise, and the meta-model becomes more stable, hand optimization of certain parts of our SDK will probably make more sense.
