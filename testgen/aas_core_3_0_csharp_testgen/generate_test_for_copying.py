"""Generate the test code for making shallow and deep copies."""

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
)

from aas_core_3_0_csharp_testgen.common import load_symbol_table


def _generate_shallow_equals(cls: intermediate.ConcreteClass) -> Stripped:
    """Generate the code for a static shallow ``Equals`` method."""
    if cls.is_implementation_specific:
        raise AssertionError(
            f"(mristin, 2022-11-04): "
            f"The class {cls.name!r} is implementation specific. "
            f"At the moment, we assume that all classes are not "
            f"implementation-specific, so that we can automatically generate the "
            f"shallow-equals methods. This way we can dispense of the whole "
            f"snippet/specific-implementation loading logic in "
            f"the unit test generation. Please notify the developers if you see this, "
            f"so that we can add the logic for implementation-specific classes "
            f"to this generation script."
        )

    exprs = []  # type: List[str]
    for prop in cls.properties:
        prop_name = csharp_naming.property_name(prop.name)
        exprs.append(f"that.{prop_name} == other.{prop_name}")

    # NOTE (mristin, 2022-11-04):
    # This is a poor man's line re-flowing.
    exprs_joined = " && ".join(exprs)
    if len(exprs_joined) < 70:
        statement = Stripped(f"return {exprs_joined};")
    else:
        exprs_joined = "\n&& ".join(exprs)
        statement = Stripped(
            f"""\
return (
{I}{aas_core_codegen.common.indent_but_first_line(exprs_joined, I)});"""
        )

    cls_name_csharp = aas_core_codegen.csharp.naming.class_name(cls.name)

    return Stripped(
        f"""\
private static bool {cls_name_csharp}ShallowEquals(
{I}Aas.{cls_name_csharp} that,
{I}Aas.{cls_name_csharp} other)
{{
{I}{aas_core_codegen.common.indent_but_first_line(statement, I)}
}}"""
    )


def _generate_transform_as_deep_equals(cls: intermediate.ConcreteClass) -> Stripped:
    """Generate the transform method that checks for deep equality."""
    if cls.is_implementation_specific:
        raise AssertionError(
            f"(mristin, 2022-11-04): "
            f"The class {cls.name!r} is implementation specific. "
            f"At the moment, we assume that all classes are not "
            f"implementation-specific, so that we can automatically generate the "
            f"shallow-equals methods. This way we can dispense of the whole "
            f"snippet/specific-implementation loading logic in "
            f"the unit test generation. Please notify the developers if you see this, "
            f"so that we can add the logic for implementation-specific classes "
            f"to this generation script."
        )

    cls_name = csharp_naming.class_name(cls.name)

    exprs = []  # type: List[Stripped]

    for prop in cls.properties:
        optional = isinstance(prop.type_annotation, intermediate.OptionalTypeAnnotation)
        type_anno = intermediate.beneath_optional(prop.type_annotation)

        prop_name = csharp_naming.property_name(prop.name)

        expr = None  # type: Optional[Stripped]

        primitive_type = intermediate.try_primitive_type(type_anno)

        # fmt: off
        if (
                isinstance(type_anno, intermediate.PrimitiveTypeAnnotation)
                or (
                    isinstance(type_anno, intermediate.OurTypeAnnotation)
                    and isinstance(
                        type_anno.our_type, intermediate.ConstrainedPrimitive
                    )
                )
        ):
            # fmt: on
            assert primitive_type is not None
            if (
                    primitive_type is intermediate.PrimitiveType.BOOL
                or primitive_type is intermediate.PrimitiveType.INT
                or primitive_type is intermediate.PrimitiveType.FLOAT
                or primitive_type is intermediate.PrimitiveType.STR
            ):
                expr = Stripped(f"that.{prop_name} == casted.{prop_name}")
            elif primitive_type is intermediate.PrimitiveType.BYTEARRAY:
                expr = Stripped(
                        f"""\
ByteSpansEqual(
{I}that.{prop_name},
{I}casted.{prop_name})"""
                )
            else:
                aas_core_codegen.common.assert_never(primitive_type)
        elif isinstance(type_anno, intermediate.OurTypeAnnotation):
            if isinstance(type_anno.our_type, intermediate.Enumeration):
                expr = Stripped(f"that.{prop_name} == casted.{prop_name}")
            elif isinstance(type_anno.our_type, intermediate.ConstrainedPrimitive):
                raise AssertionError("Expected to handle this case above")
            elif isinstance(
                    type_anno.our_type,
                    (intermediate.AbstractClass, intermediate.ConcreteClass)
            ):
                expr = Stripped(
                    f"""\
Transform(
{I}that.{prop_name},
{I}casted.{prop_name})"""
                )
            else:
                aas_core_codegen.common.assert_never(type_anno.our_type)
        elif isinstance(type_anno, intermediate.ListTypeAnnotation):
            assert (
                    isinstance(type_anno.items, intermediate.OurTypeAnnotation)
                    and isinstance(type_anno.items.our_type, intermediate.Class)
            ), (
                f"(mristin, 2022-11-03): We handle only lists of classes in the deep "
                f"equality checks at the moment. The meta-model does not contain "
                f"any other lists, so we wanted to keep the code as simple as "
                f"possible, and avoid unrolling. Please contact the developers "
                f"if you need this feature. The class in question was {cls.name!r} and "
                f"the property {prop.name!r}."
            )

            expr = Stripped(
                f"""\
that.{prop_name}.Count == casted.{prop_name}.Count
&& (
{I}that.{prop_name}
{II}.Zip(
{III}casted.{prop_name},
{III}Transform)
{II}.All(item => item))"""
            )
        else:
            aas_core_codegen.common.assert_never(type_anno)

        if optional and primitive_type is None:
            expr = Stripped(
                f"""\
(that.{prop_name} != null && casted.{prop_name} != null)
{I}? {aas_core_codegen.common.indent_but_first_line(expr, II)}
{I}: that.{prop_name} == null && casted.{prop_name} == null"""
            )

        exprs.append(expr)

    body_writer = io.StringIO()
    body_writer.write("return (")
    for i, expr in enumerate(exprs):
        body_writer.write("\n")
        if i > 0:
            body_writer.write(
                f"{I}&& {aas_core_codegen.common.indent_but_first_line(expr, I)}"
            )
        else:
            body_writer.write(
                f"{I}{aas_core_codegen.common.indent_but_first_line(expr, I)}"
            )

    body_writer.write(");")

    interface_name = csharp_naming.interface_name(cls.name)
    transform_name = csharp_naming.method_name(Identifier(f"transform_{cls.name}"))

    return Stripped(
        f"""\
public override bool {transform_name}(
{I}Aas.{interface_name} that,
{I}Aas.IClass other)
{{
{I}if (!(other is Aas.{cls_name} casted))
{I}{{
{II}return false;
{I}}}

{I}{aas_core_codegen.common.indent_but_first_line(body_writer.getvalue(), I)}
}}"""
    )


