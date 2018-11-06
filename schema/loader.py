import os
import json
import jsonschema


SCHEMA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json')
SCHEMA_EXTENSION = 'json'


def get_schema(schema_name):
    schema_name_fs = '{schema_name_canonical}.{schema_ext}'.format(
        schema_name_canonical=get_schema_name_canonical(schema_name),
        schema_ext=SCHEMA_EXTENSION,
    )
    schema_path = os.path.join(SCHEMA_FOLDER, schema_name_fs)
    if not os.path.isfile(schema_path):
        raise jsonschema.exceptions.SchemaError(f'{schema_name} does not exists at path {schema_path}')

    with open(schema_path, 'r') as descriptor:
        return json.load(descriptor)


def get_schema_name_canonical(schema_name):
    parsed_uri = jsonschema.compat.urlsplit(schema_name)
    schema_name = parsed_uri.path or parsed_uri.netloc

    return schema_name


def validate(data, schema, schema_name=None):
    try:
        jsonschema.validate(
            data,
            schema,
            resolver=jsonschema.RefResolver(
                base_uri='',
                referrer=None,
                handlers={'multi': get_schema},
            )
        )
    except jsonschema.exceptions.ValidationError as err:
        err.message = f'schema_name: {schema_name}:  {err.message}'
        raise err
