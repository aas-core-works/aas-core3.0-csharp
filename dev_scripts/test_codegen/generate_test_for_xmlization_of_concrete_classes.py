"""Generate the test code for the de/serialization of instances in XML."""

import io
import os
import pathlib
import sys
import textwrap
from typing import List

import aas_core_codegen
import aas_core_codegen.common
import aas_core_codegen.csharp.naming
import aas_core_codegen.naming
import aas_core_codegen.parse
import aas_core_codegen.run
from aas_core_codegen import intermediate
from aas_core_codegen.common import Stripped
from aas_core_codegen.csharp import common as csharp_common
from icontract import require

import test_codegen.common
from test_codegen import test_data_io


def _generate_for_self_contained(
    cls_name_csharp: str,
    cls_name_xml: str,
) -> List[Stripped]:
    """Generate the tests for a self-contained class."""
    # noinspection PyListCreation
    blocks = []  # type: List[Stripped]

    blocks.append(
        Stripped(
            f"""\
[Test]
public void Test_{cls_name_csharp}_ok()
{{
    var paths = Directory.GetFiles(
        Path.Combine(
            Aas.Tests.Common.TestDataDir,
            "Xml",
            "SelfContained",
            "Expected",
            {csharp_common.string_literal(cls_name_xml)}
        ),
        "*.xml",
        System.IO.SearchOption.AllDirectories).ToList();
    paths.Sort();

    foreach (var path in paths)
    {{
        using var xmlReader = System.Xml.XmlReader.Create(path);

        var instance = Aas.Xmlization.Deserialize.{cls_name_csharp}From(
            xmlReader);

        var errors = Aas.Verification.Verify(instance).ToList();
        Aas.Tests.Common.AssertNoVerificationErrors(errors, path);

        AssertSerializeDeserializeEqualsOriginal(
            instance, path);
    }}
}}  // public void Test_{cls_name_csharp}_ok"""
        )
    )

    blocks.append(
        Stripped(
            f"""\
[Test]
public void Test_{cls_name_csharp}_deserialization_fail()
{{
    foreach (
        string causeDir in
        Directory.GetDirectories(
            Path.Combine(
                Aas.Tests.Common.TestDataDir,
                "Xml",
                "SelfContained",
                "Unexpected",
                "Unserializable"
            )
        )
    ) {{
        string clsDir = Path.Combine(
            causeDir,
            {csharp_common.string_literal(cls_name_xml)}
        );

        if (!Directory.Exists(clsDir))
        {{
            // No examples of {cls_name_csharp} for the failure cause.
            continue;
        }}

        var paths = Directory.GetFiles(
            clsDir,
            "*.xml",
            System.IO.SearchOption.AllDirectories).ToList();
        paths.Sort();

        foreach (var path in paths)
        {{
            using var xmlReader = System.Xml.XmlReader.Create(path);

            Aas.Xmlization.Exception? exception = null;

            try
            {{
                _ = Aas.Xmlization.Deserialize.{cls_name_csharp}From(
                    xmlReader);
            }}
            catch (Aas.Xmlization.Exception observedException)
            {{
                exception = observedException;
            }}

            AssertEqualsExpectedOrRerecordDeserializationException(
                exception, path);
        }}
    }}
}}  // public void Test_{cls_name_csharp}_deserialization_fail"""
        )
    )

    blocks.append(
        Stripped(
            f"""\
[Test]
public void Test_{cls_name_csharp}_verification_fail()
{{
    foreach (
        string causeDir in
        Directory.GetDirectories(
            Path.Combine(
                Aas.Tests.Common.TestDataDir,
                "Xml",
                "SelfContained",
                "Unexpected",
                "Invalid"
            )
        )
    ) {{
        string clsDir = Path.Combine(
            causeDir,
            {csharp_common.string_literal(cls_name_xml)}
        );

        if (!Directory.Exists(clsDir))
        {{
            // No examples of {cls_name_csharp} for the failure cause.
            continue;
        }}

        var paths = Directory.GetFiles(
            clsDir,
            "*.xml",
            System.IO.SearchOption.AllDirectories).ToList();
        paths.Sort();

        foreach (var path in paths)
        {{
            using var xmlReader = System.Xml.XmlReader.Create(path);

            var instance = Aas.Xmlization.Deserialize.{cls_name_csharp}From(
                xmlReader);

            var errors = Aas.Verification.Verify(instance).ToList();
            Aas.Tests.Common.AssertEqualsExpectedOrRerecordVerificationErrors(
                errors, path);
        }}
    }}
}}  // public void Test_{cls_name_csharp}_verification_fail"""
        )
    )

    return blocks


