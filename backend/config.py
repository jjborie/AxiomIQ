"""Simple configuration values for the demo backend implementation."""

# In a real world project these values would be loaded from environment
# variables or a dedicated configuration system.  To keep this example
# self‑contained we simply define them here.

# Dummy user credentials for the `/api/login` endpoint.
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password"

# Static bearer token returned on successful authentication.  The rest of the
# API simply verifies that the incoming requests contain this token.
ACCESS_TOKEN = "fake-token"


def verify_credentials(username: str, password: str) -> bool:
    """Validate a username and password pair.

    Parameters
    ----------
    username: str
        Username supplied by the client.
    password: str
        Password supplied by the client.

    Returns
    -------
    bool
        ``True`` if the credentials match the configured defaults.
    """

    return username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD
