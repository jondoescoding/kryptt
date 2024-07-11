import hashlib

def generate_unique_id(link: str) -> int:
    """
    Generates a unique integer ID from a given link using SHA-256 hashing.

    Args:
        link (str): The link to generate a unique ID from.

    Returns:
        int: A unique integer ID generated from the link.
    """
    return int(hashlib.sha256(link.encode()).hexdigest(), 16) % (10**6)


