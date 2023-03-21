# JSON De/serialization

Our SDK handles the de/serialization of the AAS models from and to JSON format through the static class [Jsonization].

[Jsonization]: ../api/AasCore.Aas3_0.Jsonization.yml

## Serialize

To serialize, you call the method `ToJsonObject` of [Jsonization.Serialize] static class on an instance of [Environment] which will convert it to an instance of [System.Text.Json.Nodes.JsonObject].

[Jsonization.Serialize]: ../api/AasCore.Aas3_0.Jsonization.Serialize.yml
[Environment]: ../api/AasCore.Aas3_0.Environment.yml
[System.Text.Json.Nodes.JsonObject]: https://docs.microsoft.com/en-us/dotnet/api/system.text.json.nodes.jsonobject

Here is a snippet that converts the environment first into an [System.Text.Json.Nodes.JsonObject], and next converts the JSON object to text:

```cs
using System.Collections.Generic;

using Aas = AasCore.Aas3_0;
using AasJsonization = AasCore.Aas3_0.Jsonization;

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

        // Serialize to a JSON object
        var jsonObject = AasJsonization.Serialize.ToJsonObject(
            environment
        );

        // Print the JSON object
        System.Console.WriteLine(jsonObject);

        // Outputs:
        // {
        //   "submodels": [
        //     {
        //       "idShort": "someIdShort",
        //       "id": "some-unique-global-identifier",
        //       "submodelElements": [
        //         {
        //           "idShort": "someProperty",
        //           "valueType": "xs:boolean",
        //           "modelType": "Property"
        //         }
        //       ],
        //       "modelType": "Submodel"
        //     }
        //   ]
        // }
    }
}
```

## De-serialize

Our SDK can convert a [System.Text.Json.Nodes.JsonNode] back to an instance of [Environment].
All you have to do is call the method `EnvironmentFrom` from the static class [Jsonization.Deserialize].

[System.Text.Json.Nodes.JsonNode]: https://docs.microsoft.com/en-us/dotnet/api/system.text.json.nodes.jsonnode
[Environment]: ../api/AasCore.Aas3_0.Environment.yml
[Jsonization.Deserialize]: ../api/AasCore.Aas3_0.Jsonization.Deserialize.yml

Here is an example snippet:

```cs
using Nodes = System.Text.Json.Nodes;

using Aas = AasCore.Aas3_0;
using AasJsonization = AasCore.Aas3_0.Jsonization;

public class Program
{
    public static void Main()
    {
        var text = @"{
  ""submodels"": [
    {
      ""idShort"": ""someIdShort"",
      ""id"": ""some-unique-global-identifier"",
      ""submodelElements"": [
        {
          ""idShort"": ""someProperty"",
          ""valueType"": ""xs:boolean"",
          ""modelType"": ""Property""
        }
      ],
      ""modelType"": ""Submodel""
    }
  ]
}";
        var jsonNode = Nodes.JsonNode.Parse(
            text);

        // De-serialize from the JSON node
        Aas.Environment environment = (
            AasJsonization.Deserialize.EnvironmentFrom(
                jsonNode)
        );

        // Print the types of the model elements contained
        // in the environment
        foreach (var something in environment.Descend())
        {
            System.Console.WriteLine(something.GetType());
        }

        // Outputs:
        // AasCore.Aas3_0.Submodel
        // AasCore.Aas3_0.Property
    }
}
```

### Errors

If there are any errors during the de-serialization, a [Jsonization.Exception] will be thrown.
Errors occur whenever we encounter invalid JSON values.
For example, the de-serialization method expects a JSON object, but encounters a JSON array instead.

[Jsonization.Exception]: ../api/AasCore.Aas3_0.Jsonization.Exception.yml
