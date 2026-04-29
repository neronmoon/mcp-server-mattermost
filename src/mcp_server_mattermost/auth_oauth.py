"""Mattermost OAuthProxy construction."""

from fastmcp.server.auth import OAuthProxy

from .auth import MattermostTokenVerifier
from .config import OAuthClientType, Settings


def build_mattermost_oauth_proxy(settings: Settings) -> OAuthProxy:
    """Build a FastMCP OAuthProxy configured for Mattermost OAuth.

    Args:
        settings: Validated application settings.

    Returns:
        Configured FastMCP OAuthProxy instance.

    Raises:
        ValueError: If oauth_proxy settings are missing.
    """
    if not settings.oauth_mcp_public_url:
        msg = "oauth_mcp_public_url is required"
        raise ValueError(msg)
    if not settings.oauth_client_id:
        msg = "oauth_client_id is required"
        raise ValueError(msg)

    mattermost_public_url = settings.oauth_mattermost_public_url or settings.url

    if settings.oauth_client_type is OAuthClientType.PUBLIC:
        return OAuthProxy(
            upstream_authorization_endpoint=f"{mattermost_public_url}/oauth/authorize",
            upstream_token_endpoint=f"{settings.url}/oauth/access_token",
            upstream_client_id=settings.oauth_client_id,
            upstream_client_secret="",
            token_verifier=MattermostTokenVerifier(),
            base_url=settings.oauth_mcp_public_url,
            redirect_path=settings.oauth_callback_path,
            allowed_client_redirect_uris=settings.oauth_allowed_redirect_uris,
            forward_pkce=True,
            token_endpoint_auth_method="none",  # noqa: S106
            jwt_signing_key=settings.oauth_jwt_signing_key,
            require_authorization_consent=settings.oauth_require_consent,
            fallback_access_token_expiry_seconds=settings.oauth_fallback_access_token_expiry_seconds,
        )

    return OAuthProxy(
        upstream_authorization_endpoint=f"{mattermost_public_url}/oauth/authorize",
        upstream_token_endpoint=f"{settings.url}/oauth/access_token",
        upstream_client_id=settings.oauth_client_id,
        upstream_client_secret=settings.oauth_client_secret or "",
        token_verifier=MattermostTokenVerifier(),
        base_url=settings.oauth_mcp_public_url,
        redirect_path=settings.oauth_callback_path,
        allowed_client_redirect_uris=settings.oauth_allowed_redirect_uris,
        forward_pkce=True,
        token_endpoint_auth_method="client_secret_post",  # noqa: S106
        jwt_signing_key=settings.oauth_jwt_signing_key,
        require_authorization_consent=settings.oauth_require_consent,
        fallback_access_token_expiry_seconds=settings.oauth_fallback_access_token_expiry_seconds,
    )
