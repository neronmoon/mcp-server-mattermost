# Configuration

All configuration is done via environment variables with the `MATTERMOST_` prefix.

## Required Variables

| Variable | Description |
|----------|-------------|
| `MATTERMOST_URL` | Mattermost server URL (e.g., `https://mattermost.example.com`) |

## Conditional Variables

| Variable | Description |
|----------|-------------|
| `MATTERMOST_TOKEN` | Bot or personal access token. Required only when `MATTERMOST_AUTH_MODE=static_token`. |
| `MATTERMOST_OAUTH_CLIENT_ID` | Mattermost OAuth App client ID. Required when `MATTERMOST_AUTH_MODE=oauth_proxy`. |
| `MATTERMOST_OAUTH_CLIENT_SECRET` | Mattermost OAuth App secret. Required for confidential OAuth Apps. |
| `MATTERMOST_OAUTH_MCP_PUBLIC_URL` | Public base URL of this MCP server. Required when `MATTERMOST_AUTH_MODE=oauth_proxy`. |

## Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MATTERMOST_TIMEOUT` | 30 | Request timeout in seconds (1-300) |
| `MATTERMOST_MAX_RETRIES` | 3 | Maximum retry attempts for failed requests (0-10) |
| `MATTERMOST_VERIFY_SSL` | true | Verify SSL certificates |
| `MATTERMOST_LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `MATTERMOST_LOG_FORMAT` | json | Log format: `json` for production, `text` for development |
| `MATTERMOST_API_VERSION` | v4 | Mattermost API version |
| `MATTERMOST_AUTH_MODE` | static_token | Authentication mode: `static_token`, `client_token`, or `oauth_proxy` |
| `MATTERMOST_ALLOW_HTTP_CLIENT_TOKENS` | false | Deprecated alias for `MATTERMOST_AUTH_MODE=client_token` |
| `MATTERMOST_OAUTH_CLIENT_TYPE` | confidential | Mattermost OAuth App type: `public` or `confidential` |
| `MATTERMOST_OAUTH_MATTERMOST_PUBLIC_URL` | `MATTERMOST_URL` | Browser-facing Mattermost URL for OAuth redirects |
| `MATTERMOST_OAUTH_CALLBACK_PATH` | `/oauth/callback/mm` | Callback path registered in the Mattermost OAuth App |
| `MATTERMOST_OAUTH_JWT_SIGNING_KEY` | — | FastMCP JWT signing key. Required for public OAuth Apps, optional for confidential OAuth Apps. |

## Environment File

You can also use a `.env` file in the working directory:

```bash
MATTERMOST_URL=https://mattermost.example.com
MATTERMOST_TOKEN=your-token-here
MATTERMOST_TIMEOUT=60
MATTERMOST_LOG_LEVEL=DEBUG
```

## Authentication Modes

`MATTERMOST_AUTH_MODE` selects one authentication strategy per server process.

### `static_token`

Default mode. The server uses `MATTERMOST_TOKEN` for every Mattermost API request.
Use this for stdio, bot accounts, and single-user deployments.

### `client_token`

HTTP clients send their own Mattermost token in `Authorization: Bearer <token>`.
The server validates it through `GET /api/v4/users/me` and then uses that token for
Mattermost API calls.

`MATTERMOST_ALLOW_HTTP_CLIENT_TOKENS=true` is a deprecated alias for this mode.

### `oauth_proxy`

Remote MCP clients authenticate with the MCP server through the standard MCP OAuth
flow. FastMCP `OAuthProxy` redirects the user to Mattermost OAuth, Mattermost performs
login through its configured SSO provider such as Keycloak, and the MCP server stores
the resulting Mattermost user token as an upstream token.

Mattermost OAuth App settings:

| Setting | Public PoC mode | Confidential production mode |
|---------|-----------------|------------------------------|
| Is Trusted | Yes | Yes |
| Is Public Client | Yes | No |
| Client Secret | Empty | Required |
| Callback URL | `{MATTERMOST_OAUTH_MCP_PUBLIC_URL}/oauth/callback/mm` | `{MATTERMOST_OAUTH_MCP_PUBLIC_URL}/oauth/callback/mm` |
| PKCE | S256 | S256 |

The MCP server does not register directly in Keycloak. Keycloak is used by Mattermost
for SSO login, and Mattermost issues the OAuth token that the MCP server uses for API
calls.

!!! warning "Security Considerations"
    In `client_token` and `oauth_proxy` modes, any user who can reach the MCP server's
    HTTP endpoint and has a valid Mattermost account can execute MCP tools under their
    own identity. Protect the MCP server with network-level access controls such as a
    firewall, VPN, or trusted reverse proxy.

## Token Permissions

The bot token needs these permissions for full functionality:

| Permission | Required For |
|------------|--------------|
| `create_post` | Sending messages |
| `read_channel` | Reading channel messages |
| `manage_channel_members` | Adding users to channels |
| `create_direct_channel` | Creating DM channels |
| `upload_files` | File uploads |

For read-only usage, only `read_channel` permission is needed.
