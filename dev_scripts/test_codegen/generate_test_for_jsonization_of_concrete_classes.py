"""Generate the test code for the JSON de/serialization of classes."""

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
    cls_name_json: str,
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
            "Json", 
            "SelfContained", 
            "Expected",
            {csharp_common.string_literal(cls_name_json)}
        ),
        "*.json",
        System.IO.SearchOption.AllDirectories).ToList();
    paths.Sort();

    foreach (var path in paths)
    {{
        var node = Aas.Tests.CommonJson.ReadFromFile(path);

        var instance = Aas.Jsonization.Deserialize.{cls_name_csharp}From(
            node);

        var errors = Aas.Verification.Verify(instance).ToList();
        Aas.Tests.Common.AssertNoVerificationErrors(errors, path);

        AssertSerializeDeserializeEqualsOriginal(
            node, instance, path);
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
    foreach (string cause in CausesForDeserializationFailure)
    {{
        string baseDir = Path.Combine(
            Aas.Tests.Common.TestDataDir,
            "Json", 
            "SelfContained", 
            "Unexpected", 
            cause,
            {csharp_common.string_literal(cls_name_json)}
        );
         
        if (!Directory.Exists(baseDir))
        {{
            // No examples of {cls_name_csharp} for the failure cause.
            continue;
        }} 
        
        var paths = Directory.GetFiles(
            baseDir,
            "*.json",
            System.IO.SearchOption.AllDirectories).ToList();
        paths.Sort();

        foreach (var path in paths)
        {{
            var node = Aas.Tests.CommonJson.ReadFromFile(path);

            Aas.Jsonization.Exception? exception = null;
            try
            {{
                var _ = Aas.Jsonization.Deserialize.{cls_name_csharp}From(
                    node);
            }}
            catch (Aas.Jsonization.Exception observedException)
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
    foreach (string cause in Aas.Tests.Common.CausesForVerificationFailure)
    {{
        string baseDir = Path.Combine(
            Aas.Tests.Common.TestDataDir,
            "Json", 
            "SelfContained", 
            "Unexpected", 
            cause,
            {csharp_common.string_literal(cls_name_json)}
        );
         
        if (!Directory.Exists(baseDir))
        {{
            // No examples of {cls_name_csharp} for the failure cause.
            continue;
        }}
        
        var paths = Directory.GetFiles(
            baseDir,
            "*.json",
            System.IO.SearchOption.AllDirectories).ToList();
        paths.Sort();

        foreach (var path in paths)
        {{
            var node = Aas.Tests.CommonJson.ReadFromFile(path);

            var instance = Aas.Jsonization.Deserialize.{cls_name_csharp}From(
                node);
 
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
    cls_name_json: str,
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
            "Json", 
            "ContainedInEnvironment", 
            "Expected",
            {csharp_common.string_literal(cls_name_json)}
        ),
        "*.json",
        System.IO.SearchOption.AllDirectories).ToList();
    paths.Sort();

    foreach (var path in paths)
    {{
        var node = Aas.Tests.CommonJson.ReadFromFile(path);

        var container = Aas.Jsonization.Deserialize.{container_cls_csharp}From(
            node);

        var errors = Aas.Verification.Verify(container).ToList();
        Aas.Tests.Common.AssertNoVerificationErrors(errors, path);

        AssertSerializeDeserializeEqualsOriginal(
            node, container, path);
    }}
}}  // public void Test_{cls_name_csharp}_ok"""
        )
    )

    blocks.append(
        Stripped(
            f"""\
[Test]
public void Test_{cls_name_csharp}_deserialization_from_non_object_fail()
{{
    var node = Nodes.JsonValue.Create("INVALID") 
        ?? throw new System.InvalidOperationException(
            "Unexpected failure of the node creation");

    Aas.Jsonization.Exception? exception = null;
    try
    {{
        var _ = Aas.Jsonization.Deserialize.{cls_name_csharp}From(
            node);
    }}
    catch (Aas.Jsonization.Exception observedException)
    {{
        exception = observedException;
    }}

    if (exception == null)
    {{
        throw new AssertionException("Expected an exception, but got none");
    }}

    if (!exception.Message.StartsWith("Expected a JsonObject, but got "))
    {{
        throw new AssertionException(
            $"Unexpected exception message: {{exception.Message}}");
    }}
}}  // public void Test_{cls_name_csharp}_deserialization_from_non_object_fail"""
        )
    )

    blocks.append(
        Stripped(
            f"""\
[Test]
public void Test_{cls_name_csharp}_deserialization_fail()
{{
    foreach (string cause in CausesForDeserializationFailure)
    {{
        string baseDir = Path.Combine(
            Aas.Tests.Common.TestDataDir,
            "Json", 
            "ContainedInEnvironment", 
            "Unexpected", 
            cause,
            {csharp_common.string_literal(cls_name_json)});
            
        if (!Directory.Exists(baseDir))
        {{
            // No examples of {cls_name_csharp} for the failure cause.
            continue;
        }}
    
        var paths = Directory.GetFiles(
            baseDir,
            "*.json",
            System.IO.SearchOption.AllDirectories).ToList();
        paths.Sort();

        foreach (var path in paths)
        {{
            var node = Aas.Tests.CommonJson.ReadFromFile(path);

            Aas.Jsonization.Exception? exception = null;
            try
            {{
                var _ = Aas.Jsonization.Deserialize.{container_cls_csharp}From(
                    node);
            }}
            catch (Aas.Jsonization.Exception observedException)
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
    foreach (string cause in Aas.Tests.Common.CausesForVerificationFailure)
    {{
        string baseDir = Path.Combine(
            Aas.Tests.Common.TestDataDir,
            "Json", 
            "ContainedInEnvironment", 
            "Unexpected", 
            cause,
            {csharp_common.string_literal(cls_name_json)}
        );
    
        if (!Directory.Exists(baseDir))
        {{
            // No examples of {cls_name_csharp} for the failure cause.
            continue;
        }}
    
        var paths = Directory.GetFiles(
            baseDir,
            "*.json",
            System.IO.SearchOption.AllDirectories).ToList();
        paths.Sort();

        foreach (var path in paths)
        {{
            var node = Aas.Tests.CommonJson.ReadFromFile(path);

            var container = Aas.Jsonization.Deserialize.{container_cls_csharp}From(
                node);

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

    blocks.append(
        Stripped(
            """\
private static void AssertSerializeDeserializeEqualsOriginal(
    Nodes.JsonNode originalNode, Aas.IClass instance, string path)
{
    Nodes.JsonObject? serialized = null;
    try
    {
        serialized = Aas.Jsonization.Serialize.ToJsonObject(instance);
    }
    catch (System.Exception exception)
    {
        Assert.Fail(
            "Expected no exception upon serialization of an instance " +
            $"de-serialized from {path}, but got: {exception}"
        );
    }

    if (serialized == null)
    {
        Assert.Fail(
            $"Unexpected null serialization of an instance from {path}"
        );
    }
    else
    {
        Aas.Tests.CommonJson.CheckJsonNodesEqual(
            originalNode,
            serialized,
            out Reporting.Error? inequalityError);
        if (inequalityError != null)
        {
            Assert.Fail(
                $"The original JSON from {path} is unequal the serialized JSON: " +
                $"{Reporting.GenerateJsonPath(inequalityError.PathSegments)}: " +
                inequalityError.Cause
            );
        }
    }
}

private static readonly List<string> CausesForDeserializationFailure = (
    new List<string>()
    {
        "TypeViolation",
        "RequiredViolation",
        "EnumViolation",
        "NullViolation",
        "UnexpectedAdditionalProperty"
    });

private static void AssertEqualsExpectedOrRerecordDeserializationException(
    Aas.Jsonization.Exception? exception,
    string path)
{
    if (exception == null)
    {
        Assert.Fail(
            $"Expected a Jsonization exception when de-serializing {path}, but got none."
        );
    }
    else
    {
        string exceptionPath = path + ".exception";
        string got = exception.Message;
        if (Aas.Tests.Common.RecordMode)
        {
            System.IO.File.WriteAllText(exceptionPath, got);
        }
        else
        {
            if (!System.IO.File.Exists(exceptionPath))
            {
                throw new System.IO.FileNotFoundException(
                    $"The file with the recorded exception does not exist: {exceptionPath}");
            }

            string expected = System.IO.File.ReadAllText(exceptionPath);
            Assert.AreEqual(
                expected.Replace("\\r\\n", "\\n"),
                got.Replace("\\r\\n", "\\n"),
                $"The expected exception does not match the actual one for the file {path}");
        }
    }
}"""
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
        cls_name_json = aas_core_codegen.naming.json_model_type(our_type.name)

        if container_cls is our_type:
            blocks.extend(
                _generate_for_self_contained(
                    cls_name_csharp=cls_name_csharp, cls_name_json=cls_name_json
                )
            )
        else:
            blocks.extend(
                _generate_for_contained_in_environment(
                    cls_name_csharp=cls_name_csharp,
                    cls_name_json=cls_name_json,
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
using Nodes = System.Text.Json.Nodes;
using Path = System.IO.Path;

using System.Collections.Generic;  // can't alias
using System.Linq;  // can't alias
using NUnit.Framework; // can't alias

namespace AasCore.Aas3_0.Tests
{
    public class TestJsonizationOfConcreteClasses
    {
"""
    )

    for i, block in enumerate(blocks):
        if i > 0:
            writer.write("\n\n")

        writer.write(textwrap.indent(block, "        "))

    writer.write(
        """
    }  // class TestJsonizationOfConcreteClasses
}  // namespace AasCore.Aas3_0.Tests

/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */
"""
    )

    target_pth = (
        repo_root / "src/AasCore.Aas3_0.Tests/TestJsonizationOfConcreteClasses.cs"
    )
    target_pth.write_text(writer.getvalue(), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
