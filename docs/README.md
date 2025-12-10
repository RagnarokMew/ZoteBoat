# Software Architecture Documentation

## Before you start

For the documentation to be as modular as possible please try to write each 
section in its own file to avoid conflict.

## Requirements

To build the software architecture documentation you will need `typst`.

## Building the documentation

```bash
$ make
# OR
$ typst compile master.typ
```

## Writing the documentation

For most of the documentation, writing clear text will be enough.

For more advanced features (adding images, styling, ...) please use the [typst reference](https://typst.app/docs/reference/)

### Adding sections to Detailed Component Design

Each section should have its own `.typ` file, placed in the components directory 
and should be included in `components.typ`. See `components/example.typ`

