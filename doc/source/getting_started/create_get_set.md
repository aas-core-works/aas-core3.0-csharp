# Create, Get and Set Properties of an AAS Model

The namespace [AasCore.Aas3_0](../api/AasCore.Aas3_0.yml) contains all the classes of the meta-model.

You can simply use their constructors to create an AAS model.

Usually you start bottom-up, all the way up to the [AasCore.Aas3_0.Environment](../api/AasCore.Aas3_0.Environment.yml).

## Getters and Setters

For each property in the meta-model, there is a corresponding getter and setter.

For example, see the getter and setter for [AasCore.Aas3_0.Submodel.Category].

[AasCore.Aas3_0.Submodel.Category]: ../api/AasCore.Aas3_0.Submodel.yml#AasCore_Aas3_0_Submodel_Category

## Getters with a Default Value

For optional properties which come with a default value, we provide special getters, `{property name}OrDefault`.
If the property has not been set, this getter will give you the default value.
Otherwise, if the model sets the property, the value of the property will be returned.

For example, see [AasCore.Aas3_0.Submodel.KindOrDefault].

[AasCore.Aas3_0.Submodel.KindOrDefault]: ../api/AasCore.Aas3_0.Submodel.yml#AasCore_Aas3_0_Submodel_KindOrDefault

## Example: Create an environment with a submodel

Here is a very rudimentary example where we show how to create an environment which contains a submodel.

The submodel will contain two elements, a property and a blob.

(We will alias the namespace `AasCore.Aas3_0` to `Aas` for readability.
You might or might not want to write your code like that; the aliasing is not necessary.)

```cs
using System.Collections.Generic;

using Aas = AasCore.Aas3_0;
					
public class Program
{
	public static void Main()
	{
		// Create the first element
		var someElement = new Aas.Property(
			Aas.DataTypeDefXsd.Int)
		{
			Value="1984"
		};
		
		// Create the second element
		var content = new byte[]
		{
			0xDE, 0xAD, 0xBE, 0xEF
		};
		
		var anotherElement = new Aas.Blob(
			"application/octet-stream")
		{
			Value=content
		};
		
		// You can also directly access the element properties
		anotherElement.Value[3] = 0xED;
		
		// Nest the elements in a submodel
		var elements = new List<Aas.ISubmodelElement>()
		{
			someElement,
			anotherElement
		};
		
		var submodel = new Aas.Submodel(
			"some-unique-global-identifier")
		{
			SubmodelElements = elements
		};
		
		// Now create the environment to wrap it all
		var submodels = new List<Aas.ISubmodel>()
		{
			submodel
		};
		
		var environment = new Aas.Environment()
		{
			Submodels = submodels
		};
		
		// You can access the properties from the children
		// as well.
		(
			environment
			.Submodels[0]
			.SubmodelElements[1] as Aas.Blob
		).Value[3] = 0xEF;
		
		// Now you can do something with the environment...
	}
}
```
