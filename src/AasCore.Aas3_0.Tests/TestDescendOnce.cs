/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */

using Aas = AasCore.Aas3_0;  // renamed
using Directory = System.IO.Directory;
using Path = System.IO.Path;

using NUnit.Framework; // can't alias

namespace AasCore.Aas3_0.Tests
{
    public class TestDescendOnce
    {
        private static void CompareOrRerecordTrace(
            IClass instance,
            string expectedPath)
        {
            var writer = new System.IO.StringWriter();
            foreach (var descendant in instance.DescendOnce())
            {
                switch (descendant)
                {
                    case IIdentifiable identifiable:
                        {
                            writer.WriteLine(
                                $"{identifiable.GetType()} with ID {identifiable.Id}");
                            break;
                        }
                    case IReferable referable:
                        {
                            writer.WriteLine(
                                $"{referable.GetType()} with ID-short {referable.IdShort}");
                            break;
                        }
                    default:
                        {
                            writer.WriteLine(descendant.GetType().Name);
                            break;
                        }
                }
            }

            string got = writer.ToString();

            if (Aas.Tests.Common.RecordMode)
            {
                string? parent = Path.GetDirectoryName(expectedPath);
                if (parent != null)
                {
                    if (!Directory.Exists(parent))
                    {
                        Directory.CreateDirectory(parent);
                    }
                }

                System.IO.File.WriteAllText(expectedPath, got);
            }
            else
            {
                if (!System.IO.File.Exists(expectedPath))
                {
                    throw new System.IO.FileNotFoundException(
                        $"The file with the recorded trace does not exist: {expectedPath}");
                }

                string expected = System.IO.File.ReadAllText(expectedPath);
                Assert.AreEqual(
                    expected.Replace("\r\n", "\n"),
                    got.Replace("\r\n", "\n"),
                    $"The expected trace from {expectedPath} does not match the actual one");
            }
        }

