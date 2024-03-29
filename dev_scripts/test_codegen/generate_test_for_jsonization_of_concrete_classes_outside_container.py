"""Generate the test code for the jsonization of classes outside a container."""

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

import test_codegen.common
from test_codegen import test_data_io


def main() -> int:
    """Execute the main routine."""
    symbol_table = test_codegen.common.load_symbol_table()

    this_path = pathlib.Path(os.path.realpath(__file__))
    repo_root = this_path.parent.parent.parent

    test_data_dir = repo_root / "test_data"

    # noinspection PyListCreation
    blocks = []  # type: List[str]

    environment_cls = symbol_table.must_find_concrete_class(
        aas_core_codegen.common.Identifier("Environment")
    )

    for our_type in symbol_table.our_types:
        if not isinstance(our_type, intermediate.ConcreteClass):
            continue

        container_cls = test_data_io.determine_container_class(
            cls=our_type, test_data_dir=test_data_dir, environment_cls=environment_cls
        )

        if container_cls is our_type:
            # NOTE (mristin, 2022-06-27):
            # These classes are tested already in TestJsonizationOfConcreteClasses.
            # We only need to test for class instances contained in a container.
            continue

        cls_name_csharp = aas_core_codegen.csharp.naming.class_name(our_type.name)

        blocks.append(
            Stripped(
                f"""\
[Test]
public void Test_round_trip_{cls_name_csharp}()
{{
    var instance = Aas.Tests.CommonJsonization.LoadMaximal{cls_name_csharp}();

    var jsonObject = Aas.Jsonization.Serialize.ToJsonObject(instance);
    
    var anotherInstance = Aas.Jsonization.Deserialize.{cls_name_csharp}From(
        jsonObject);
    
    var anotherJsonObject = Aas.Jsonization.Serialize.ToJsonObject(
        anotherInstance);

    Aas.Tests.CommonJson.CheckJsonNodesEqual(
        jsonObject,
        anotherJsonObject,
        out Aas.Reporting.Error? error);

    if (error != null)
    {{
        Assert.Fail(
            "When we de/serialize the complete instance " +
            "as {cls_name_csharp}, we get an error in the round trip: " +
            $"{{Reporting.GenerateJsonPath(error.PathSegments)}}: " +
            error.Cause
        );
    }}
}}  // public void Test_round_trip_{cls_name_csharp}"""
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

using NUnit.Framework; // can't alias

namespace AasCore.Aas3_0.Tests
{
    /// <summary>
    /// Test de/serialization of classes contained in a container <i>outside</i>
    /// of that container.
    /// </summary>
    /// <remarks>
    /// This is necessary so that we also test the methods that directly de/serialize
    /// an instance in rare use cases where it does not reside within a container such
    /// as <see cref="Aas.Environment" />.
    /// </remarks>
    public class TestJsonizationOfConcreteClassesOutsideContainer
    {
"""
    )

    for i, block in enumerate(blocks):
        if i > 0:
            writer.write("\n\n")

        writer.write(textwrap.indent(block, "        "))

    writer.write(
        """
    }  // class TestJsonizationOfConcreteClassesOutsideContainer
}  // namespace AasCore.Aas3_0.Tests

/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */
"""
    )

    this_path = pathlib.Path(os.path.realpath(__file__))
    repo_root = this_path.parent.parent.parent

    target_pth = (
        repo_root
        / "src/AasCore.Aas3_0.Tests"
        / "TestJsonizationOfConcreteClassesOutsideContainer.cs"
    )
    target_pth.write_text(writer.getvalue(), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
