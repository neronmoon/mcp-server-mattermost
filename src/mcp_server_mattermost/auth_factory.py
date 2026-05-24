"""FastMCP authentication provider selection."""

from fastmcp.server.auth import AuthProvider
from typing_extensions import assert_never

from .auth import MattermostTokenVerifier
from .auth_oauth import build_mattermost_oauth_proxy
from .config import AuthMode, Settings, get_settings


def build_auth_provider(settings: Settings) -> AuthProvider | None:
    """Build the FastMCP auth provider for the configured auth mode.

    Args:
        settings: Validated application settings.

    Returns:
        Auth provider for HTTP transports, or None for static token mode.
    """
    match settings.auth_mode:
        case AuthMode.STATIC_TOKEN:
            return None
        case AuthMode.CLIENT_TOKEN:
            return MattermostTokenVerifier()
        case AuthMode.OAUTH_PROXY:
            return build_mattermost_oauth_proxy(settings)
        case _ as unreachable:
            assert_never(unreachable)


def build_auth_provider_from_env() -> AuthProvider | None:
    """Build auth provider from environment-backed settings."""
    return build_auth_provider(get_settings())