        [Test]
        public void Test_Extension()
        {
            Aas.Extension instance = (
                Aas.Tests.CommonJsonization.LoadMaximalExtension());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Extension",
                    "maximal.json.trace"));
        }  // public void Test_Extension

        [Test]
        public void Test_AdministrativeInformation()
        {
            Aas.AdministrativeInformation instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAdministrativeInformation());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "AdministrativeInformation",
                    "maximal.json.trace"));
        }  // public void Test_AdministrativeInformation

        [Test]
        public void Test_Qualifier()
        {
            Aas.Qualifier instance = (
                Aas.Tests.CommonJsonization.LoadMaximalQualifier());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Qualifier",
                    "maximal.json.trace"));
        }  // public void Test_Qualifier

        [Test]
        public void Test_AssetAdministrationShell()
        {
            Aas.AssetAdministrationShell instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAssetAdministrationShell());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "AssetAdministrationShell",
                    "maximal.json.trace"));
        }  // public void Test_AssetAdministrationShell

        [Test]
        public void Test_AssetInformation()
        {
            Aas.AssetInformation instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAssetInformation());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "AssetInformation",
                    "maximal.json.trace"));
        }  // public void Test_AssetInformation

        [Test]
        public void Test_Resource()
        {
            Aas.Resource instance = (
                Aas.Tests.CommonJsonization.LoadMaximalResource());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Resource",
                    "maximal.json.trace"));
        }  // public void Test_Resource

        [Test]
        public void Test_SpecificAssetId()
        {
            Aas.SpecificAssetId instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSpecificAssetId());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "SpecificAssetId",
                    "maximal.json.trace"));
        }  // public void Test_SpecificAssetId

        [Test]
        public void Test_Submodel()
        {
            Aas.Submodel instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodel());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Submodel",
                    "maximal.json.trace"));
        }  // public void Test_Submodel

        [Test]
        public void Test_RelationshipElement()
        {
            Aas.RelationshipElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalRelationshipElement());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "RelationshipElement",
                    "maximal.json.trace"));
        }  // public void Test_RelationshipElement

        [Test]
        public void Test_SubmodelElementList()
        {
            Aas.SubmodelElementList instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodelElementList());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "SubmodelElementList",
                    "maximal.json.trace"));
        }  // public void Test_SubmodelElementList

        [Test]
        public void Test_SubmodelElementCollection()
        {
            Aas.SubmodelElementCollection instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodelElementCollection());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "SubmodelElementCollection",
                    "maximal.json.trace"));
        }  // public void Test_SubmodelElementCollection

        [Test]
        public void Test_Property()
        {
            Aas.Property instance = (
                Aas.Tests.CommonJsonization.LoadMaximalProperty());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Property",
                    "maximal.json.trace"));
        }  // public void Test_Property

        [Test]
        public void Test_MultiLanguageProperty()
        {
            Aas.MultiLanguageProperty instance = (
                Aas.Tests.CommonJsonization.LoadMaximalMultiLanguageProperty());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "MultiLanguageProperty",
                    "maximal.json.trace"));
        }  // public void Test_MultiLanguageProperty

        [Test]
        public void Test_Range()
        {
            Aas.Range instance = (
                Aas.Tests.CommonJsonization.LoadMaximalRange());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Range",
                    "maximal.json.trace"));
        }  // public void Test_Range

        [Test]
        public void Test_ReferenceElement()
        {
            Aas.ReferenceElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalReferenceElement());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "ReferenceElement",
                    "maximal.json.trace"));
        }  // public void Test_ReferenceElement

        [Test]
        public void Test_Blob()
        {
            Aas.Blob instance = (
                Aas.Tests.CommonJsonization.LoadMaximalBlob());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Blob",
                    "maximal.json.trace"));
        }  // public void Test_Blob

        [Test]
        public void Test_File()
        {
            Aas.File instance = (
                Aas.Tests.CommonJsonization.LoadMaximalFile());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "File",
                    "maximal.json.trace"));
        }  // public void Test_File

        [Test]
        public void Test_AnnotatedRelationshipElement()
        {
            Aas.AnnotatedRelationshipElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAnnotatedRelationshipElement());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "AnnotatedRelationshipElement",
                    "maximal.json.trace"));
        }  // public void Test_AnnotatedRelationshipElement

        [Test]
        public void Test_Entity()
        {
            Aas.Entity instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEntity());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Entity",
                    "maximal.json.trace"));
        }  // public void Test_Entity

        [Test]
        public void Test_EventPayload()
        {
            Aas.EventPayload instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEventPayload());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "EventPayload",
                    "maximal.json.trace"));
        }  // public void Test_EventPayload

        [Test]
        public void Test_BasicEventElement()
        {
            Aas.BasicEventElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalBasicEventElement());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "BasicEventElement",
                    "maximal.json.trace"));
        }  // public void Test_BasicEventElement

        [Test]
        public void Test_Operation()
        {
            Aas.Operation instance = (
                Aas.Tests.CommonJsonization.LoadMaximalOperation());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Operation",
                    "maximal.json.trace"));
        }  // public void Test_Operation

        [Test]
        public void Test_OperationVariable()
        {
            Aas.OperationVariable instance = (
                Aas.Tests.CommonJsonization.LoadMaximalOperationVariable());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "OperationVariable",
                    "maximal.json.trace"));
        }  // public void Test_OperationVariable

        [Test]
        public void Test_Capability()
        {
            Aas.Capability instance = (
                Aas.Tests.CommonJsonization.LoadMaximalCapability());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Capability",
                    "maximal.json.trace"));
        }  // public void Test_Capability

        [Test]
        public void Test_ConceptDescription()
        {
            Aas.ConceptDescription instance = (
                Aas.Tests.CommonJsonization.LoadMaximalConceptDescription());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "ConceptDescription",
                    "maximal.json.trace"));
        }  // public void Test_ConceptDescription

        [Test]
        public void Test_Reference()
        {
            Aas.Reference instance = (
                Aas.Tests.CommonJsonization.LoadMaximalReference());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Reference",
                    "maximal.json.trace"));
        }  // public void Test_Reference

        [Test]
        public void Test_Key()
        {
            Aas.Key instance = (
                Aas.Tests.CommonJsonization.LoadMaximalKey());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Key",
                    "maximal.json.trace"));
        }  // public void Test_Key

        [Test]
        public void Test_LangStringNameType()
        {
            Aas.LangStringNameType instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringNameType());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "LangStringNameType",
                    "maximal.json.trace"));
        }  // public void Test_LangStringNameType

        [Test]
        public void Test_LangStringTextType()
        {
            Aas.LangStringTextType instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringTextType());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "LangStringTextType",
                    "maximal.json.trace"));
        }  // public void Test_LangStringTextType

        [Test]
        public void Test_Environment()
        {
            Aas.Environment instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEnvironment());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "Environment",
                    "maximal.json.trace"));
        }  // public void Test_Environment

        [Test]
        public void Test_EmbeddedDataSpecification()
        {
            Aas.EmbeddedDataSpecification instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEmbeddedDataSpecification());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "EmbeddedDataSpecification",
                    "maximal.json.trace"));
        }  // public void Test_EmbeddedDataSpecification

        [Test]
        public void Test_LevelType()
        {
            Aas.LevelType instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLevelType());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "LevelType",
                    "maximal.json.trace"));
        }  // public void Test_LevelType

        [Test]
        public void Test_ValueReferencePair()
        {
            Aas.ValueReferencePair instance = (
                Aas.Tests.CommonJsonization.LoadMaximalValueReferencePair());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "ValueReferencePair",
                    "maximal.json.trace"));
        }  // public void Test_ValueReferencePair

        [Test]
        public void Test_ValueList()
        {
            Aas.ValueList instance = (
                Aas.Tests.CommonJsonization.LoadMaximalValueList());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "ValueList",
                    "maximal.json.trace"));
        }  // public void Test_ValueList

        [Test]
        public void Test_LangStringPreferredNameTypeIec61360()
        {
            Aas.LangStringPreferredNameTypeIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringPreferredNameTypeIec61360());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "LangStringPreferredNameTypeIec61360",
                    "maximal.json.trace"));
        }  // public void Test_LangStringPreferredNameTypeIec61360

        [Test]
        public void Test_LangStringShortNameTypeIec61360()
        {
            Aas.LangStringShortNameTypeIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringShortNameTypeIec61360());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "LangStringShortNameTypeIec61360",
                    "maximal.json.trace"));
        }  // public void Test_LangStringShortNameTypeIec61360

        [Test]
        public void Test_LangStringDefinitionTypeIec61360()
        {
            Aas.LangStringDefinitionTypeIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringDefinitionTypeIec61360());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "LangStringDefinitionTypeIec61360",
                    "maximal.json.trace"));
        }  // public void Test_LangStringDefinitionTypeIec61360

        [Test]
        public void Test_DataSpecificationIec61360()
        {
            Aas.DataSpecificationIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalDataSpecificationIec61360());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "DescendOnce",
                    "DataSpecificationIec61360",
                    "maximal.json.trace"));
        }  // public void Test_DataSpecificationIec61360
    }  // class TestDescendOnce
}  // namespace AasCore.Aas3_0.Tests

/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */
