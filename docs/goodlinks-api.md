# GoodLinks API Specification

GoodLinks exposes a local HTTP API for reading and modifying the
library stored by the GoodLinks app. The API is intended for trusted
applications, extensions, and automation scripts running on the same
computer as GoodLinks.

The API is available in GoodLinks 3.2 and later.

## Contents

- [Service Model](#service-model)
- [Authentication](#authentication)
- [Protocol Conventions](#protocol-conventions)
- [Data Types](#data-types)
- [Schemas](#schemas)
- [Common Query Parameters](#common-query-parameters)
- [Endpoints](#endpoints)
- [Errors](#errors)
- [Examples](#examples)

## Service Model

### Origin

The API server is built into GoodLinks and listens on a fixed localhost
address. The base URL is:

```text
http://localhost:9428/api/v1
```

All endpoints documented in this specification are relative to
`/api/v1`.

### Availability

Clients must treat the API as available only while GoodLinks is running
and the API is enabled in GoodLinks settings.

Before making requests, a user must:

1. Enable the API in GoodLinks settings.
2. Copy the API token from GoodLinks settings.

If the API token is changed, clients should reload their configuration
before sending additional requests.

### Transport

The API uses HTTP over localhost. It is designed for same-machine
clients and does not define a remote access or multi-user authorization
model.

## Authentication

Every request to an `/api/*` endpoint must include an API token in the
`Authorization` header using the Bearer scheme:

```http
Authorization: Bearer <token>
```

Requests with a missing, malformed, or invalid token fail with
`401 Unauthorized`.

Clients should treat the token as a password. Do not commit it to source
control, log it, or expose it to untrusted processes.

## Protocol Conventions

### HTTP Methods

The API uses the following methods:

| Method | Semantics |
| --- | --- |
| `GET` | Retrieve resources or derived content. |
| `POST` | Create a resource or perform an upsert operation. |
| `PATCH` | Update selected fields on an existing resource. |
| `DELETE` | Delete one or more resources. |

If an endpoint path exists but the method is unsupported, the server
returns `405 Method Not Allowed`.

### Request Bodies

Request bodies, when required, must be UTF-8 encoded JSON objects and
must include:

```http
Content-Type: application/json
```

Unknown fields in JSON request bodies are ignored. Missing required
fields, invalid field types, invalid parameter values, invalid date
formats, and values that exceed documented limits fail with
`400 Bad Request`.

### Response Bodies

JSON responses use UTF-8 encoded JSON. Endpoints that return article
content or exported highlights return a non-JSON text body as documented
for the endpoint.

Successful `DELETE` requests return `204 No Content` with no response
body.

### Timestamps

All timestamp values are ISO 8601 strings in UTC, for example:

```text
2025-11-11T15:04:05Z
```

Timestamp query parameters and request fields must use this format.

### Booleans

Boolean query parameters accept `true` or `false`.

### Pagination

List endpoints use offset pagination:

| Parameter | Type | Default | Constraints |
| --- | --- | --- | --- |
| `limit` | integer | `20` | Minimum `1`, maximum `1000`. |
| `offset` | integer | `0` | Number of matching items to skip. |

Paginated JSON responses have this envelope:

```json
{
  "data": [],
  "hasMore": false
}
```

`hasMore` is `true` when additional matching items are available after
the current page.

## Data Types

| Type | Definition |
| --- | --- |
| `ID` | String identifier assigned by GoodLinks. |
| `URL` | HTTP or HTTPS URL. Link creation accepts URLs up to 2000 characters. |
| `Timestamp` | ISO 8601 UTC timestamp. |
| `Tag` | Non-empty string up to 100 characters. Hierarchical tags use `/`, such as `technology/programming`. |
| `Nullable<T>` | Either a value of type `T` or JSON `null`. |

## Schemas

### Link

Represents a saved link in the GoodLinks library.

| Field | Type | Nullable | Description |
| --- | --- | --- | --- |
| `id` | string | no | Unique link identifier. |
| `url` | string | no | Full saved URL. |
| `title` | string | yes | Article or page title. |
| `summary` | string | yes | Summary or description. |
| `author` | string | yes | Author name when available. |
| `tags` | array of strings | yes | Tags associated with the link. Returns `null` when no tags are set. |
| `wordCount` | integer | yes | Estimated article word count. |
| `starred` | boolean | no | Whether the link is starred. |
| `highlighted` | boolean | no | Whether the link has at least one highlight. |
| `addedAt` | string | no | Time the link was saved. |
| `modifiedAt` | string | no | Time the link was last modified. |
| `readAt` | string | yes | Time the link was marked read. `null` means unread. |

Example:

```json
{
  "id": "abc123",
  "url": "https://example.com/article",
  "title": "Example Article Title",
  "summary": "This is a brief summary of the article.",
  "author": "John Doe",
  "tags": ["technology", "programming"],
  "wordCount": 1250,
  "starred": false,
  "highlighted": false,
  "addedAt": "2025-01-15T10:30:00Z",
  "modifiedAt": "2025-01-15T10:30:00Z",
  "readAt": "2025-01-16T14:20:00Z"
}
```

### Link List

Represents a visible GoodLinks list.

| Field | Type | Nullable | Description |
| --- | --- | --- | --- |
| `id` | string | no | List identifier. |
| `name` | string | no | Display name. |

### Highlight

Represents a highlight attached to a link.

| Field | Type | Nullable | Description |
| --- | --- | --- | --- |
| `id` | string | no | Unique highlight identifier. |
| `linkID` | string | no | ID of the link that owns the highlight. |
| `content` | string | no | Highlighted text as plain text. |
| `markdownContent` | string | no | Highlighted text as Markdown. |
| `note` | string | yes | Optional annotation. |
| `createdAt` | string | no | Time the highlight was created. |

Example:

```json
{
  "id": "highlight123",
  "linkID": "abc123",
  "content": "This is an important quote from the article.",
  "markdownContent": "This is an **important** quote from the article.",
  "note": "Key insight",
  "createdAt": "2025-01-15T10:30:00Z"
}
```

### Error

Error responses are JSON objects.

| Field | Type | Nullable | Description |
| --- | --- | --- | --- |
| `error` | string | no | Human-readable error message. |
| `details` | any | yes | Optional diagnostic details. |

Example:

```json
{
  "error": "Invalid request",
  "details": {
    "field": "url",
    "message": "URL is required"
  }
}
```

## Common Query Parameters

### Link Search Parameters

These parameters are used by `GET /links` and, where noted, by
`GET /lists/{list}`.

| Parameter | Type | Repeated | Description |
| --- | --- | --- | --- |
| `search` | string | no | Searches title, summary, content, URL, and author. |
| `tag` | string | yes | Returns links with at least one of the specified tags. Ignored for `GET /lists/untagged`. |
| `starred` | boolean | no | `true` returns starred links; `false` returns unstarred links. Only supported by `GET /links`. |
| `read` | boolean | no | `true` returns read links; `false` returns unread links. Only supported by `GET /links`. |
| `tagged` | boolean | no | `true` returns tagged links; `false` returns untagged links. Only supported by `GET /links`. |
| `highlighted` | boolean | no | `true` returns links with highlights; `false` returns links without highlights. Only supported by `GET /links`. |
| `wordCountMin` | integer | no | Minimum word count. Only supported by `GET /links`. |
| `wordCountMax` | integer | no | Maximum word count. Only supported by `GET /links`. |
| `addedAfter` | timestamp | no | Returns links added after this timestamp. Only supported by `GET /links`. |
| `addedBefore` | timestamp | no | Returns links added before this timestamp. Only supported by `GET /links`. |
| `readAfter` | timestamp | no | Returns links read after this timestamp. Only supported by `GET /links`. |
| `readBefore` | timestamp | no | Returns links read before this timestamp. Only supported by `GET /links`. |
| `sort` | string | no | Sort order. Only supported by `GET /links`. |
| `limit` | integer | no | Page size. |
| `offset` | integer | no | Page offset. |

Valid `sort` values for `GET /links`:

| Value | Sort order |
| --- | --- |
| `newestSaved` | Newest saved first. This is the default. |
| `oldestSaved` | Oldest saved first. |
| `newestRead` | Newest read first. |
| `oldestRead` | Oldest read first. |
| `shortest` | Shortest articles first. |
| `longest` | Longest articles first. |
| `titleA` | Title ascending, A-Z. |
| `titleZ` | Title descending, Z-A. |

### Highlight Search Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `q` | string | Searches highlight content and notes. |
| `linkID` | string | Returns highlights belonging to a link. |
| `content` | string | Returns highlights whose content contains this text. |
| `note` | string | Returns highlights whose note contains this text. |
| `createdAfter` | timestamp | Returns highlights created after this timestamp. |
| `createdBefore` | timestamp | Returns highlights created before this timestamp. |
| `sort` | string | Highlight sort order. |
| `limit` | integer | Page size. |
| `offset` | integer | Page offset. |

Valid highlight `sort` values:

| Value | Sort order |
| --- | --- |
| `newest` | Newest highlights first. This is the default. |
| `oldest` | Oldest highlights first. |
| `linkID` | Sort by link ID. |
| `content` | Sort by content alphabetically. |
| `note` | Sort by note alphabetically. |

## Endpoints

### `GET /links`

Retrieves links. The response shape depends on the query parameters:

- If `url` is provided, the endpoint returns a single `Link`.
- If `url` is omitted, the endpoint returns a paginated list of `Link`
  objects.

#### Get Link by URL

Query parameters:

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | string | yes | URL-encoded URL of the link to retrieve. |

Response:

- `200 OK` with a `Link`.

Errors:

- `404 Not Found` if no link with the specified URL exists.

#### Search Links

Query parameters:

- All [Link Search Parameters](#link-search-parameters), except `url`.

Response:

- `200 OK` with a paginated link envelope:

```json
{
  "data": [
    {
      "id": "abc123",
      "url": "https://example.com/article",
      "title": "Example Article Title",
      "summary": "This is a brief summary of the article.",
      "author": "John Doe",
      "tags": ["technology", "programming"],
      "wordCount": 1250,
      "starred": false,
      "highlighted": false,
      "addedAt": "2025-01-15T10:30:00Z",
      "modifiedAt": "2025-01-15T10:30:00Z",
      "readAt": null
    }
  ],
  "hasMore": true
}
```

### `POST /links`

Creates a link or updates an existing link with the same URL.

If no metadata is supplied, GoodLinks attempts to fetch metadata
automatically. When the URL already exists, fields supplied in the
request update the existing link; omitted fields preserve existing
values. `addedAt` is only used when creating a new link.

Request body:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | string | yes | HTTP or HTTPS URL. Maximum 2000 characters. |
| `title` | string | no | Link title. Maximum 200 characters. Newlines are replaced with spaces and surrounding whitespace is trimmed. |
| `summary` | string | no | Link summary. Maximum 400 characters. Newlines are replaced with spaces and surrounding whitespace is trimmed. |
| `tags` | array of strings | no | Tags to associate with the link. Each tag must be non-empty and at most 100 characters. |
| `read` | boolean | no | Marks the link read when `true`. Defaults to `false`. |
| `starred` | boolean | no | Sets starred state. Defaults to `false`. |
| `addedAt` | timestamp | no | Save time for a new link. Defaults to the current time. Future values are clamped to the current time. Ignored when updating an existing link. |

Response:

- `200 OK` with the created or updated `Link`.

### `GET /links/current`

Retrieves the link currently selected in GoodLinks.

Response:

- `200 OK` with a `Link`.

Errors:

- `404 Not Found` if no link is currently selected.

### `GET /links/{id}`

Retrieves a link by ID.

Path parameters:

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | string | Link ID. |

Response:

- `200 OK` with a `Link`.

Errors:

- `404 Not Found` if the link does not exist.

### `PATCH /links/{id}`

Updates selected metadata fields on a link.

Path parameters:

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | string | Link ID. |

Request body:

| Field | Type | Description |
| --- | --- | --- |
| `title` | string | Link title. Maximum 200 characters. Newlines are replaced with spaces and surrounding whitespace is trimmed. |
| `summary` | string | Link summary. Maximum 400 characters. Newlines are replaced with spaces and surrounding whitespace is trimmed. |
| `starred` | boolean | Sets starred state. |
| `read` | boolean | `true` sets `readAt` to the current time. `false` clears `readAt`. |
| `addedTags` | array of strings | Tags to add to the existing tag set. Existing tags are not duplicated. |
| `removedTags` | array of strings | Tags to remove from the existing tag set. Missing tags are ignored. |
| `tags` | array of strings | Replaces all tags. An empty array removes all tags. If provided, `addedTags` and `removedTags` are ignored. |

Response:

- `200 OK` with the updated `Link`.

Errors:

- `404 Not Found` if the link does not exist.

### `DELETE /links`

Deletes one or more links. Deleted links are moved to trash and can be
recovered.

Query parameters:

| Parameter | Type | Repeated | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | string | yes | yes | Link ID to delete. At least one ID is required. |

Response:

- `204 No Content`.

Errors:

- `404 Not Found` if all supplied link IDs are invalid.

### `GET /links/{id}/content`

Retrieves cached or downloaded article content for a link.

Path parameters:

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | string | Link ID. |

Query parameters:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `format` | string | `html` | Content format. Valid values are `html`, `plaintext`, and `markdown`. |
| `autoDownload` | boolean | `true` | When `false`, GoodLinks returns only already cached article content. |

Response:

| `format` | Status | Content-Type | Body |
| --- | --- | --- | --- |
| `html` | `200 OK` | `text/html` | Article HTML. |
| `plaintext` | `200 OK` | `text/plain` | Article plain text. |
| `markdown` | `200 OK` | `text/markdown` | Article Markdown. |

Errors:

- `404 Not Found` if the link does not exist or no content is
  available.

### `GET /lists`

Retrieves visible GoodLinks lists.

Response:

- `200 OK` with an array of `Link List` objects.

Example:

```json
[
  {
    "id": "all",
    "name": "All"
  },
  {
    "id": "starred",
    "name": "Starred"
  }
]
```

### `GET /lists/{list}`

Retrieves links from a main list. Links are sorted by date added,
newest first.

Path parameters:

| Parameter | Type | Description |
| --- | --- | --- |
| `list` | string | Main list identifier. |

Valid list identifiers:

| Value | Description |
| --- | --- |
| `unread` | Links that have not been read. |
| `read` | Links that have been read. |
| `starred` | Links that have been starred. |
| `untagged` | Links with no tags. |
| `highlighted` | Links with highlights. |
| `all` | All links in the library. |

Query parameters:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `search` | string | none | Searches title, summary, content, URL, and author. |
| `tag` | string | none | Repeatable. Returns links with at least one supplied tag. Ignored when `list` is `untagged`. |
| `includeRead` | boolean | `false` | Includes read links for the `starred`, `untagged`, and `highlighted` lists. |
| `limit` | integer | `20` | Page size. Minimum `1`, maximum `1000`. |
| `offset` | integer | `0` | Page offset. |

Response:

- `200 OK` with the same paginated link envelope used by
  `GET /links`.

Errors:

- `404 Not Found` if `list` is not a valid list identifier.

### `GET /tags`

Retrieves all tags that have at least one link.

Response:

- `200 OK` with an array of strings.

Example:

```json
["design", "technology", "technology/programming"]
```

### `GET /highlights`

Searches highlights across the library.

Query parameters:

- All [Highlight Search Parameters](#highlight-search-parameters).

Response:

- `200 OK` with a paginated highlight envelope:

```json
{
  "data": [
    {
      "id": "highlight123",
      "linkID": "abc123",
      "content": "This is an important quote from the article.",
      "markdownContent": "This is an **important** quote from the article.",
      "note": "Key insight",
      "createdAt": "2025-01-15T10:30:00Z"
    }
  ],
  "hasMore": true
}
```

### `PATCH /highlights/{id}`

Updates a highlight.

Path parameters:

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | string | Highlight ID. |

Request body:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `note` | string | no | Highlight note. Use an empty string to clear the note. |

Response:

- `200 OK` with the updated `Highlight`.

Errors:

- `404 Not Found` if the highlight does not exist.

### `GET /links/{id}/highlights/export`

Exports highlights from a link using the export format template
configured in GoodLinks settings.

Path parameters:

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | string | Link ID. |

Response:

- `200 OK`
- `Content-Type: text/markdown`
- Body contains the rendered Markdown export. The format follows the
  user's configured Mustache export template.

Errors:

- `404 Not Found` if the link does not exist or the link has no
  highlights.

## Errors

### Common Status Codes

| Status | Meaning |
| --- | --- |
| `400 Bad Request` | The request is syntactically invalid or contains invalid data. |
| `401 Unauthorized` | The API token is missing, malformed, or invalid. |
| `404 Not Found` | The requested resource, list, content, or export does not exist. |
| `405 Method Not Allowed` | The endpoint exists, but the HTTP method is not supported. |

### Validation Failures

The server returns `400 Bad Request` for invalid request data, including:

- Missing required request fields.
- Invalid JSON.
- Invalid field types.
- Invalid query parameter values.
- Invalid timestamp formats.
- URL values that are not HTTP or HTTPS URLs.
- Values that exceed documented length limits.
- `limit` values outside the range `1...1000`.

## Examples

### Search Unread Links

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links?search=python&read=false&limit=20"
```

### Get a Link by URL

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links?url=https%3A%2F%2Fexample.com%2Farticle"
```

### Add a Link

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "title": "Example Article",
    "summary": "This is an example article about something interesting.",
    "tags": ["technology", "programming"],
    "starred": false,
    "read": false
  }' \
  http://localhost:9428/api/v1/links
```

### Update Link Tags

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "addedTags": ["technology"],
    "removedTags": ["draft"]
  }' \
  http://localhost:9428/api/v1/links/abc123
```

### Replace Link Tags

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "tags": ["design", "ui"]
  }' \
  http://localhost:9428/api/v1/links/abc123
```

### Delete Multiple Links

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X DELETE \
  "http://localhost:9428/api/v1/links?id=abc123&id=def456&id=ghi789"
```

### Retrieve Article Markdown

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links/abc123/content?format=markdown"
```

### Search Highlights

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/highlights?q=important&sort=newest&limit=20"
```

### Update a Highlight Note

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "note": "This is an important insight about the highlighted text."
  }' \
  http://localhost:9428/api/v1/highlights/highlight123
```

### Export Link Highlights

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links/abc123/highlights/export"
```
