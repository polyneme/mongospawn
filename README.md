`mongospawn` is a tool to help spawn MongoDB resources given JSON Schema
specifications.

The primary near-term use case is support for the [National Microbiome Data
Collaborative (NMDC)](https://microbiomedata.org/) pilot project. In particular,
given a JSON Schema with all array-types properties and with each array item a
`$ref` reference to one of the JSON Schema `definitions` (see [NMDC
example](https://github.com/microbiomedata/nmdc-metadata/blob/d93d5f33b41d55a270dd014c8c27b18a6e804375/schema/nmdc.schema.json)),
`mongospawn` can generate MongoDB `$jsonSchema` documents to apply as validators
for collections in a database that correspond to each of the original JSON
Schema's array-typed properties. MongoDB's implementation of JSON Schema does
not support `$ref`, `definitions`, etc., so `mongospawn` expands references to
generate appropriate per-collection schema documents.

In addition to generating derived schema documents, `mongospawn` can spawn new
databases/collections, with schema validation set, via the `pymongo` driver, and
can also manage access to the spawned resources via `mongogrant`.

## Development
```
pip install -e .[dev]
```

### Testing
Use pinned dependencies:
```
make
```