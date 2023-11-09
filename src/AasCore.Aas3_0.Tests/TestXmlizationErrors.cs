using Aas = AasCore.Aas3_0; // renamed

using NUnit.Framework; // can't alias

namespace AasCore.Aas3_0.Tests
{
    public class TestXmlizationErrors
    {
        [Test]
        public void Test_error_on_unexpected_declaration()
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

            // We intentionally do not call `MoveToContent` to test the error message.
            // This is a very common situation, see:
            // https://github.com/aas-core-works/aas-core3.0-csharp/issues/24

            string? message = null;

            try
            {
                Aas.Xmlization.Deserialize.EnvironmentFrom(
                    xmlReader);
            }
            catch (AasCore.Aas3_0.Xmlization.Exception exception)
            {
                message = exception.Message;
            }

            if (message == null)
            {
                throw new AssertionException("Unexpected no exception");
            }
            Assert.AreEqual(
                "Unexpected XML declaration when reading an instance of " +
                "class Environment, as we expect the reader to be set at content " +
                "with MoveToContent at: the beginning",
                message);
        }
    }
}