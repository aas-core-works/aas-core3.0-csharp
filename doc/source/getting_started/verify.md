# Verify

Our SDK allows you to verify that a model satisfies the constraints of the meta-model.

The verification logic is concentrated in the static class [Verification], and all it takes is a call to `Verify` method.
The method `Verify` will check that constraints in the given model element are satisfied, including the recursion into children elements.
The method returns an iterator of errors, which you can use to for further processing (*e.g.*, report to the user).

[Verification]: ../api/AasCore.Aas3_0.Verification.yml

Here is a short example snippet:

```cs
using System.Collections.Generic;
using System.Linq;

using Aas = AasCore.Aas3_0;
using AasVerification = AasCore.Aas3_0.Verification;
using AasReporting = AasCore.Aas3_0.Reporting;

public class Program
{
    public static void Main()
    {
        // Prepare the environment
        var someProperty = new Aas.Property(
            Aas.DataTypeDefXsd.Boolean)
        {
            // 🗲🗲💀🗲🗲
            // The ID-shorts must be proper variable names,
            // but there is a dash ("-") in this ID-short.
            IdShort = "some-Property",
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

        // Verify the environment and print out the errors
        foreach (var error in AasVerification.Verify(environment))
        {
            System.Console.WriteLine(
                error.Cause
            );
        }

        // Outputs:
        // Invariant violated:
        // ID-short of Referables shall only feature letters, digits, underscore (``_``);
        // starting mandatory with a letter. *I.e.* ``[a-zA-Z][a-zA-Z0-9_]+``.
    }
}
```

## Reporting

The error is an instance of [Error], living in the scope of the static class [Reporting].
You can use the methods `GenerateJsonPath` and `GenerateRelativeXPath` to convert the error's path to a readable path.

[Error]: ../api/AasCore.Aas3_0.Reporting.Error.yml
[Reporting]: ../api/AasCore.Aas3_0.Reporting.yml

Here is the above snippet modified so that the path is included in the prints:

```cs
// ...

using AasVerification = AasCore.Aas3_0.Verification;
using AasReporting = AasCore.Aas3_0.Reporting;

public class Program
{
    public static void Main()
    {
        // ...

        // Verify the environment and print out the errors
        foreach (var error in AasVerification.Verify(environment))
        {
            System.Console.WriteLine(
                AasReporting.GenerateJsonPath(error.PathSegments)
                + ": "
                + error.Cause
            );
        }

        // Outputs:
        // submodels[0].submodelElements[0].idShort: Invariant violated:
        // ID-short of Referables shall only feature letters, digits, underscore (``_``);
        // starting mandatory with a letter. *I.e.* ``[a-zA-Z][a-zA-Z0-9_]+``.
    }
}
```

## Limit the Number of Reported Errors

Since the `Verify` method of the static class [Verification] gives you an iterator (an [IEnumerable]), you can simply stop the verification after observing a certain number of errors.

[IEnumerable]: https://docs.microsoft.com/en-us/dotnet/api/system.collections.ienumerable

Here is a snippet which reports only the first 10 errors:

```cs

// Verify the environment and print out the first 10 errors
int errorCount = 0;
foreach (var error in AasVerification.Verify(environment))
{
    System.Console.WriteLine(error.Cause);

    errorCount++;
    if (errorCount == 10) break;
}
```

## Omitted Constraints

Not all constraints specified in the meta-model can be verified.
Some constraints require external dependencies such as an AAS registry.
Verifying the constraints with external dependencies is out-of-scope of our SDK, as we still lack standardized interfaces to those dependencies.

However, all the constraints which need no external dependency are verified.
For a full list of exception, consult the [aas-core-meta description of the meta-model] which this SDK has been generated after.

[aas-core-meta description of the meta-model]: https://github.com/aas-core-works/aas-core-meta/blob/931b355682c4a7b84a2fb94932cf09bcf7ce9a1f/aas_core_meta/v3rc2.py#L4
