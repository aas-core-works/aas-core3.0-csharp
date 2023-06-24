/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */

using Aas = AasCore.Aas3_0;  // renamed
using Directory = System.IO.Directory;
using Path = System.IO.Path;

using NUnit.Framework; // can't alias
using System.Collections.Generic;  // can't alias

namespace AasCore.Aas3_0.Tests
{
    public class TestDescendAndVisitorThrough
    {
        private static string Trace(Aas.IClass instance)
        {
            switch (instance)
            {
                case IIdentifiable identifiable:
                    {
                        return $"{identifiable.GetType()} with ID {identifiable.Id}";
                    }
                case IReferable referable:
                    {
                        return $"{referable.GetType()} with ID-short {referable.IdShort}";
                    }
                default:
                    {
                        return instance.GetType().Name;
                    }
            }
        }

        class TracingVisitorThrough : Aas.Visitation.VisitorThrough
        {
            public readonly List<string> Log = new List<string>();

            public override void Visit(IClass that)
            {
                Log.Add(Trace(that));
                base.Visit(that);
            }
        }

        private static void AssertDescendAndVisitorThroughSame(
            Aas.IClass instance)
        {
            var logFromDescend = new List<string>();
            foreach (var subInstance in instance.Descend())
            {
                logFromDescend.Add(Trace(subInstance));
            }

            var visitor = new TracingVisitorThrough();
            visitor.Visit(instance);
            var traceFromVisitor = visitor.Log;

            Assert.IsNotEmpty(traceFromVisitor);

            Assert.AreEqual(
                Trace(instance),
                traceFromVisitor[0]);

            traceFromVisitor.RemoveAt(0);

            Assert.That(traceFromVisitor, Is.EquivalentTo(logFromDescend));
        }

