# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.19] - 2025-10-14

### Fixed

* 🔁 **Reverted Client Header Forwarding**: Reverted changes introduced in 0.0.18.

## [0.0.18] - 2025-10-14

### Added

* 🧩 **OAuth Support for Streamable HTTP Servers**: Introduced full OAuth 2.0 support with dynamic client registration for 'streamable_http' MCP servers. This enables secure, standards-compliant authentication flows for both user and service clients.
* 🔧 **Configurable Disabled Tools**: Added 'disabled_tools' option in server configuration, allowing selective disabling of specific tools without modifying code. Useful for managing staged rollouts or limited-access environments.
* 🧠 **Adjustable Log Level at Runtime**: Logging verbosity can now be adjusted dynamically, giving operators finer control over monitoring and debugging noise without requiring restarts.
* 🔁 **Client Header Forwarding**: Added automatic forwarding of client HTTP headers to MCP backends—enabling trace propagation, correlation IDs, and richer observability in distributed environments.
* 🛤️ **Support for Custom Path Prefixes**: Servers can now run under a custom path prefix, allowing flexible deployment within multi-service gateways or reverse proxy environments.
* 📄 **Root Path Documentation**: Added documentation describing behavior and configuration for root path handling in multi-app or nested setups.

### Changed

* 🧰 **Refactored Connection Timeout Defaults**: Connection timeout is now set to 'None' by default to prevent premature disconnects during long-running or streaming tasks.
* 🧹 **Removed Deprecated Python Version Tagging**: Dropped explicit Python version tagging; the project now officially supports Python 3.11 and above without manual tagging overhead.

### Fixed

* 🪛 **Improved Hot Reload Lifespan Tracking**: Fixed an issue where sub-applications created during hot reloads were not properly initialized or cleaned up—ensuring stable lifecycle management during dynamic reconfiguration.
* 🔗 **Symlink Handling in Config Watcher**: Resolved a bug where configuration symlinks were not updating correctly on modification; watcher now tracks and reloads the proper file path automatically.

## [0.0.17] - 2025-07-22

### Added

