# Enhancing

In any complex application, creating, modifying and de/serializing AAS instances is not enough.
You have to insert your custom application-specific data to the model in order for the model to be useful.

Take, for example, parent-child relationship.
The current library ignores it, and there is no easy way for you to find out to which [Submodel] a particular [ISubmodelElement] belongs to.

[Submodel]: ../api/AasCore.Aas3_0.Submodel.yml
[ISubmodelElement]: ../api/AasCore.Aas3_0.ISubmodelElement.yml

We did want to keep the types as simple as possible — the parent-child relationships can get tricky very soon if you have multiple environments with shared submodels *etc.*
Instead of overcomplicating the code and making it barely traceable, we decided to keep it simple and frugal in features.

However, that is little solace if you are developing an GUI editor where you know for sure that there will be only one environment, and where parent-child relationships are crucial for so many tasks.
What is more, parent-child relationships are not the only data that need to be intertwined — you probably want history, localized caches *etc.*

## Hasthable?

There are different ways how application-specific data can be synced with the model.
One popular technique is to use [Hashtable]'s and simply map model instances to your custom nuggets of data.
This works well if the data is read-only, and you can spare the cycles for the lookups (which is often acceptable as they run on average in time complexity `O(1)` anyhow).

[Hashtable]: https://learn.microsoft.com/en-US/dotnet/api/system.collections.hashtable

Otherwise, if you need to modify the data, maintaining the consistency between the [Hashtable] and your nuggets becomes difficult.
For example, if you forget to remove the entries from the [Hashtable] when you remove the instances from the model, you might clog your garbage collector.

## Wrapping

Hence, if you modify the data, you need to keep it close to the model instance.
In dynamic languages, such as Python and JavaScript, you can simply add your custom fields to the object.
This does not work in such a static language like C#.

One solution, usually called [Decorator pattern], is to *wrap* or *decorate* the instances with your application-specific data.
The decorated objects should satisfy both the interface of the original model and provide a way to retrieve your custom nuggets of information.

[Decorator pattern]: https://en.wikipedia.org/wiki/Decorator_pattern

Writing wrappers for many classes in the AAS meta-model is a tedious task.
We therefore pre-generated the most of the boilerplate code in the static class [Enhancing].

[Enhancing]: ../api/AasCore.Aas3_0.Enhancing.yml

In the context of decoration, we call your specific data *enhancements*.
First, you need to specify how individual instances are enhanced, *i.e.* how to produce enhancements for each one of them.
We call this an *enhancement factory*.
Second, you need to recursively wrap your instances with the given enhancement factory.

The [Enhancing] is generic and can work with any form of enhancement classes.
You need to specify your enhancement factory as a [function delegate] which takes an instance of [IClass] as input and returns an enhancement, or `null`, if you do not want to enhance the particular instance.

[function delegate]: https://learn.microsoft.com/en-us/dotnet/api/system.func-2
[IClass]: ../api/AasCore.Aas3_0.IClass.yml

The wrapping and unwrapping is specified in the generic class [Enhancer], which takes the enhancement factory as the only argument.

[Enhancer]: ../api/AasCore.Aas3_0.Enhancing.Enhancer-1.yml

The methods `Enhancer.Wrap` and `Enhancer.Unwrap` perform the wrapping and unwrapping, respectively.
The method `Enhancer.MustWrap` is a shortcut method that spares you a non-null check of `Enhancer.Unwrap`.

## Example: Parent-Child Enhancement

Let us now consider the aforementioned example.
We want to keep track of parent-child relationships in a model.

The following code snippets first constructs an environment for illustration.
Then we specify the enhancement such that each instance is initialized with the parent set to `null`.
Finally, we modify the enhancements such that they reflect the parent-child relationships.

