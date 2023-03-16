/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */

using Aas = AasCore.Aas3_0;  // renamed
using Directory = System.IO.Directory;
using Nodes = System.Text.Json.Nodes;
using Path = System.IO.Path;

using NUnit.Framework;  // can't alias

namespace AasCore.Aas3_0.Tests
{
    public class TestXOrDefault
    {
        private static void CompareOrRerecordValue(
            object value,
            string expectedPath)
        {
            Nodes.JsonNode got = Aas.Tests.CommonJson.ToJson(
                value);

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

                System.IO.File.WriteAllText(
                    expectedPath, got.ToJsonString());
            }
            else
            {
                if (!System.IO.File.Exists(expectedPath))
                {
                    throw new System.IO.FileNotFoundException(
                        $"The file with the recorded value does not exist: {expectedPath}");
                }

                Nodes.JsonNode expected = Aas.Tests.CommonJson.ReadFromFile(
                    expectedPath);

                Aas.Tests.CommonJson.CheckJsonNodesEqual(
                    expected, got, out Aas.Reporting.Error? error);

                if (error != null)
                {
                    Assert.Fail(
                        $"The original value from {expectedPath} is unequal the obtain value " +
                        "when serialized to JSON: " +
                        $"{Reporting.GenerateJsonPath(error.PathSegments)}: " +
                        error.Cause
                    );
                }
            }
        }