- 🔄 **Hot Reload Support for Configuration Files**: Added \`--hot-reload\` flag to watch your config file for changes and dynamically reload MCP servers without restarting the application—enabling seamless development workflows and runtime configuration updates.
- 🤫 **HTTP Request Filtering for Cleaner Logs**: Added configurable log filtering to reduce noise from frequent HTTP requests, making debugging and monitoring much clearer in production environments.

### Changed

- ⬆️ **Updated MCP Package to v1.12.1**: Upgraded MCP dependency to resolve compatibility issues with Pydantic and improve overall stability and performance.
- 🔧 **Normalized Streamable HTTP Configuration**: Streamlined configuration syntax for streamable-http servers to align with MCP standards while maintaining backward compatibility.

## [0.0.16] - 2025-07-02

### Added

- 🔁 **Enhanced Endpoint Support for Arbitrary Return Types**: Endpoints can now return any JSON-serializable value—removing limitations on tool outputs and enabling support for more diverse workflows, including advanced data structures or dynamic return formats.
- 🪵 **Improved Log Clarity with Streamlined Print Trace Output**: Internal logging has been upgraded with more structured and interpretable print traces, giving users clearer visibility into backend tool behavior and execution flow—especially helpful when debugging multi-agent sequences or nested toolchains.

### Fixed

- 🔄 **Resolved Infinite Loop Edge Case in Custom Schema Inference**: Fixed a bug where circular references ($ref) caused schema processing to hang or crash in rare custom schema setups—ensuring robust and reliable auto-documentation even for deeply nested models.

## [0.0.15] - 2025-06-06

### Added

- 🔐 **Support for Custom Headers in SSE and Streamable Http MCP Connections**: You can now pass custom HTTP headers (e.g., for authentication tokens or trace IDs) when connecting to SSE or streamable_http servers—enabling seamless integration with remote APIs that require secure or contextual headers.
- 📘 **MCP Server Instructions Exposure**: mcpo now detects and exposes instructions output by MCP tools, bringing descriptive setup guidelines and usage help directly into the OpenAPI schema—so users, UIs, and LLM agents can better understand tool capabilities with zero additional config.
- 🧪 **MCP Exception Stacktrace Printing During Failures**: When a connected MCP server raises an internal error, mcpo now displays the detailed stacktrace from the tool directly in the logs—making debugging on failure dramatically easier for developers and MLops teams working on complex flows.

### Fixed

- 🧽 **Corrected Handling of Underscore Prefix Parameters in Pydantic Modes**: Parameters with leading underscores (e.g. _token) now work correctly without conflict or omission in auto-generated schemas—eliminating validation issues and improving compatibility with tools relying on such parameter naming conventions.

## [0.0.14] - 2025-05-11

### Added

- 🌐 **Streamable HTTP Transport Support**: mcpo now supports MCP servers using the Streamable HTTP transport. This allows for more flexible and robust communication, including session management and resumable streams. Configure via CLI with '--server-type "streamable_http" -- <URL>' or in the config file with 'type: "streamable_http"' and a 'url'.

## [0.0.13] - 2025-05-01

### Added

- 🧪 **Support for Mixed and Union Types (anyOf/nullables)**: mcpo now accurately exposes OpenAPI schemas with anyOf compositions and nullable fields.
- 🧷 **Authentication-Required Docs Access with --strict-auth**: When enabled, the new --strict-auth option restricts access to both the tool endpoints and their interactive documentation pages—ensuring sensitive internal services aren’t inadvertently exposed to unauthenticated users or LLMs.
- 🧬 **Custom Schema Definitions for Complex Models**: Developers can now register custom BaseModel schemas with arbitrary nesting and field variants, allowing precise OpenAPI representations of deeply structured payloads—ensuring crystal-clear docs and compatibility for multi-layered data workflows.
- 🔄 **Smarter Schema Inference Across Data Types**: Schema generation has been enhanced to gracefully handle nested unions, nulls, and fallback types, dramatically improving accuracy in tools using variable output formats or flexible data contracts.

## [0.0.12] - 2025-04-14

### Fixed

- ⏳ **Disabled SSE Read Timeout to Prevent Inactivity Errors**: Resolved an issue where Server-Sent Events (SSE) MCP tools would unexpectedly terminate after 5 minutes of no activity—ensuring durable, always-on connections for real-time workflows like streaming updates, live dashboards, or long-running agents.

## [0.0.11] - 2025-04-12

### Added

- 🌊 **SSE-Based MCP Server Support**: mcpo now supports SSE (Server-Sent Events) MCP servers out of the box—just pass 'mcpo --server-type "sse" -- http://127.0.0.1:8001/sse' when launching or use the standard "url" field in your config for seamless real-time integration with streaming MCP endpoints; see the README for full examples and enhanced workflows with live progress, event pushes, and interactive updates.

## [0.0.10] - 2025-04-10

### Added

- 📦 **Support for --env-path to Load Environment Variables from File**: Use the new --env-path flag to securely pass environment variables via a .env-style file—making it easier than ever to manage secrets and config without cluttering your CLI or exposing sensitive data.
- 🧪 **Enhanced Support for Nested Object and Array Types in OpenAPI Schema**: Tools with complex input/output structures (e.g., JSON payloads with arrays or nested fields) are now correctly interpreted and exposed with accurate OpenAPI documentation—making form-based testing in the UI smoother and integrations far more predictable.
- 🛑 **Smart HTTP Exceptions for Better Debugging**: Clear, structured HTTP error responses are now automatically returned for bad requests or internal tool errors—helping users immediately understand what went wrong without digging through raw traces.

### Fixed

- 🪛 **Fixed --env Flag Behavior for Inline Environment Variables**: Resolved issues where the --env CLI flag silently failed or misbehaved—environment injection is now consistent and reliable whether passed inline with --env or via --env-path.

## [0.0.9] - 2025-04-06

### Added

- 🧭 **Clearer Docs Navigation with Path Awareness**: Optimized the /docs and /[tool]/docs pages to clearly display full endpoint paths when using mcpo --config, making it obvious where each tool is hosted—no more guessing or confusion when running multiple tools under different routes.
- 🛤️ **New --path-prefix Option for Precise Routing Control**: Introduced optional --path-prefix flag allowing you to customize the route prefix for all mounted tools—great for integrating mcpo into existing infrastructures, reverse proxies, or multi-service APIs without route collisions.
- 🐳 **Official Dockerfile for Easy Deployment**: Added a first-party Dockerfile so you can containerize mcpo in seconds—perfect for deploying to production, shipping models with standardized dependencies, and running anywhere with a consistent environment.

## [0.0.8] - 2025-04-03

### Added

- 🔒 **SSL Support via '--ssl-certfile' and '--ssl-keyfile'**: Easily enable HTTPS for your mcpo servers by passing certificate and key files—ideal for securing deployments in production, enabling encrypted communication between clients (e.g. browsers, AI agents) and your MCP tools without external proxies.

## [0.0.7] - 2025-04-03

### Added

- 🖼️ **Image Content Output Support**: mcpo now gracefully handles image outputs from MCP tools—returning them directly as binary image content so users can render or download visuals instantly, unlocking powerful new use cases like dynamic charts, AI art, and diagnostics through any standard HTTP client or browser.

## [0.0.6] - 2025-04-02

### Added

- 🔐 **CLI Auth with --api-key**: Secure your endpoints effortlessly with the new --api-key option, enabling basic API key authentication for instant protection without custom middleware or external auth systems—ideal for public or multi-agent deployments.
- 🌐 **Flexible CORS Access via --cors-allow-origins**: Unlock controlled cross-origin access with the new --cors-allow-origins CLI flag—perfect for integrating mcpo with frontend apps, remote UIs, or cloud dashboards while maintaining CORS security.

### Fixed

- 🧹 **Cleaner Proxy Output**: Dropped None arguments from proxy requests, resulting in reduced clutter and improved interoperability with servers expecting clean inputs—ensuring more reliable downstream performance with MCP tools.