        private static void CompareOrRerecordTrace(
            IClass instance,
            string expectedPath)
        {
            var writer = new System.IO.StringWriter();
            foreach (var descendant in instance.Descend())
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
        public void Test_Descend_of_Extension()
        {
            Aas.Extension instance = (
                Aas.Tests.CommonJsonization.LoadMaximalExtension());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Extension",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Extension

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Extension()
        {
            Aas.Extension instance = (
                Aas.Tests.CommonJsonization.LoadMaximalExtension());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Extension

        [Test]
        public void Test_Descend_of_AdministrativeInformation()
        {
            Aas.AdministrativeInformation instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAdministrativeInformation());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "AdministrativeInformation",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_AdministrativeInformation

        [Test]
        public void Test_Descend_against_VisitorThrough_for_AdministrativeInformation()
        {
            Aas.AdministrativeInformation instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAdministrativeInformation());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_AdministrativeInformation

        [Test]
        public void Test_Descend_of_Qualifier()
        {
            Aas.Qualifier instance = (
                Aas.Tests.CommonJsonization.LoadMaximalQualifier());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Qualifier",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Qualifier

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Qualifier()
        {
            Aas.Qualifier instance = (
                Aas.Tests.CommonJsonization.LoadMaximalQualifier());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Qualifier

        [Test]
        public void Test_Descend_of_AssetAdministrationShell()
        {
            Aas.AssetAdministrationShell instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAssetAdministrationShell());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "AssetAdministrationShell",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_AssetAdministrationShell

        [Test]
        public void Test_Descend_against_VisitorThrough_for_AssetAdministrationShell()
        {
            Aas.AssetAdministrationShell instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAssetAdministrationShell());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_AssetAdministrationShell

        [Test]
        public void Test_Descend_of_AssetInformation()
        {
            Aas.AssetInformation instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAssetInformation());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "AssetInformation",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_AssetInformation

        [Test]
        public void Test_Descend_against_VisitorThrough_for_AssetInformation()
        {
            Aas.AssetInformation instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAssetInformation());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_AssetInformation

        [Test]
        public void Test_Descend_of_Resource()
        {
            Aas.Resource instance = (
                Aas.Tests.CommonJsonization.LoadMaximalResource());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Resource",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Resource

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Resource()
        {
            Aas.Resource instance = (
                Aas.Tests.CommonJsonization.LoadMaximalResource());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Resource

        [Test]
        public void Test_Descend_of_SpecificAssetId()
        {
            Aas.SpecificAssetId instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSpecificAssetId());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "SpecificAssetId",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_SpecificAssetId

        [Test]
        public void Test_Descend_against_VisitorThrough_for_SpecificAssetId()
        {
            Aas.SpecificAssetId instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSpecificAssetId());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_SpecificAssetId

        [Test]
        public void Test_Descend_of_Submodel()
        {
            Aas.Submodel instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodel());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Submodel",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Submodel

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Submodel()
        {
            Aas.Submodel instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodel());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Submodel

        [Test]
        public void Test_Descend_of_RelationshipElement()
        {
            Aas.RelationshipElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalRelationshipElement());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "RelationshipElement",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_RelationshipElement

        [Test]
        public void Test_Descend_against_VisitorThrough_for_RelationshipElement()
        {
            Aas.RelationshipElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalRelationshipElement());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_RelationshipElement

        [Test]
        public void Test_Descend_of_SubmodelElementList()
        {
            Aas.SubmodelElementList instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodelElementList());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "SubmodelElementList",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_SubmodelElementList

        [Test]
        public void Test_Descend_against_VisitorThrough_for_SubmodelElementList()
        {
            Aas.SubmodelElementList instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodelElementList());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_SubmodelElementList

        [Test]
        public void Test_Descend_of_SubmodelElementCollection()
        {
            Aas.SubmodelElementCollection instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodelElementCollection());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "SubmodelElementCollection",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_SubmodelElementCollection

        [Test]
        public void Test_Descend_against_VisitorThrough_for_SubmodelElementCollection()
        {
            Aas.SubmodelElementCollection instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodelElementCollection());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_SubmodelElementCollection

        [Test]
        public void Test_Descend_of_Property()
        {
            Aas.Property instance = (
                Aas.Tests.CommonJsonization.LoadMaximalProperty());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Property",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Property

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Property()
        {
            Aas.Property instance = (
                Aas.Tests.CommonJsonization.LoadMaximalProperty());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Property

        [Test]
        public void Test_Descend_of_MultiLanguageProperty()
        {
            Aas.MultiLanguageProperty instance = (
                Aas.Tests.CommonJsonization.LoadMaximalMultiLanguageProperty());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "MultiLanguageProperty",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_MultiLanguageProperty

        [Test]
        public void Test_Descend_against_VisitorThrough_for_MultiLanguageProperty()
        {
            Aas.MultiLanguageProperty instance = (
                Aas.Tests.CommonJsonization.LoadMaximalMultiLanguageProperty());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_MultiLanguageProperty

        [Test]
        public void Test_Descend_of_Range()
        {
            Aas.Range instance = (
                Aas.Tests.CommonJsonization.LoadMaximalRange());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Range",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Range

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Range()
        {
            Aas.Range instance = (
                Aas.Tests.CommonJsonization.LoadMaximalRange());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Range

        [Test]
        public void Test_Descend_of_ReferenceElement()
        {
            Aas.ReferenceElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalReferenceElement());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "ReferenceElement",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_ReferenceElement

        [Test]
        public void Test_Descend_against_VisitorThrough_for_ReferenceElement()
        {
            Aas.ReferenceElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalReferenceElement());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_ReferenceElement

        [Test]
        public void Test_Descend_of_Blob()
        {
            Aas.Blob instance = (
                Aas.Tests.CommonJsonization.LoadMaximalBlob());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Blob",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Blob

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Blob()
        {
            Aas.Blob instance = (
                Aas.Tests.CommonJsonization.LoadMaximalBlob());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Blob

        [Test]
        public void Test_Descend_of_File()
        {
            Aas.File instance = (
                Aas.Tests.CommonJsonization.LoadMaximalFile());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "File",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_File

        [Test]
        public void Test_Descend_against_VisitorThrough_for_File()
        {
            Aas.File instance = (
                Aas.Tests.CommonJsonization.LoadMaximalFile());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_File

        [Test]
        public void Test_Descend_of_AnnotatedRelationshipElement()
        {
            Aas.AnnotatedRelationshipElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAnnotatedRelationshipElement());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "AnnotatedRelationshipElement",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_AnnotatedRelationshipElement

        [Test]
        public void Test_Descend_against_VisitorThrough_for_AnnotatedRelationshipElement()
        {
            Aas.AnnotatedRelationshipElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalAnnotatedRelationshipElement());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_AnnotatedRelationshipElement

        [Test]
        public void Test_Descend_of_Entity()
        {
            Aas.Entity instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEntity());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Entity",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Entity

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Entity()
        {
            Aas.Entity instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEntity());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Entity

        [Test]
        public void Test_Descend_of_EventPayload()
        {
            Aas.EventPayload instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEventPayload());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "EventPayload",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_EventPayload

        [Test]
        public void Test_Descend_against_VisitorThrough_for_EventPayload()
        {
            Aas.EventPayload instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEventPayload());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_EventPayload

        [Test]
        public void Test_Descend_of_BasicEventElement()
        {
            Aas.BasicEventElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalBasicEventElement());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "BasicEventElement",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_BasicEventElement

        [Test]
        public void Test_Descend_against_VisitorThrough_for_BasicEventElement()
        {
            Aas.BasicEventElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalBasicEventElement());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_BasicEventElement

        [Test]
        public void Test_Descend_of_Operation()
        {
            Aas.Operation instance = (
                Aas.Tests.CommonJsonization.LoadMaximalOperation());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Operation",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Operation

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Operation()
        {
            Aas.Operation instance = (
                Aas.Tests.CommonJsonization.LoadMaximalOperation());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Operation

        [Test]
        public void Test_Descend_of_OperationVariable()
        {
            Aas.OperationVariable instance = (
                Aas.Tests.CommonJsonization.LoadMaximalOperationVariable());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "OperationVariable",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_OperationVariable

        [Test]
        public void Test_Descend_against_VisitorThrough_for_OperationVariable()
        {
            Aas.OperationVariable instance = (
                Aas.Tests.CommonJsonization.LoadMaximalOperationVariable());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_OperationVariable

        [Test]
        public void Test_Descend_of_Capability()
        {
            Aas.Capability instance = (
                Aas.Tests.CommonJsonization.LoadMaximalCapability());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Capability",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Capability

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Capability()
        {
            Aas.Capability instance = (
                Aas.Tests.CommonJsonization.LoadMaximalCapability());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Capability

        [Test]
        public void Test_Descend_of_ConceptDescription()
        {
            Aas.ConceptDescription instance = (
                Aas.Tests.CommonJsonization.LoadMaximalConceptDescription());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "ConceptDescription",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_ConceptDescription

        [Test]
        public void Test_Descend_against_VisitorThrough_for_ConceptDescription()
        {
            Aas.ConceptDescription instance = (
                Aas.Tests.CommonJsonization.LoadMaximalConceptDescription());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_ConceptDescription

        [Test]
        public void Test_Descend_of_Reference()
        {
            Aas.Reference instance = (
                Aas.Tests.CommonJsonization.LoadMaximalReference());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Reference",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Reference

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Reference()
        {
            Aas.Reference instance = (
                Aas.Tests.CommonJsonization.LoadMaximalReference());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Reference

        [Test]
        public void Test_Descend_of_Key()
        {
            Aas.Key instance = (
                Aas.Tests.CommonJsonization.LoadMaximalKey());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Key",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Key

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Key()
        {
            Aas.Key instance = (
                Aas.Tests.CommonJsonization.LoadMaximalKey());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Key

        [Test]
        public void Test_Descend_of_LangStringNameType()
        {
            Aas.LangStringNameType instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringNameType());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "LangStringNameType",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_LangStringNameType

        [Test]
        public void Test_Descend_against_VisitorThrough_for_LangStringNameType()
        {
            Aas.LangStringNameType instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringNameType());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_LangStringNameType

        [Test]
        public void Test_Descend_of_LangStringTextType()
        {
            Aas.LangStringTextType instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringTextType());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "LangStringTextType",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_LangStringTextType

        [Test]
        public void Test_Descend_against_VisitorThrough_for_LangStringTextType()
        {
            Aas.LangStringTextType instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringTextType());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_LangStringTextType

        [Test]
        public void Test_Descend_of_Environment()
        {
            Aas.Environment instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEnvironment());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "Environment",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_Environment

        [Test]
        public void Test_Descend_against_VisitorThrough_for_Environment()
        {
            Aas.Environment instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEnvironment());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_Environment

        [Test]
        public void Test_Descend_of_EmbeddedDataSpecification()
        {
            Aas.EmbeddedDataSpecification instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEmbeddedDataSpecification());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "EmbeddedDataSpecification",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_EmbeddedDataSpecification

        [Test]
        public void Test_Descend_against_VisitorThrough_for_EmbeddedDataSpecification()
        {
            Aas.EmbeddedDataSpecification instance = (
                Aas.Tests.CommonJsonization.LoadMaximalEmbeddedDataSpecification());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_EmbeddedDataSpecification

        [Test]
        public void Test_Descend_of_LevelType()
        {
            Aas.LevelType instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLevelType());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "LevelType",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_LevelType

        [Test]
        public void Test_Descend_against_VisitorThrough_for_LevelType()
        {
            Aas.LevelType instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLevelType());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_LevelType

        [Test]
        public void Test_Descend_of_ValueReferencePair()
        {
            Aas.ValueReferencePair instance = (
                Aas.Tests.CommonJsonization.LoadMaximalValueReferencePair());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "ValueReferencePair",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_ValueReferencePair

        [Test]
        public void Test_Descend_against_VisitorThrough_for_ValueReferencePair()
        {
            Aas.ValueReferencePair instance = (
                Aas.Tests.CommonJsonization.LoadMaximalValueReferencePair());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_ValueReferencePair

        [Test]
        public void Test_Descend_of_ValueList()
        {
            Aas.ValueList instance = (
                Aas.Tests.CommonJsonization.LoadMaximalValueList());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "ValueList",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_ValueList

        [Test]
        public void Test_Descend_against_VisitorThrough_for_ValueList()
        {
            Aas.ValueList instance = (
                Aas.Tests.CommonJsonization.LoadMaximalValueList());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_ValueList

        [Test]
        public void Test_Descend_of_LangStringPreferredNameTypeIec61360()
        {
            Aas.LangStringPreferredNameTypeIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringPreferredNameTypeIec61360());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "LangStringPreferredNameTypeIec61360",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_LangStringPreferredNameTypeIec61360

        [Test]
        public void Test_Descend_against_VisitorThrough_for_LangStringPreferredNameTypeIec61360()
        {
            Aas.LangStringPreferredNameTypeIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringPreferredNameTypeIec61360());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_LangStringPreferredNameTypeIec61360

        [Test]
        public void Test_Descend_of_LangStringShortNameTypeIec61360()
        {
            Aas.LangStringShortNameTypeIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringShortNameTypeIec61360());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "LangStringShortNameTypeIec61360",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_LangStringShortNameTypeIec61360

        [Test]
        public void Test_Descend_against_VisitorThrough_for_LangStringShortNameTypeIec61360()
        {
            Aas.LangStringShortNameTypeIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringShortNameTypeIec61360());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_LangStringShortNameTypeIec61360

        [Test]
        public void Test_Descend_of_LangStringDefinitionTypeIec61360()
        {
            Aas.LangStringDefinitionTypeIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringDefinitionTypeIec61360());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "LangStringDefinitionTypeIec61360",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_LangStringDefinitionTypeIec61360

        [Test]
        public void Test_Descend_against_VisitorThrough_for_LangStringDefinitionTypeIec61360()
        {
            Aas.LangStringDefinitionTypeIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalLangStringDefinitionTypeIec61360());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_LangStringDefinitionTypeIec61360

        [Test]
        public void Test_Descend_of_DataSpecificationIec61360()
        {
            Aas.DataSpecificationIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalDataSpecificationIec61360());

            CompareOrRerecordTrace(
                instance,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "Descend",
                    "DataSpecificationIec61360",
                    "maximal.json.trace"));
        }  // public void Test_Descend_of_DataSpecificationIec61360

        [Test]
        public void Test_Descend_against_VisitorThrough_for_DataSpecificationIec61360()
        {
            Aas.DataSpecificationIec61360 instance = (
                Aas.Tests.CommonJsonization.LoadMaximalDataSpecificationIec61360());

            AssertDescendAndVisitorThroughSame(
                instance);
        }  // public void Test_Descend_against_VisitorThrough_for_DataSpecificationIec61360
    }  // class TestDescendAndVisitorThrough
}  // namespace AasCore.Aas3_0.Tests

/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */