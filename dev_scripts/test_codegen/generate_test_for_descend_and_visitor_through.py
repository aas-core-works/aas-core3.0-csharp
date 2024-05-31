"""Generate the test code for the ``Descend`` methods and ``VisitorThrough``."""

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

import test_codegen.common


def main() -> int:
    """Execute the main routine."""
    symbol_table = test_codegen.common.load_symbol_table()

    this_path = pathlib.Path(os.path.realpath(__file__))
    repo_root = this_path.parent.parent.parent

    # noinspection PyListCreation
    blocks = []  # type: List[str]

    blocks.append(
        Stripped(
            """\
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
                "The file with the recorded trace does not " +
                $"exist: {expectedPath}; maybe you want to set the environment " +
                $"variable {Aas.Tests.Common.RecordModeEnvironmentVariableName}?");
        }

        string expected = System.IO.File.ReadAllText(expectedPath);
        Assert.AreEqual(
            expected.Replace("\\r\\n", "\\n"),
            got.Replace("\\r\\n", "\\n"),
            $"The expected trace from {expectedPath} does not match the actual one");
    }
}"""
        )
    )

    for our_type in symbol_table.our_types:
        if not isinstance(our_type, intermediate.ConcreteClass):
            continue

        cls_name_csharp = aas_core_codegen.csharp.naming.class_name(our_type.name)
        cls_name_json = aas_core_codegen.naming.json_model_type(our_type.name)

        blocks.append(
            Stripped(
                f"""\
[Test]
public void Test_Descend_of_{cls_name_csharp}()
{{
    Aas.{cls_name_csharp} instance = (
        Aas.Tests.CommonJsonization.LoadMaximal{cls_name_csharp}());

    CompareOrRerecordTrace(
        instance,
        Path.Combine(
            Aas.Tests.Common.TestDataDir,
            "Descend",
            {csharp_common.string_literal(cls_name_json)},
            "maximal.json.trace"));
}}  // public void Test_Descend_of_{cls_name_csharp}

[Test]
public void Test_Descend_against_VisitorThrough_for_{cls_name_csharp}()
{{
    Aas.{cls_name_csharp} instance = (
        Aas.Tests.CommonJsonization.LoadMaximal{cls_name_csharp}());
    
    AssertDescendAndVisitorThroughSame(
        instance);
}}  // public void Test_Descend_against_VisitorThrough_for_{cls_name_csharp}"""
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
using System.Collections.Generic;  // can't alias

namespace AasCore.Aas3_0.Tests
{
    public class TestDescendAndVisitorThrough
    {
"""
    )

    for i, block in enumerate(blocks):
        if i > 0:
            writer.write("\n\n")

        writer.write(textwrap.indent(block, "        "))

    writer.write(
        """
    }  // class TestDescendAndVisitorThrough
}  // namespace AasCore.Aas3_0.Tests

/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */
"""
    )

    target_pth = repo_root / "src/AasCore.Aas3_0.Tests/TestDescendAndVisitorThrough.cs"
    target_pth.write_text(writer.getvalue(), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