def _generate_deep_equals_transformer(
    symbol_table: intermediate.SymbolTable,
) -> Stripped:
    """Generate the transformer that checks for deep equality."""
    blocks = [
        Stripped(
            f"""\
/// <summary>Compare two byte spans for equal content.</summary>
/// <remarks>
/// <c>byte[]</c> implicitly converts to <c>ReadOnlySpan</c>.
/// See: https://stackoverflow.com/a/48599119/1600678
/// </remarks>
private static bool ByteSpansEqual(
{I}System.ReadOnlySpan<byte> that,
{I}System.ReadOnlySpan<byte> other)
{{
{I}return that.SequenceEqual(other);
}}"""
        )
    ]  # type: List[Stripped]

    for our_type in symbol_table.our_types:
        if not isinstance(our_type, intermediate.ConcreteClass):
            continue

        if our_type.is_implementation_specific:
            raise AssertionError(
                f"(mristin, 2022-11-04): "
                f"The class {our_type.name!r} is implementation specific. "
                f"At the moment, we assume that all classes are not "
                f"implementation-specific, so that we can automatically generate the "
                f"deep-equals methods. This way we can dispense of the whole "
                f"snippet/specific-implementation loading logic in "
                f"the unit test generation. Please notify the developers if you see "
                f"this, so that we can add the logic for implementation-specific "
                f"classes to this generation script."
            )

        blocks.append(_generate_transform_as_deep_equals(cls=our_type))

    writer = io.StringIO()
    writer.write(
        f"""\
internal class DeepEqualsier
{I}: Aas.Visitation.AbstractTransformerWithContext<Aas.IClass, bool>
{{
"""
    )

    for i, block in enumerate(blocks):
        if i > 0:
            writer.write("\n\n")

        writer.write(textwrap.indent(block, I))

    writer.write("\n}  // internal class DeepEqualsier")

    return Stripped(writer.getvalue())


