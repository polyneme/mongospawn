from copy import deepcopy
import json
from typing import Dict

DBSchema = dict
CollSchema = dict


def dbschema_from_file(filepath) -> DBSchema:
    with open(filepath) as f:
        dbschema = json.load(f)
    check_dbschema(dbschema)
    return dbschema


def dbschema_from_str(json_str) -> DBSchema:
    dbschema = json.loads(json_str)
    check_dbschema(dbschema)
    return dbschema


def check_dbschema(dbschema):
    """raises an Exception if the given dbschema is invalid."""
    assert "properties" in dbschema, "No properties field in toplevel"
    assert "definitions" in dbschema, "No definitions field in toplevel"
    collections = dbschema["properties"]
    for name, spec in collections.items():
        assert spec.get("type") == "array", f"{name} not array-typed"
        itemspec = spec.get("items", {}).get(
            "$ref",
        )
        assert isinstance(itemspec, str) and itemspec.startswith(
            "#/definitions/"
        ), f"{name} item spec not a $ref"
        itemref = itemspec.split("#/definitions/")[-1]
        assert itemref in dbschema.get(
            "definitions"
        ), f"{name} reference to {itemref} not found in definitions"


def collschemas_for(dbschema: DBSchema) -> Dict[str, CollSchema]:
    """Give a database schema, generate a map of collection names to schemas."""
    check_dbschema(dbschema)
    collections = dbschema["properties"]
    collschemas = {}
    for coll_name, coll_spec in collections.items():
        coll_itemref = coll_spec["items"]["$ref"].split("#/definitions/")[-1]
        objschema = dbschema["definitions"][coll_itemref]
        objschema_new = make_compatible(objschema, dbschema)
        if "_id" not in objschema_new["properties"]:
            objschema_new["properties"]["_id"] = {"bsonType": "objectId"}
        collschemas[coll_name] = objschema_new
    return collschemas


def make_compatible(objschema, dbschema):
    """Produce a MongoDB-compatible object schema given the original.

    Tasks for compatibility:
    1. replace type="integer" specs with bsonType="long".
    2. expand and replace $ref usages (recursively as applicable).
    3. $jsonSchema keyword 'required' cannot be an empty array
    """
    objschema_new = deepcopy(objschema)
    properties_spec = objschema_new["properties"]
    property_names = [p for p in properties_spec]
    for p_name in property_names:
        p_spec = properties_spec[p_name]
        if p_spec.get("type") == "integer":
            p_spec["bsonType"] = ["int", "long"]
            p_spec.pop("type")
        if "$ref" in p_spec:
            ref = p_spec["$ref"].split("#/definitions/")[-1]
            if ref == objschema_new.get("title"): # same-type reference
                if "id" not in properties_spec:
                    # avoid infinite recursion
                    properties_spec.pop(p_name)
                else:
                    # reference to other document in this collection
                    p_spec["type"] = "string"
                    p_spec.pop("$ref")
            else:
                if "id" not in dbschema["definitions"][ref].get("properties"):
                    properties_spec[p_name] = make_compatible(
                        dbschema["definitions"][ref], dbschema
                    )
                else:
                    p_spec["type"] = "string"
                    p_spec.pop("$ref")
        if p_spec.get("type") == "array" and "$ref" in p_spec.get("items"):
            ref = p_spec["items"]["$ref"].split("#/definitions/")[-1]
            if ref == objschema_new.get("title"): # same-type reference
                if "id" not in properties_spec:
                    # avoid infinite recursion
                    properties_spec.pop(p_name)
                else:
                    # reference to other document in this collection
                    p_spec["items"]["type"] = "string"
                    p_spec["items"].pop("$ref")
            else:
                if "id" not in dbschema["definitions"][ref].get("properties"):
                    properties_spec[p_name]["items"] = make_compatible(
                        dbschema["definitions"][ref], dbschema
                    )
                else:
                    properties_spec[p_name]["items"]["type"] = "string"
                    properties_spec[p_name]["items"].pop("$ref")

    if "required" in objschema_new and len(objschema_new["required"]) == 0:
        objschema_new.pop("required")
    return objschema_new
