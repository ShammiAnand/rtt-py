def ensure_types_match(entity: str, type: str) -> bool:
    """
    checks if then entity value and the type are equivalent

    returns true if entity is a POSIX compliant path and type is dir
    returns true if entity is a url and type is url
    returns false otherwise
    """

    if type == "dir":
        return (
            entity.startswith("/")
            or entity.startswith("./")
            or entity.startswith("../")
        )
    elif type == "url":
        return entity.startswith("http://") or entity.startswith("https://")
    else:
        raise ValueError(f"unknown type {type}")
