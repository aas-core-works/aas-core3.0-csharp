using Aas = AasCore.Aas3_0; // renamed

using Nodes = System.Text.Json.Nodes;

using System.Collections.Generic;  // can't alias
using System.Linq;  // can't alias
using NUnit.Framework; // can't alias

namespace AasCore.Aas3_0.Tests
{
    public class TestExamples
    {
        [Test]
        public void Test_create_get_set()
        {
            // Create the first element
            var someElement = new Aas.Property(
                Aas.DataTypeDefXsd.Int)
            {
                IdShort = "someElement",
                Value = "1984"
            };

            // Create the second element
            var content = new byte[]
            {
                0xDE, 0xAD, 0xBE, 0xEF
            };

            var anotherElement = new Aas.Blob(
                "application/octet-stream")
            {
                IdShort = "anotherElement",
                Value = content
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
                (environment
                    .Submodels[0]
                    .SubmodelElements![1] as Aas.Blob)!
            ).Value![3] = 0xEF;

            // Now you can do something with the environment...
        }

        [Test]
        public void Test_descend()
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
                // ReSharper disable once UnusedVariable
                var prop in environment
                    .Descend()
                    .OfType<Aas.Property>()
                    .Where(
                        prop =>
                            prop.IdShort != null
                            && prop.IdShort.ToLower().Contains("another")
                    )
            )
            {
                // System.Console.WriteLine(prop.IdShort);
            }

            // Outputs:
            // anotherProperty
            // yetAnotherProperty
        }

        class Visitor : Aas.Visitation.VisitorThrough
        {
            public override void VisitProperty(Aas.IProperty prop)
            {
                if (
                    prop.IdShort != null
                    && prop.IdShort.ToLower().Contains("another")
                )
                {
                    // System.Console.WriteLine(prop.IdShort);
                }
            }
        };


        [Test]
        public void Test_visitor()
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

        [Test]
        public void Test_shallow_and_deep_copy()
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

            var environment = new Aas.Environment()
            {
                Submodels = new List<Aas.ISubmodel>()
                {
                    submodel
                }
            };

            // Make a deep copy
            // ReSharper disable once UnusedVariable
            var deepCopy = Aas.Copying.Deep(environment);

            // Make a shallow copy
            // ReSharper disable once UnusedVariable
            var shallowCopy = Aas.Copying.Shallow(environment);

            // Changes to the property affect only the shallow copy,
            // but not the deep one
            environment.Submodels[0].SubmodelElements![0].IdShort = "changed";

            // System.Console.WriteLine(
            //     shallowCopy.Submodels![0].SubmodelElements![0].IdShort);
            //
            // System.Console.WriteLine(
            //     deepCopy.Submodels![0].SubmodelElements![0].IdShort);

            // Output:
            // changed
            // someProperty
        }

        [Test]
        public void Test_JSON_serialization()
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

            var environment = new Aas.Environment()
            {
                Submodels = new List<Aas.ISubmodel>()
                {
                    submodel
                }
            };

            // Serialize to a JSON object
            // ReSharper disable once UnusedVariable
            var jsonObject = Aas.Jsonization.Serialize.ToJsonObject(
                environment
            );

            // Print the JSON object
            // System.Console.WriteLine(jsonObject);

            // Outputs:
            // {
            //   "submodels": [
            //     {
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

        [Test]
        public void Test_JSON_deserialization()
        {
            var text = @"{
  ""submodels"": [
    {
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
                Aas.Jsonization.Deserialize.EnvironmentFrom(
                    jsonNode!)
            );

            // Print the types of the model elements contained
            // in the environment
            // ReSharper disable once UnusedVariable
            foreach (var something in environment.Descend())
            {
                // System.Console.WriteLine(something.GetType());
            }

            // Outputs:
            // AasCore.Aas3_0.Submodel
            // AasCore.Aas3_0.Property
        }

        [Test]
        public void Test_XML_serialization()
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

            var environment = new Aas.Environment()
            {
                Submodels = new List<Aas.ISubmodel>()
                {
                    submodel
                }
            };

            // Serialize to an XML writer
            var outputBuilder = new System.Text.StringBuilder();
            using var writer = System.Xml.XmlWriter.Create(
                outputBuilder,
                new System.Xml.XmlWriterSettings()
                {
                    Encoding = System.Text.Encoding.UTF8,
                    OmitXmlDeclaration = true
                }
            );

            Aas.Xmlization.Serialize.To(
                environment,
                writer
            );

            writer.Flush();
            Assert.AreEqual(
                "<environment xmlns=\"https://admin-shell.io/aas/3/0\">" +
                "<submodels><submodel>" +
                "<id>some-unique-global-identifier</id>" +
                "<submodelElements><property><idShort>someProperty</idShort>" +
                "<valueType>xs:boolean</valueType></property></submodelElements>" +
                "</submodel></submodels></environment>",
                outputBuilder.ToString());
        }

        [Test]
        public void Test_XML_deserialization()
        {
            var text = (
                "<?xml version=\"1.0\" encoding=\"utf-8\"?>" +
                "<environment xmlns=\"https://admin-shell.io/aas/3/0\">" +
                "<submodels><submodel>" +
                "<id>some-unique-global-identifier</id>" +
                "<submodelElements><property><idShort>someProperty</idShort>" +
                "<valueType>xs:boolean</valueType></property></submodelElements>" +
                "</submodel></submodels></environment>"
            );

            using var stringReader = new System.IO.StringReader(
                text);

            using var xmlReader = System.Xml.XmlReader.Create(
                stringReader);

            // This step is necessary to skip the non-content. Otherwise,
            // the deserialization would have thrown an exception.
            xmlReader.MoveToContent();

            var environment = Aas.Xmlization.Deserialize.EnvironmentFrom(
                xmlReader);

            // Print the types of the model elements contained
            // in the environment
            // ReSharper disable once UnusedVariable
            foreach (var something in environment.Descend())
            {
                // System.Console.WriteLine(something.GetType());
            }

            // Outputs:
            // AasCore.Aas3_0.Submodel
            // AasCore.Aas3_0.Property
        }

        class Enhancement
        {
            // ReSharper disable once NotAccessedField.Local
            public Aas.IClass? Parent;
        }

        [Test]
        public void Test_enhancing()
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

            // Enhance with parent
            environment = (Aas.IEnvironment)enhancer.Wrap(environment);

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
            // System.Console.WriteLine(
            //     enhancer.MustUnwrap(environment.Submodels![0]).Parent == environment
            // );

            // Prints:
            // True
        }

        class IdEnhancement
        {
            // ReSharper disable once MemberCanBePrivate.Local
            // ReSharper disable once NotAccessedField.Local
            public long Id;

            public IdEnhancement(long id)
            {
                Id = id;
            }
        }

        private Aas.IEnvironment EnhanceSeparatedFromUnwrapping(Aas.IEnvironment environment)
        {
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
            return (Aas.IEnvironment)enhancer.Wrap(environment);
        }
        
        [Test]
        public void Test_selective_enhancing()
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

            // Enhance
            environment = EnhanceSeparatedFromUnwrapping(environment); 
            
            // Define the unwrapping
            var unwrapper = new Aas.Enhancing.Unwrapper<IdEnhancement>();
            
            // The submodel and property are enhanced.
            // ReSharper disable once NotAccessedVariable
            IdEnhancement enhancement = unwrapper.MustUnwrap(environment.Submodels![0]);
            
            Assert.AreEqual(2, enhancement.Id);
        }
    }
}