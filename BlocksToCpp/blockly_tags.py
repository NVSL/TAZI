block = "block"
shadow = "shadow"
statement = "statement"
value = "value"
mutation = "mutation"
comment = "comment"
field = "field"

def block_is_type( block, type_name ):
    if( type(type_name) == list):
        return block.tag in type_name
    return block.tag == type_name