@require(lambda container_cls_csharp: container_cls_csharp == "Environment")
def _generate_for_contained_in_environment(
    cls_name_csharp: str,
    cls_name_xml: str,
    container_cls_csharp: str,
) -> List[Stripped]:
    """Generate the tests for a class contained in an ``Environment`` instance."""
    # noinspection PyListCreation
    blocks = []  # type: List[Stripped]

    blocks.append(
        Stripped(
            f"""\
[Test]
public void Test_{cls_name_csharp}_ok()
{{
    var paths = Directory.GetFiles(
        Path.Combine(
            Aas.Tests.Common.TestDataDir,
            "Xml",
            "ContainedInEnvironment",
            "Expected",
            {csharp_common.string_literal(cls_name_xml)}
        ),
        "*.xml",
        System.IO.SearchOption.AllDirectories).ToList();
    paths.Sort();

    foreach (var path in paths)
    {{
        using var xmlReader = System.Xml.XmlReader.Create(path);

        var container = Aas.Xmlization.Deserialize.{container_cls_csharp}From(
            xmlReader);

        var errors = Aas.Verification.Verify(container).ToList();
        Aas.Tests.Common.AssertNoVerificationErrors(errors, path);

        AssertSerializeDeserializeEqualsOriginal(
            container, path);
    }}
}}  // public void Test_{cls_name_csharp}_ok"""
        )
    )

    blocks.append(
        Stripped(
            f"""\
[Test]
public void Test_{cls_name_csharp}_deserialization_fail()
{{
    foreach (
        string causeDir in
        Directory.GetDirectories(
            Path.Combine(
                Aas.Tests.Common.TestDataDir,
                "Xml",
                "ContainedInEnvironment",
                "Unexpected",
                "Unserializable"
            )
        )
    ) {{
        string clsDir = Path.Combine(
            causeDir,
            {csharp_common.string_literal(cls_name_xml)}
        );

        if (!Directory.Exists(clsDir))
        {{
            // No examples of {cls_name_csharp} for the failure cause.
            continue;
        }}

        var paths = Directory.GetFiles(
            clsDir,
            "*.xml",
            System.IO.SearchOption.AllDirectories).ToList();
        paths.Sort();

        foreach (var path in paths)
        {{
            using var xmlReader = System.Xml.XmlReader.Create(path);

            Aas.Xmlization.Exception? exception = null;

            try
            {{
                _ = Aas.Xmlization.Deserialize.{container_cls_csharp}From(
                    xmlReader);
            }}
            catch (Aas.Xmlization.Exception observedException)
            {{
                exception = observedException;
            }}

            AssertEqualsExpectedOrRerecordDeserializationException(
                exception, path);
        }}
    }}
}}  // public void Test_{cls_name_csharp}_deserialization_fail"""
        )
    )

    blocks.append(
        Stripped(
            f"""\
[Test]
public void Test_{cls_name_csharp}_verification_fail()
{{
    foreach (
        string causeDir in
        Directory.GetDirectories(
            Path.Combine(
                Aas.Tests.Common.TestDataDir,
                "Xml",
                "ContainedInEnvironment",
                "Unexpected",
                "Invalid"
            )
        )
    ) {{
        string clsDir = Path.Combine(
            causeDir,
            {csharp_common.string_literal(cls_name_xml)}
        );

        if (!Directory.Exists(clsDir))
        {{
            // No examples of {cls_name_csharp} for the failure cause.
            continue;
        }}

        var paths = Directory.GetFiles(
            clsDir,
            "*.xml",
            System.IO.SearchOption.AllDirectories).ToList();
        paths.Sort();

        foreach (var path in paths)
        {{
            using var xmlReader = System.Xml.XmlReader.Create(path);

            var container = Aas.Xmlization.Deserialize.{container_cls_csharp}From(
                xmlReader);

            var errors = Aas.Verification.Verify(container).ToList();
            Aas.Tests.Common.AssertEqualsExpectedOrRerecordVerificationErrors(
                errors, path);
        }}
    }}
}}  // public void Test_{cls_name_csharp}_verification_fail"""
        )
    )

    return blocks


