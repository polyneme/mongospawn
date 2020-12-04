`mongospawn` is a tool to help spawn MongoDB resources given JSON Schema
specifications.

The primary near-term use case is support for the [National Microbiome Data
Collaborative (NMDC)](https://microbiomedata.org/) pilot project. In particular,
given a JSON Schema with all array-typed properties and with each array item a
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

## Setup
For development:
```
pip install -e .[dev]
```

To update dependency versions:
```
make update
```

To use pinned dependencies for reproducible testing:
```
make
```

# Usage

Example using [NMDC's JSON
Schema](https://github.com/microbiomedata/nmdc-metadata/blob/d93d5f33b41d55a270dd014c8c27b18a6e804375/schema/nmdc.schema.json):

```python
from mongospawn.schema import dbschema_from_file, collschemas_for
from pymongo import MongoClient

client = MongoClient()
db = client.nmdc_test

dbschema = dbschema_from_file("nmdc.schema.json")
collschemas = collschemas_for(dbschema)
for name in collschemas:
    db.drop_collection(name)
    db.create_collection(name, validator={"$jsonSchema": collschemas[name]})
    print(f"created {name} collection")
# created activity_set collection
# created biosample_set collection
# created data_object_set collection
# created omics_processing_set collection
# created study_set collection
```

Now, e.g. if you try to insert a non-conformant JSON document, a
`pymongo.errors.WriteError` will be raised:
```python
db.biosample_set.insert_one({"not_a_real_field": 1})
# => WriteError: Document failed validation...
```