        [Test]
        public void Test_Extension_ValueTypeOrDefault_non_default()
        {
            Aas.Extension instance = (
                Aas.Tests.CommonJsonization.LoadMaximalExtension());

            string value = Aas.Stringification.ToString(
                instance.ValueTypeOrDefault())
                    ?? throw new System.InvalidOperationException(
                        "Failed to stringify the enum");

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Extension",
                    "ValueTypeOrDefault.non-default.json"));
        }  // public void Test_Extension_ValueTypeOrDefault_non_default

        [Test]
        public void Test_Extension_ValueTypeOrDefault_default()
        {
            Aas.Extension instance = (
                Aas.Tests.CommonJsonization.LoadMinimalExtension());

            string value = Aas.Stringification.ToString(
                instance.ValueTypeOrDefault())
                    ?? throw new System.InvalidOperationException(
                        "Failed to stringify the enum");

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Extension",
                    "ValueTypeOrDefault.default.json"));
        }  // public void Test_Extension_ValueTypeOrDefault_default

        [Test]
        public void Test_Qualifier_KindOrDefault_non_default()
        {
            Aas.Qualifier instance = (
                Aas.Tests.CommonJsonization.LoadMaximalQualifier());

            string value = Aas.Stringification.ToString(
                instance.KindOrDefault())
                    ?? throw new System.InvalidOperationException(
                        "Failed to stringify the enum");

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Qualifier",
                    "KindOrDefault.non-default.json"));
        }  // public void Test_Qualifier_KindOrDefault_non_default

        [Test]
        public void Test_Qualifier_KindOrDefault_default()
        {
            Aas.Qualifier instance = (
                Aas.Tests.CommonJsonization.LoadMinimalQualifier());

            string value = Aas.Stringification.ToString(
                instance.KindOrDefault())
                    ?? throw new System.InvalidOperationException(
                        "Failed to stringify the enum");

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Qualifier",
                    "KindOrDefault.default.json"));
        }  // public void Test_Qualifier_KindOrDefault_default

        [Test]
        public void Test_Submodel_KindOrDefault_non_default()
        {
            Aas.Submodel instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodel());

            string value = Aas.Stringification.ToString(
                instance.KindOrDefault())
                    ?? throw new System.InvalidOperationException(
                        "Failed to stringify the enum");

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Submodel",
                    "KindOrDefault.non-default.json"));
        }  // public void Test_Submodel_KindOrDefault_non_default

        [Test]
        public void Test_Submodel_KindOrDefault_default()
        {
            Aas.Submodel instance = (
                Aas.Tests.CommonJsonization.LoadMinimalSubmodel());

            string value = Aas.Stringification.ToString(
                instance.KindOrDefault())
                    ?? throw new System.InvalidOperationException(
                        "Failed to stringify the enum");

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Submodel",
                    "KindOrDefault.default.json"));
        }  // public void Test_Submodel_KindOrDefault_default

        [Test]
        public void Test_SubmodelElementList_OrderRelevantOrDefault_non_default()
        {
            Aas.SubmodelElementList instance = (
                Aas.Tests.CommonJsonization.LoadMaximalSubmodelElementList());

            var value = instance.OrderRelevantOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "SubmodelElementList",
                    "OrderRelevantOrDefault.non-default.json"));
        }  // public void Test_SubmodelElementList_OrderRelevantOrDefault_non_default

        [Test]
        public void Test_SubmodelElementList_OrderRelevantOrDefault_default()
        {
            Aas.SubmodelElementList instance = (
                Aas.Tests.CommonJsonization.LoadMinimalSubmodelElementList());

            var value = instance.OrderRelevantOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "SubmodelElementList",
                    "OrderRelevantOrDefault.default.json"));
        }  // public void Test_SubmodelElementList_OrderRelevantOrDefault_default

        [Test]
        public void Test_Property_CategoryOrDefault_non_default()
        {
            Aas.Property instance = (
                Aas.Tests.CommonJsonization.LoadMaximalProperty());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Property",
                    "CategoryOrDefault.non-default.json"));
        }  // public void Test_Property_CategoryOrDefault_non_default

        [Test]
        public void Test_Property_CategoryOrDefault_default()
        {
            Aas.Property instance = (
                Aas.Tests.CommonJsonization.LoadMinimalProperty());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Property",
                    "CategoryOrDefault.default.json"));
        }  // public void Test_Property_CategoryOrDefault_default

        [Test]
        public void Test_MultiLanguageProperty_CategoryOrDefault_non_default()
        {
            Aas.MultiLanguageProperty instance = (
                Aas.Tests.CommonJsonization.LoadMaximalMultiLanguageProperty());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "MultiLanguageProperty",
                    "CategoryOrDefault.non-default.json"));
        }  // public void Test_MultiLanguageProperty_CategoryOrDefault_non_default

        [Test]
        public void Test_MultiLanguageProperty_CategoryOrDefault_default()
        {
            Aas.MultiLanguageProperty instance = (
                Aas.Tests.CommonJsonization.LoadMinimalMultiLanguageProperty());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "MultiLanguageProperty",
                    "CategoryOrDefault.default.json"));
        }  // public void Test_MultiLanguageProperty_CategoryOrDefault_default

        [Test]
        public void Test_Range_CategoryOrDefault_non_default()
        {
            Aas.Range instance = (
                Aas.Tests.CommonJsonization.LoadMaximalRange());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Range",
                    "CategoryOrDefault.non-default.json"));
        }  // public void Test_Range_CategoryOrDefault_non_default

        [Test]
        public void Test_Range_CategoryOrDefault_default()
        {
            Aas.Range instance = (
                Aas.Tests.CommonJsonization.LoadMinimalRange());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Range",
                    "CategoryOrDefault.default.json"));
        }  // public void Test_Range_CategoryOrDefault_default

        [Test]
        public void Test_ReferenceElement_CategoryOrDefault_non_default()
        {
            Aas.ReferenceElement instance = (
                Aas.Tests.CommonJsonization.LoadMaximalReferenceElement());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "ReferenceElement",
                    "CategoryOrDefault.non-default.json"));
        }  // public void Test_ReferenceElement_CategoryOrDefault_non_default

        [Test]
        public void Test_ReferenceElement_CategoryOrDefault_default()
        {
            Aas.ReferenceElement instance = (
                Aas.Tests.CommonJsonization.LoadMinimalReferenceElement());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "ReferenceElement",
                    "CategoryOrDefault.default.json"));
        }  // public void Test_ReferenceElement_CategoryOrDefault_default

        [Test]
        public void Test_Blob_CategoryOrDefault_non_default()
        {
            Aas.Blob instance = (
                Aas.Tests.CommonJsonization.LoadMaximalBlob());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Blob",
                    "CategoryOrDefault.non-default.json"));
        }  // public void Test_Blob_CategoryOrDefault_non_default

        [Test]
        public void Test_Blob_CategoryOrDefault_default()
        {
            Aas.Blob instance = (
                Aas.Tests.CommonJsonization.LoadMinimalBlob());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "Blob",
                    "CategoryOrDefault.default.json"));
        }  // public void Test_Blob_CategoryOrDefault_default

        [Test]
        public void Test_File_CategoryOrDefault_non_default()
        {
            Aas.File instance = (
                Aas.Tests.CommonJsonization.LoadMaximalFile());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "File",
                    "CategoryOrDefault.non-default.json"));
        }  // public void Test_File_CategoryOrDefault_non_default

        [Test]
        public void Test_File_CategoryOrDefault_default()
        {
            Aas.File instance = (
                Aas.Tests.CommonJsonization.LoadMinimalFile());

            var value = instance.CategoryOrDefault();

            CompareOrRerecordValue(
                value,
                Path.Combine(
                    Aas.Tests.Common.TestDataDir,
                    "XOrDefault",
                    "File",
                    "CategoryOrDefault.default.json"));
        }  // public void Test_File_CategoryOrDefault_default
    }  // class TestXOrDefault
}  // namespace AasCore.Aas3_0.Tests

/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */
