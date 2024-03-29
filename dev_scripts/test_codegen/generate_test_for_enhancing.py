"""Generate the test code for enhancing the model instances."""

import io
import os
import pathlib
import sys
import textwrap
from typing import List, Optional

import aas_core_codegen
import aas_core_codegen.common
import aas_core_codegen.csharp.naming
import aas_core_codegen.naming
import aas_core_codegen.parse
import aas_core_codegen.run
from aas_core_codegen import intermediate
from aas_core_codegen.common import Stripped, Identifier
from aas_core_codegen.csharp import (
    common as csharp_common,
    naming as csharp_naming,
)
from aas_core_codegen.csharp.common import (
    INDENT as I,
    INDENT2 as II,
    INDENT3 as III,
    INDENT4 as IIII,
    INDENT5 as IIIII,
)

from test_codegen.common import load_symbol_table


def main() -> int:
    """Execute the main routine."""
    symbol_table = load_symbol_table()

    # noinspection PyListCreation
    blocks = [
        Stripped(
            f"""\
class Enhancement
{{
{I}public readonly long SomeCustomId;

{I}public Enhancement(long someCustomId)
{I}{{
{II}SomeCustomId = someCustomId;
{I}}}
}}"""
        ),
        Stripped(
            f"""\
private static AasEnhancing.Enhancer<Enhancement> CreateEnhancer()
{{
{I}long lastCustomId = 0;

{I}var enhancementFactory = new System.Func<IClass, Enhancement>(
{II}delegate
{II}{{
{III}lastCustomId++;
{III}return new Enhancement(lastCustomId);
{II}}}
{I});

{I}return new AasEnhancing.Enhancer<Enhancement>(enhancementFactory);
}}"""
        ),
    ]  # type: List[Stripped]

    for our_type in symbol_table.our_types:
        if not isinstance(our_type, intermediate.ConcreteClass):
            continue

        cls_name = csharp_naming.class_name(our_type.name)

        blocks.append(
            Stripped(
                f"""\
[Test]
public void Test_{cls_name}()
{{
{I}var instance = (
{II}Aas.Tests.CommonJsonization.LoadMaximal{cls_name}()
{I});

{I}var enhancer = CreateEnhancer();
{I}
{I}Assert.IsNull(enhancer.Unwrap(instance));

{I}var wrapped = enhancer.Wrap(instance);
{I}Assert.IsNotNull(wrapped);

{I}var idSet = new HashSet<long>();

{I}idSet.Add(enhancer.MustUnwrap(wrapped).SomeCustomId);
{I}idSet.UnionWith(
{II}wrapped
{III}.Descend()
{III}.Select(
{IIII}(descendant) =>
{IIIII}enhancer.MustUnwrap(descendant).SomeCustomId
{IIII})
{I});

{I}Assert.AreEqual(1, idSet.Min());
{I}Assert.AreEqual(idSet.Count, idSet.Max());
}}  // public void Test_{cls_name}"""
            )
        )

    writer = io.StringIO()
    writer.write(
        f"""\
/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */

using Aas = AasCore.Aas3_0; // renamed
using AasEnhancing = AasCore.Aas3_0.Enhancing; // renamed

using System.Collections.Generic; // can't alias
using System.Linq; // can't alias

using NUnit.Framework; // can't alias

namespace AasCore.Aas3_0.Tests
{{
{I}public class TestEnhancing
{II}{{
"""
    )

    for i, block in enumerate(blocks):
        if i > 0:
            writer.write("\n\n")

        writer.write(textwrap.indent(block, II))

    writer.write(
        """
    }  // class TestEnhancing
}  // namespace AasCore.Aas3_0.Tests

/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */
"""
    )

    this_path = pathlib.Path(os.path.realpath(__file__))
    repo_root = this_path.parent.parent.parent

    target_pth = repo_root / "src/AasCore.Aas3_0.Tests/TestEnhancing.cs"
    target_pth.write_text(writer.getvalue(), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
