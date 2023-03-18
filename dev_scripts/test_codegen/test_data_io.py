"""Read test data."""
import inspect
import itertools
import json
import pathlib

import aas_core_codegen.naming
from aas_core_codegen import intermediate
from aas_core_codegen.common import Identifier
from aas_core_codegen.python import naming as python_naming
from icontract import require

from aas_core3 import types as aas_types, jsonization as aas_jsonization


def _load_instance_from_environment(
    path: pathlib.Path, cls: intermediate.ConcreteClass
) -> aas_types.Class:
    """Load an instance from the environment at ``path``."""
    with path.open("rt", encoding="utf-8") as fid:
        jsonable = json.load(fid)

    container = aas_jsonization.environment_from_jsonable(jsonable)

    cls_name_python = python_naming.class_name(cls.name)
    cls_python = getattr(aas_types, cls_name_python, None)
    assert cls_python is not None, (
        f"Could not find the class with name {cls_name_python!r} "
        f"in {aas_types.__name__}"
    )

    assert isinstance(cls_python, type)
    assert inspect.isclass(cls_python)

    for something in itertools.chain([container], container.descend()):
        if isinstance(something, cls_python):
            assert isinstance(something, aas_types.Class)
            return something

    raise AssertionError(
        f"Failed to find an instance of {cls_name_python!r} "
        f"beneath and including {container}"
    )


def _load_self_contained_instance(
    path: pathlib.Path, cls: intermediate.ConcreteClass
) -> aas_types.Class:
    """Load an instance self-contained at ``path``."""
    with path.open("rt", encoding="utf-8") as fid:
        jsonable = json.load(fid)

    from_function_name = python_naming.function_name(
        Identifier(f"{cls.name}_from_jsonable")
    )
    from_function = getattr(aas_jsonization, from_function_name, None)
    if from_function is None:
        raise AssertionError(
            f"Function {from_function_name!r} not found "
            f"in {aas_jsonization.__name__}"
        )

    assert inspect.isfunction(from_function)
    instance = from_function(jsonable)

    cls_name_python = python_naming.class_name(cls.name)
    cls_python = getattr(aas_types, cls_name_python, None)
    assert cls_python is not None, (
        f"Could not find the class with name {cls_name_python!r} "
        f"in {aas_types.__name__}"
    )

    assert isinstance(cls_python, type)
    assert inspect.isclass(cls_python)

    assert isinstance(
        instance, cls_python
    ), f"Expected an instance of {cls_python} at {path}, but got: {instance}"

    assert isinstance(instance, aas_types.Class)

    return instance


def load_maximal(
    test_data_dir: pathlib.Path, cls: intermediate.ConcreteClass
) -> aas_types.Class:
    """Load the maximal example for the given class."""
    cls_name_json = aas_core_codegen.naming.json_model_type(cls.name)

    base_path = (
        test_data_dir / "Json" / "ContainedInEnvironment" / "Expected" / cls_name_json
    )
    if base_path.exists():
        maximal_path = base_path / "maximal.json"

        return _load_instance_from_environment(path=maximal_path, cls=cls)

    base_path = test_data_dir / "Json" / "SelfContained" / "Expected" / cls_name_json
    if base_path.exists():
        maximal_path = base_path / "maximal.json"
        return _load_self_contained_instance(path=maximal_path, cls=cls)

    raise FileNotFoundError(
        f"The maximal JSON file for {cls.name!r} could not be found"
    )


def load_minimal(
    test_data_dir: pathlib.Path, cls: intermediate.ConcreteClass
) -> aas_types.Class:
    """Load the minimal example for the given class."""
    cls_name_json = aas_core_codegen.naming.json_model_type(cls.name)

    base_path = (
        test_data_dir / "Json" / "ContainedInEnvironment" / "Expected" / cls_name_json
    )
    if base_path.exists():
        minimal_path = base_path / "minimal.json"

        return _load_instance_from_environment(path=minimal_path, cls=cls)

    base_path = test_data_dir / "Json" / "SelfContained" / "Expected" / cls_name_json
    if base_path.exists():
        minimal_path = base_path / "minimal.json"
        return _load_self_contained_instance(path=minimal_path, cls=cls)

    raise FileNotFoundError(
        f"The minimal JSON file for {cls.name!r} could not be found"
    )


@require(lambda test_data_dir: test_data_dir.is_dir())
@require(lambda environment_cls: environment_cls.name == "Environment")
def determine_container_class(
    cls: intermediate.ConcreteClass,
    test_data_dir: pathlib.Path,
    environment_cls: intermediate.ConcreteClass,
) -> intermediate.ConcreteClass:
    """Determine the container class based on the test data directory."""
    cls_name_json = aas_core_codegen.naming.json_model_type(cls.name)

    contained_in_environment_path = (
        test_data_dir / "Json" / "ContainedInEnvironment" / "Expected" / cls_name_json
    )

    self_contained_path = (
        test_data_dir / "Json" / "SelfContained" / "Expected" / cls_name_json
    )

    if contained_in_environment_path.exists():
        return environment_cls
    elif self_contained_path.exists():
        return cls
    else:
        raise RuntimeError(
            f"Neither {contained_in_environment_path} nor {self_contained_path} "
            f"exist beneath {test_data_dir}. We do not know how to infer "
            f"the kind of how the instance of {cls_name_json} is contained."
        )
