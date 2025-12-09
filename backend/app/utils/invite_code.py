"""Invite code generation utilities."""
import secrets
import string


def generate_invite_code(length: int = 12) -> str:
    """
    Generate a random invite code.

    Args:
        length: Length of the invite code (default 12)

    Returns:
        URL-safe random string
    """
    alphabet = string.ascii_uppercase + string.digits
    # Exclude similar looking characters: 0, O, I, 1
    alphabet = alphabet.replace('0', '').replace('O', '').replace('I', '').replace('1', '')
    return ''.join(secrets.choice(alphabet) for _ in range(length))
