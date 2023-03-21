# Iterate, Copy and Transform

The SDK provides various ways how you can loop through the elements of the model, and how these elements can be transformed.
Each following section will look into one of the approaches.

## `OverXOrEmpty`

For all the optional lists, there is a corresponding `Over{property name}OrEmpty` getter.
It gives you an [System.Collection.IEnumerable].
If the property is not set, this getter will give you an empty enumerable.
Otherwise, it will return the enumerable over the list.

[System.Collection.IEnumerable]: https://learn.microsoft.com/en-us/dotnet/api/system.collections.ienumerable?view=net-6.0

For example, see `OverSubmodelsOrEmpty` in [AasCore.Aas3_0.Environment.OverSubmodelsOrEmpty].

[AasCore.Aas3_0.Environment.OverSubmodelsOrEmpty]: ../api/AasCore.Aas3_0.Environment.yml#AasCore_Aas3_0_Environment_OverSubmodelsOrEmpty

## `DescendOnce` and `Descend`

If you are writing a simple script, want to use [LINQ] and do not care about the performance, the SDK provides two methods in the most general interface [IClass], `DescendOnce` and `Descend`, which you can use to loop through the instances.

[LINQ]: https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/
[IClass]: ../api/AasCore.Aas3_0.IClass.yml

Both `DescendOnce` and `Descend` iterate over model children of an [IClass].
`DescendOnce`, as it names suggests, stops after all the children has been iterated over.
`Descend` continues recursively to grand-children *etc.*

Here is a short example how you can get all the properties from an environment whose ID-short starts with `another`:

```cs
using System.Collections.Generic;
using System.Linq;

using Aas = AasCore.Aas3_0;

public class Program
{
    public static void Main()
    {
        // Prepare the environment
        var someProperty = new Aas.Property(
            Aas.DataTypeDefXsd.Boolean)
        {
            IdShort = "someProperty",
        };

        var anotherProperty = new Aas.Property(
            Aas.DataTypeDefXsd.Boolean)
        {
            IdShort = "anotherProperty"
        };

        var yetAnotherProperty = new Aas.Property(
            Aas.DataTypeDefXsd.Boolean)
        {
            IdShort = "yetAnotherProperty"
        };

        var submodel = new Aas.Submodel(
            "someIdShort",
            "some-unique-global-identifier")
        {
            SubmodelElements = new List<Aas.ISubmodelElement>()
            {
                someProperty,
                anotherProperty,
                yetAnotherProperty
            }
        };

        var environment = new Aas.Environment()
        {
            Submodels = new List<Aas.ISubmodel>()
            {
                submodel
            }
        };

        // Iterate over all properties which have "another"
        // in the ID-short
        foreach (
            var prop in environment
                 .Descend()
                 .OfType<Aas.IProperty>()
                 .Where(
                     prop => (
                       prop.IdShort != null
                       && prop.IdShort.ToLower().Contains("another")
                     )
                 )
        )
        {
            System.Console.WriteLine(prop.IdShort);
        }

        // Outputs:
        // anotherProperty
        // yetAnotherProperty
    }
}
```

Iteration with `Descend` and `DescendOnce` works well if the performance is irrelevant.
However, if the performance matters, this is not a good approach.
First, all the children model elements will be visited (even though you need only a small subset).
Second, the call to LINQ's `OfType<Aas.IProperty>` needs to perform a type cast for every child.

Let's see in the next section how we could use a more efficient, but also a more complex approach.

## Visitor

[Visitor pattern] is a common design pattern in software engineering.
We will not explain the details of the pattern here as you can read about in the ample literature in books or in Internet.

The cornerstone of the visitor pattern in [double dispatch]: instead of casting to the desired type during the iteration, we add a method `Accept` to [IClass], whose implementations then directly dispatch to the appropriate method.

[Visitor pattern]: https://en.wikipedia.org/wiki/Visitor_pattern
[double dispatch]: https://en.wikipedia.org/wiki/Double_dispatch

This allows us to spare casts and directly dispatch the execution.
The SDK already implements `Accept` methods, so you only have to implement the visitor.

The visitor class has a visiting method for each class of the meta-model.
In the SDK, we provide different flavors of the visitor abstract classes which you can readily implement:

* [AbstractVisitor] which needs all the visit methods to be implemented,
* [VisitorThrough] which visits all the elements and does nothing, and
* [AbstractVisitorWithContext] which propagates a context object along the iteration.

[AbstractVisitor]: ../api/AasCore.Aas3_0.Visitation.AbstractVisitor.yml
[VisitorThrough]: ../api/AasCore.Aas3_0.Visitation.VisitorThrough.yml
[AbstractVisitorWithContext]: ../api/AasCore.Aas3_0.Visitation.AbstractVisitorWithContext-1.yml

Let us re-write the above example related to `Descend` method with a visitor pattern:

