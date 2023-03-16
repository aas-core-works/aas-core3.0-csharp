# How to build the documentation

Change to the repository root directory.

## Install DocFX

[Docfx] is the tool we use to render our documentation into HTML.

[docfx]: https://dotnet.github.io/docfx/index.html

Change to the `doc/` directory from the root repository and install docfx there:

```
cd doc/
nuget install docfx.console -Version 2.59.3
```

The docfx will be installed to `doc/docfx.console.2.59.3`.

## Render the Documentation

Now change back to the repository root.

First build the solution with:

```
dotnet build src/
```

The build step is necessary, so that references can be correctly de-referenced.
Otherwise, you will see `Invalid cref value "!:..."` warnings.
See [this docfx issue on GitHub].

[this docfx issue on GitHub]: https://github.com/dotnet/docfx/issues/5112

Then call the rendering script to render the documentation:

```
doc/docfx.console.2.59.3/tools/docfx.exe doc/source/docfx.json
```

The script will install the exact docfx version locally in the `doc/` directory if it has not been installed before.

The documentation resides now in `doc/build`.

If you want to read it, open the file `doc/build/index.html` in your browser.
