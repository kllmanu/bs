def blue(text) -> str:
    """Return the text in blue color."""
    return f"\033[1;34m{text}\033[0m"


def green(text) -> str:
    """Return the text in green color."""
    return f"\033[1;32m{text}\033[0m"


def magenta(text) -> str:
    """Return the text in magenta color."""
    return f"\033[1;35m{text}\033[0m"


def select(items, selected) -> list:
    """Retrieve the original object after selection."""

    # Create a mapping from string representation to object
    repr_to_obj = {repr(item): item for item in items}

    # Get the original object(s)
    selected_objects = [repr_to_obj[s] for s in selected]

    return selected_objects