```cs
using System.Collections.Generic;

using Aas = AasCore.Aas3_0;
using AasVisitation = AasCore.Aas3_0.Visitation;

class Visitor : AasVisitation.VisitorThrough
{
    public override void Visit(Aas.Property prop)
    {
        if (prop.IdShort.ToLower().Contains("another"))
        {
            System.Console.WriteLine(prop.IdShort);
        }
    }
};

public class Program
{
    public static void Main()
    {
        // Prepare the environment
        var someProperty = new Aas.Property(
            Aas.DataTypeDefXsd.Boolean)
        {
            IdShort = "someProperty",
        };

        var anotherProperty = new Aas.Property(
            Aas.DataTypeDefXsd.Boolean)
        {
            IdShort = "anotherProperty"
        };

        var yetAnotherProperty = new Aas.Property(
            Aas.DataTypeDefXsd.Boolean)
        {
            IdShort = "yetAnotherProperty"
        };

        var submodel = new Aas.Submodel(
            "someIdShort",
            "some-unique-global-identifier")
        {
            SubmodelElements = new List<Aas.ISubmodelElement>()
            {
                someProperty,
                anotherProperty,
                yetAnotherProperty
            }
        };

        var environment = new Aas.Environment()
        {
            Submodels = new List<Aas.ISubmodel>()
            {
                submodel
            }
        };

        // Iterate over all properties which have "another"
        // in the ID-short
        var visitor = new Visitor();
        visitor.Visit(environment);

        // Outputs:
        // anotherProperty
        // yetAnotherProperty
    }
}
```

There are important differences to iteration with `Descend`:

* Due to [double dispatch], we spare a cast.
  This is usually more efficient.
* We can handle multiple types of the elements, not only a single type (`Property` in this case).
  This can allow for better readability of the code as well as better performance if two or more element types need to be considered in *one* iteration.
* The iteration logic in `Descend` lives very close to where it is executed.
  In contrast, the visitor needs to be defined as a separate class.
  While sometimes faster, writing the visitor makes the code less readable.

## Descend or Visitor?

In general, people familiar with the [visitor pattern] and object-oriented programming will prefer, obviously, visitor class.
People who like LINQ will prefer `Descend`.

It is difficult to discuss different tastes, so you should probably come up with explicit code guidelines in your code and stick to them.

Make sure you always profile before you sacrifice readability and blindly apply one or the other approach for performance reasons.

## Shallow and Deep Copies

In the static class [Copying], we provide methods for making shallow and deep copies of an instance of AAS model.

In both manners of copying, primitive values (such as `bool`, `string` *etc.*) are copied by value.

Shallow copying copies all the non-primitive values by reference.
The lists are also copied by reference, and no new lists are created in the copy.

Deep copying makes a deep copy recursively, where we make a deep copy of all the underlying non-primitive values.

Here is an example of how you can make a shallow and a deep copy of an [Environment]:

```cs
using System.Collections.Generic;
using System.Linq;

using Aas = AasCore.Aas3_0;

public class Program
{
    public static void Main()
    {
          // Prepare the environment
          var someProperty = new Aas.Property(
              Aas.DataTypeDefXsd.Boolean)
          {
              IdShort = "someProperty",
          };

          var submodel = new Aas.Submodel(
              "someIdShort",
              "some-unique-global-identifier")
          {
              SubmodelElements = new List<Aas.ISubmodelElement>()
              {
                  someProperty
              }
          };

          var environment = new Aas.Environment()
          {
              Submodels = new List<Aas.ISubmodel>()
              {
                  submodel
              }
          };

          // Make a deep copy
          var deepCopy = Aas.Copying.Deep(environment);
  
          // Make a shallow copy
          var shallowCopy = Aas.Copying.Shallow(environment);
  
          // Changes to the property affect only the shallow copy,
          // but not the deep one
          environment.Submodels[0].SubmodelElements![0].IdShort = "changed";

          System.Console.WriteLine(
              shallowCopy.Submodels![0].SubmodelElements![0].IdShort);
  
          System.Console.WriteLine(
              deepCopy.Submodels![0].SubmodelElements![0].IdShort);
              
          // Output:
          // changed
          // someProperty
    }
}
```

## Transformer

A transformer pattern is an analogous to [visitor pattern], where we "transform" the visited element into some other form (be it a string or a different object).
It is very common in compiler design, where the abstract syntax tree is transformed into a different representation.

The SDK provides two different flavors of a transformer:

* [AbstractTransformer], where the model element is directly transformed into something, and
* [AbstractTransformerWithContext], which propagates the context object along the transformations.

[AbstractTransformer]: ../api/AasCore.Aas3_0.Visitation.AbstractTransformer-1.yml
[AbstractTransformerWithContext]: ../api/AasCore.Aas3_0.Visitation.AbstractTransformerWithContext-2.yml

Since we need to provide a transformation method for each class of the meta-model, we deliberately omit an example due to the length of the code.
If you need a practical example, see the source code of the [Verification] static class, where we implemented the verification logic using an [AbstractTransformer].

[Verification]: ../api/AasCore.Aas3_0.Verification.yml