def main() -> int:
    """Execute the main routine."""
    symbol_table = test_codegen.common.load_symbol_table()

    this_path = pathlib.Path(os.path.realpath(__file__))
    repo_root = this_path.parent.parent.parent

    test_data_dir = repo_root / "test_data"

    # noinspection PyListCreation
    blocks = []  # type: List[str]

    xml_namespace_literal = csharp_common.string_literal(
        symbol_table.meta_model.xml_namespace
    )

    blocks.append(
        Stripped(
            f"""\
private static void CheckElementsEqual(
    XElement expected,
    XElement got,
    out Reporting.Error? error)
{{
    error = null;

    if (expected.Name.LocalName != got.Name.LocalName)
    {{
        error = new Reporting.Error(
            "Mismatch in element names: " +
            $"{{expected}} != {{got}}"
        );
        return;
    }}

    string? expectedContent = (expected.FirstNode as XText)?.Value;
    string? gotContent = (got.FirstNode as XText)?.Value;

    if (expectedContent != gotContent)
    {{
        error = new Reporting.Error(
            $"Mismatch in element contents: {{expected}} != {{got}}"
        );
        return;
    }}

    var expectedChildren = expected.Elements().ToList();
    var gotChildren = got.Elements().ToList();

    if (expectedChildren.Count != gotChildren.Count)
    {{
        error = new Reporting.Error(
            $"Mismatch in child elements: {{expected}} != {{got}}"
        );
        return;
    }}

    for (int i = 0; i < expectedChildren.Count; i++)
    {{
        CheckElementsEqual(
            expectedChildren[i],
            gotChildren[i],
            out error);

        if (error != null)
        {{
            error.PrependSegment(
                new Reporting.IndexSegment(i));

            error.PrependSegment(
                new Reporting.NameSegment(
                    expected.Name.ToString()));
        }}
    }}
}}

private static void AssertSerializeDeserializeEqualsOriginal(
    Aas.IClass instance, string path)
{{
    // Serialize
    var outputBuilder = new System.Text.StringBuilder();

    {{
        using var writer = System.Xml.XmlWriter.Create(
            outputBuilder,
            new System.Xml.XmlWriterSettings()
            {{
                Encoding = System.Text.Encoding.UTF8,
                OmitXmlDeclaration = true
            }}
        );
        Aas.Xmlization.Serialize.To(
            instance,
            writer);
    }}

    string outputText = outputBuilder.ToString();

    // Compare input == output
    {{
        using var outputReader = new System.IO.StringReader(outputText);
        var gotDoc = XDocument.Load(outputReader);

        Assert.AreEqual(
            gotDoc.Root?.Name.Namespace.ToString(),
            {xml_namespace_literal});

        foreach (var child in gotDoc.Descendants())
        {{
            Assert.AreEqual(
                child.GetDefaultNamespace().NamespaceName,
                {xml_namespace_literal});
        }}

        var expectedDoc = XDocument.Load(path);

        CheckElementsEqual(
            expectedDoc.Root!,
            gotDoc.Root!,
            out Reporting.Error? inequalityError);

        if (inequalityError != null)
        {{
            Assert.Fail(
                $"The original XML from {{path}} is unequal the serialized XML: " +
                $"#/{{Reporting.GenerateRelativeXPath(inequalityError.PathSegments)}}: " +
                inequalityError.Cause
            );
        }}
    }}
}}

private static void AssertEqualsExpectedOrRerecordDeserializationException(
    Aas.Xmlization.Exception? exception,
    string path)
{{
    if (exception == null)
    {{
        Assert.Fail(
            $"Expected a Xmlization exception when de-serializing {{path}}, but got none."
        );
    }}
    else
    {{
        string exceptionPath = path + ".exception";
        string got = exception.Message;
        if (Aas.Tests.Common.RecordMode)
        {{
            System.IO.File.WriteAllText(exceptionPath, got);
        }}
        else
        {{
            if (!System.IO.File.Exists(exceptionPath))
            {{
                throw new System.IO.FileNotFoundException(
                    "The file with the recorded exception does not " +
                    $"exist: {{exceptionPath}}; maybe you want to set the environment " +
                    $"variable {{Aas.Tests.Common.RecordModeEnvironmentVariableName}}?");
            }}

            string expected = System.IO.File.ReadAllText(exceptionPath);
            Assert.AreEqual(
                expected.Replace("\\r\\n", "\\n"),
                got.Replace("\\r\\n", "\\n"),
                $"The expected exception does not match the actual one for the file {{path}}");
        }}
    }}
}}"""
        )
    )

    environment_cls = symbol_table.must_find_concrete_class(
        aas_core_codegen.common.Identifier("Environment")
    )

    for our_type in symbol_table.our_types:
        if not isinstance(our_type, intermediate.ConcreteClass):
            continue

        container_cls = test_data_io.determine_container_class(
            cls=our_type, test_data_dir=test_data_dir, environment_cls=environment_cls
        )
        container_cls_csharp = aas_core_codegen.csharp.naming.class_name(
            container_cls.name
        )

        cls_name_csharp = aas_core_codegen.csharp.naming.class_name(our_type.name)
        cls_name_xml = aas_core_codegen.naming.xml_class_name(our_type.name)

        if container_cls is our_type:
            blocks.extend(
                _generate_for_self_contained(
                    cls_name_csharp=cls_name_csharp, cls_name_xml=cls_name_xml
                )
            )
        else:
            blocks.extend(
                _generate_for_contained_in_environment(
                    cls_name_csharp=cls_name_csharp,
                    cls_name_xml=cls_name_xml,
                    container_cls_csharp=container_cls_csharp,
                )
            )

    writer = io.StringIO()
    writer.write(
        """\
/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */

using Aas = AasCore.Aas3_0;  // renamed
using Directory = System.IO.Directory;
using Path = System.IO.Path;

using NUnit.Framework; // can't alias
using System.Linq;  // can't alias
using System.Xml.Linq; // can't alias

namespace AasCore.Aas3_0.Tests
{
    public class TestXmlizationOfConcreteClasses
    {
"""
    )

    for i, block in enumerate(blocks):
        if i > 0:
            writer.write("\n\n")

        writer.write(textwrap.indent(block, "        "))

    writer.write(
        """
    }  // class TestXmlizationOfConcreteClasses
}  // namespace AasCore.Aas3_0.Tests

/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */
"""
    )

    target_pth = (
        repo_root / "src/AasCore.Aas3_0.Tests/TestXmlizationOfConcreteClasses.cs"
    )
    target_pth.write_text(writer.getvalue(), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