```cs
using Aas = AasCore.Aas3_0;
using AasEnhancing = AasCore.Aas3_0.Enhancing;

using System.Linq;
using System.Collections.Generic;

public class Program
{
    class Enhancement
    {
        public Aas.IClass? Parent = null;
    }

    public static void Main()
    {
        // Prepare the environment
        var someProperty = new Aas.Property(
            Aas.DataTypeDefXsd.Boolean)
        {
            IdShort = "someProperty",
        };

        var submodel = new Aas.Submodel(
            "some-unique-global-identifier")
        {
            SubmodelElements = new List<Aas.ISubmodelElement>()
            {
                someProperty
            }
        };

        Aas.IEnvironment environment = new Aas.Environment()
        {
            Submodels = new List<Aas.ISubmodel>()
            {
                submodel
            }
        };

        // Prepare the enhancer
        var enhancer = new Aas.Enhancing.Enhancer<Enhancement>(
            (instance => new Enhancement())
        );

        // Enhance with parent set to `null`
        environment = (Aas.IEnvironment) enhancer.Wrap(environment);

        var queue = new Queue<Aas.IClass>();
        queue.Enqueue(environment);
        while (queue.Count > 0)
        {
            var instance = queue.Dequeue();
            foreach (var child in instance.DescendOnce())
            {
                enhancer.MustUnwrap(child).Parent = instance;
                queue.Enqueue(child);
            }
        }

        // Retrieve the parent of the first submodel
        System.Console.WriteLine(
            enhancer.MustUnwrap(environment.Submodels![0]).Parent 
            == environment
        );

        // Prints:
        // True
    }
}
```

Note that this approach is indeed more maintainable than the one with [Hashtable], but you still need to take extra care.
If you create new submodels and insert them into the environment, you have to make sure that you wrap them appropriately.
If you move a submodel from one environment to another, you have to update the parent link manually *etc.*

## Example: Selective Enhancement

We demonstrate now how you can selectively enhance only some instances in the [Environment].

For example, let us assign a unique identifier to all instances which are referable, *i.e.*, implement [IReferable].
All the other instances are not enhanced.

[IReferable]: ../api/AasCore.Aas3_0.IReferable.yml
[Environment]: ../api/AasCore.Aas3_0.Environment.yml

```cs
using Aas = AasCore.Aas3_0;
using AasEnhancing = AasCore.Aas3_0.Enhancing;

using System.Linq;
using System.Collections.Generic;

public class Program
{
    class IdEnhancement
    {
        public long Id;

        public IdEnhancement(long id)
        {
            Id = id;
        }
    }

    public static void Main()
    {
        // Prepare the environment
        Aas.IEnvironment environment = new Aas.Environment()
        {
            Submodels = new List<Aas.ISubmodel>()
            {
                new Aas.Submodel(
                    "some-unique-global-identifier")
                {
                    SubmodelElements = new List<Aas.ISubmodelElement>()
                    {
                        new Aas.Property(
                            Aas.DataTypeDefXsd.Boolean)
                        {
                            IdShort = "someProperty",
                        }
                    },
                    Administration = new Aas.AdministrativeInformation()
                    {
                        Version="1.0"
                    }
                }
            }
        };

        // Prepare the enhancer
        long lastId = 0;
        var enhancementFactory = new System.Func<IClass, IdEnhancement?>(
            instance =>
            {
                if (instance is Aas.IReferable)
                {
                    lastId++;
                    return new IdEnhancement(lastId);
                }

                return null;
            }
        );

        var enhancer = new Aas.Enhancing.Enhancer<IdEnhancement>(
            enhancementFactory
        );

        // Enhance
        environment = (Aas.IEnvironment)enhancer.Wrap(environment);

        // The submodel and property are enhanced.
        IdEnhancement enhancement = enhancer.MustUnwrap(environment.Submodels![0]);
        System.Console.WriteLine(enhancement.Id);

        // Prints:
        // 2

        enhancement = enhancer.MustUnwrap(environment.Submodels![0].SubmodelElements![0]);
        System.Console.WriteLine(enhancement.Id);

        // Prints:
        // 1

        // The administrative information is not referable, and thus not enhanced.
        IdEnhancement? maybeEnhancement = enhancer.Unwrap(
            environment.Submodels![0].Administration!
        );

        System.Console.WriteLine(maybeEnhancement == null);

        // Prints:
        // True
    }
}
```

## No Re-wraps Allowed

We disallow re-wraps of already wrapped instances to avoid costly iterations over the object trees, and throw an exception.
Additionally, we want to prevent bugs in many settings where the enhancement factory assigns unique identifiers to instances or performs non-idempotent operations.

Please let us know by [creating an issue] if you need re-wraps to be allowed, and please tell us more about your particular scenario.

[create an issue]: https://github.com/aas-core-works/aas-core3.0-csharp/issues/new