def _generate_deep_equals(cls: intermediate.ConcreteClass) -> Stripped:
    """Generate the code for a static deep ``Equals`` method."""
    if cls.is_implementation_specific:
        raise AssertionError(
            f"(mristin, 2022-11-04): "
            f"The class {cls.name!r} is implementation specific. "
            f"At the moment, we assume that all classes are not "
            f"implementation-specific, so that we can automatically generate the "
            f"shallow-equals methods. This way we can dispense of the whole "
            f"snippet/specific-implementation loading logic in "
            f"the unit test generation. Please notify the developers if you see this, "
            f"so that we can add the logic for implementation-specific classes "
            f"to this generation script."
        )

    cls_name = csharp_naming.class_name(cls.name)

    return Stripped(
        f"""\
private static bool {cls_name}DeepEquals(
{I}Aas.{cls_name} that,
{I}Aas.{cls_name} other)
{{
{I}return DeepEqualsierInstance.Transform(that, other);
}}"""
    )


def main() -> int:
    """Execute the main routine."""
    symbol_table = load_symbol_table()

    # noinspection PyListCreation
    blocks = [
        _generate_deep_equals_transformer(symbol_table=symbol_table),
        Stripped(
            f"""\
private static readonly DeepEqualsier DeepEqualsierInstance = new DeepEqualsier();"""
        ),
    ]  # type: List[Stripped]

    for our_type in symbol_table.our_types:
        if not isinstance(our_type, intermediate.ConcreteClass):
            continue

        blocks.append(_generate_shallow_equals(cls=our_type))

    for our_type in symbol_table.our_types:
        if not isinstance(our_type, intermediate.ConcreteClass):
            continue

        blocks.append(_generate_deep_equals(cls=our_type))

    for our_type in symbol_table.our_types:
        if not isinstance(our_type, intermediate.ConcreteClass):
            continue

        cls_name = csharp_naming.class_name(our_type.name)

        blocks.append(
            Stripped(
                f"""\
[Test]
public void Test_{cls_name}_shallow_copy()
{{
    Aas.{cls_name} instance = (
        Aas.Tests.CommonJsonization.LoadMaximal{cls_name}());

    var instanceCopy = Aas.Copying.Shallow(instance);

    Assert.IsTrue(
        {cls_name}ShallowEquals(
            instance, instanceCopy),
        {csharp_common.string_literal(cls_name)});
}}  // public void Test_{cls_name}_shallow_copy"""
            )
        )

        blocks.append(
            Stripped(
                f"""\
[Test]
public void Test_{cls_name}_deep_copy()
{{
    Aas.{cls_name} instance = (
        Aas.Tests.CommonJsonization.LoadMaximal{cls_name}());

    var instanceCopy = Aas.Copying.Deep(instance);

    Assert.IsTrue(
        {cls_name}DeepEquals(
            instance, instanceCopy),
        {csharp_common.string_literal(cls_name)});
}}  // public void Test_{cls_name}_deep_copy"""
            )
        )

    blocks.append(
        Stripped(
            """\
[Test]
public void Test_snippet_in_docs()
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
    var deepCopy = Aas.Copying.Deep(environment);

    // Make a shallow copy
    var shallowCopy = Aas.Copying.Shallow(environment);

    // Changes to the property affect only the shallow copy,
    // but not the deep one
    environment.Submodels[0].SubmodelElements![0].IdShort = "changed";

    Assert.AreEqual(
        "changed",
        shallowCopy.Submodels![0].SubmodelElements![0].IdShort);

    Assert.AreEqual(
        "someProperty",
        deepCopy.Submodels![0].SubmodelElements![0].IdShort);
}  // public void Test_snippet_in_docs"""
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

// We need to use System.MemoryExtension.SequenceEqual.
using System;  // can't alias
using System.Collections.Generic;  // can't alias
using System.Linq;  // can't alias

using NUnit.Framework;  // can't alias

namespace AasCore.Aas3_0.Tests
{
    public class TestCopying
    {
"""
    )

    for i, block in enumerate(blocks):
        if i > 0:
            writer.write("\n\n")

        writer.write(textwrap.indent(block, "        "))

    writer.write(
        """
    }  // class TestCopying
}  // namespace AasCore.Aas3_0.Tests

/*
 * This code has been automatically generated by testgen.
 * Do NOT edit or append.
 */
"""
    )

    this_path = pathlib.Path(os.path.realpath(__file__))
    repo_root = this_path.parent.parent.parent

    target_pth = repo_root / "src/AasCore.Aas3_0.Tests/TestCopying.cs"
    target_pth.write_text(writer.getvalue(), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
