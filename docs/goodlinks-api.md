# GoodLinks API

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Request and Response Formats](#request-and-response-formats)
- [Authentication](#authentication)
- [Links](#links)
- [Lists](#lists)
- [Tags](#tags)
- [Highlights](#highlights)

## Overview

The GoodLinks API provides access to your local GoodLinks library. Use
it to build companion apps, extensions, or automation scripts that can
read and modify your links, tags, and highlights.

The API runs as a built-in web server on your computer and is designed
for trusted applications running on the same machine. All communication
happens over `localhost`, keeping your data secure and private.

**Note:** The API is available from GoodLinks 3.2.

## Getting Started

Before making API calls, you'll need to:

1. **Enable the API** in GoodLinks settings.
2. **Get the API token** from GoodLinks settings.

## Request and Response Formats

### Base URL

All API endpoints are prefixed with `/api/v1`. Combine this with the API
address:

```text
http://localhost:9428/api/v1
```

### HTTP Methods

The API follows REST conventions:

- `GET` - Retrieve resources (links, tags, etc.).
- `POST` - Create new resources.
- `PATCH` - Update resources.
- `DELETE` - Delete resources.

Using the wrong HTTP method returns `405 Method Not Allowed`.

### Request Headers

Include these headers in your requests:

- **Authorization**: `Bearer <token>` (required for all `/api/*`
  endpoints).
- **Content-Type**: `application/json` (required for requests with a
  body).

### Request Bodies

When sending data (POST, PATCH requests):

- Use UTF-8 encoded JSON.
- Unknown fields in the request body are ignored.
- If required fields are missing, the API returns `400 Bad Request` with
  details about what is missing.

**Example:**

```json
{
  "url": "https://example.com/article",
  "title": "Example Article"
}
```

### Response Format

Successful responses return JSON objects with resource data. Some
endpoints include pagination metadata:

- `hasMore` (boolean) - Whether there are more items available beyond
  the current page.

**Example success response:**

```json
{
  "data": [...],
  "hasMore": true
}
```

### Error Responses

When something goes wrong, you'll receive an error response with:

- `error` - A human-readable error message.
- `details` - (Optional) Additional information to help diagnose the
  issue.

**Example error response:**

```json
{
  "error": "Invalid request",
  "details": {
    "field": "url",
    "message": "URL is required"
  }
}
```

### Common Errors

The following errors can occur on any endpoint:

- **`400 Bad Request`** - Invalid request data (e.g., missing required
  fields, invalid parameter values, invalid date format, field too
  long).
- **`401 Unauthorized`** - Authentication token is missing or invalid.

### Timestamps

All date and time values use ISO-8601 format in UTC timezone:
`2025-11-11T15:04:05Z`.

## Authentication

The API uses token-based authentication to secure access to your
library. You'll need to include your API token with every request.

### Setting Up Authentication

Get the API credentials in GoodLinks settings:

- Go to Settings > API.
- Copy the API token.

**Important:** After changing the API token or API address, restart any
applications or scripts that use the API so they pick up the new values.

### Using Authentication

Include the API token in the `Authorization` header using the `Bearer`
scheme. Here are examples:

**Using curl:**

```bash
curl -H "Authorization: Bearer your-api-token" \
  http://localhost:9428/api/v1/links
```

**Using JavaScript (fetch):**

```javascript
fetch("http://localhost:9428/api/v1/links", {
  headers: {
    Authorization: "Bearer your-api-token",
  },
});
```

**Using Python (requests):**

```python
import requests

headers = {
    "Authorization": "Bearer your-api-token",
}

requests.get("http://localhost:9428/api/v1/links", headers=headers)
```

### Security Best Practices

- **Protect your token**: Treat your API token like a password. Never
  share it or commit it to version control.
- **Rotate tokens**: Regenerate your API token periodically, and
  immediately if you suspect it has been compromised.
- **Trust your apps**: Only use the API with applications you trust,
  since they'll have full access to your library.

### Authentication Errors

If your token is missing or incorrect, you'll receive a
`401 Unauthorized` response. Check that:

- Your API token matches what's shown in GoodLinks settings.
- The `Authorization` header is included in your request.
- The token is prefixed with `Bearer `, including the trailing space.

## Links

### Link Metadata

Links returned by the API include the following fields:

- **`id`** (string) - Unique identifier for the link.
- **`url`** (string) - The full URL of the saved link.
- **`title`** (string, nullable) - The title of the article or page.
- **`summary`** (string, nullable) - A brief summary or description of
  the content.
- **`author`** (string, nullable) - The author of the article, if
  available.
- **`tags`** (array of strings, nullable) - Tags associated with the
  link. Returns `null` if no tags are set.
- **`wordCount`** (integer, nullable) - Estimated number of words in
  the article content.
- **`starred`** (boolean) - Whether the link has been starred.
- **`highlighted`** (boolean) - Whether the link has any highlights.
- **`addedAt`** (string) - ISO-8601 timestamp indicating when the link
  was saved to the library.
- **`modifiedAt`** (string) - ISO-8601 timestamp indicating when the
  link was last modified.
- **`readAt`** (string, nullable) - ISO-8601 timestamp indicating when
  the link was marked as read.

**Example link object:**

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

### Get a Link by ID

Retrieve a single link by its ID.

**Endpoint:** `GET /api/v1/links/{id}`

**Path Parameters:**

- **`id`** (string, required) - The unique identifier of the link to
  retrieve.

**Response:**

Returns a single link object with all metadata fields.

**Errors:**

- `404 Not Found` - Link with the specified ID does not exist.

**Example Request:**

```bash
curl -H "Authorization: Bearer your-api-token" \
  http://localhost:9428/api/v1/links/abc123
```

**Example Response:**

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

### Get a Link by URL

Retrieve a single link by its URL. This is useful when you have the URL
but not the link ID.

**Endpoint:** `GET /api/v1/links`

**Query Parameters:**

- **`url`** (string, required) - The URL of the link to retrieve. Must
  be URL-encoded.

**Note:** When the `url` parameter is provided, this endpoint returns a
single link object. For retrieving multiple links, see "Search Links"
below.

**Response:**

Returns a single link object with all metadata fields, identical to the
"Get a Link by ID" endpoint.

**Errors:**

- `404 Not Found` - Link with the specified URL does not exist.

**Example Request:**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links?url=https%3A%2F%2Fexample.com%2Farticle"
```

### Get Current Link

Retrieve the link currently selected in GoodLinks.

**Endpoint:** `GET /api/v1/links/current`

**Response:**

Returns a single link object with all metadata fields, identical to the
"Get a Link by ID" endpoint.

**Errors:**

- `404 Not Found` - No link is currently selected in GoodLinks.

**Example Request:**

```bash
curl -H "Authorization: Bearer your-api-token" \
  http://localhost:9428/api/v1/links/current
```

### Get Links in List

Retrieve links from a specific main list with optional filtering and
pagination. Links are sorted by date added (newest first) by default.

**Endpoint:** `GET /api/v1/lists/{list}`

**Path Parameters:**

- **`list`** (string, required) - The main list to retrieve links
  from. Valid values:
  - `unread` - Links that haven't been read.
  - `read` - Links that have been read.
  - `starred` - Links that have been starred.
  - `untagged` - Links that have no tags.
  - `highlighted` - Links that have highlights.
  - `all` - All links in the library.

**Query Parameters:**

- **`search`** (string, optional) - Search text to filter links by
  title, summary, content, URL, and author.
- **`tag`** (string, optional) - Tag to filter by. This parameter can
  be specified multiple times. Only links with at least one of the
  specified tags will be returned. This parameter is ignored when
  `list=untagged`.
- **`includeRead`** (boolean, optional) - Whether to include read
  links in the results. Only relevant for `starred`, `untagged` and
  `highlighted` lists. Defaults to `false`.
- **`limit`** (integer, optional) - Maximum number of links to return
  per page. Must be between 1 and 1000. Defaults to `20` if not
  specified.
- **`offset`** (integer, optional) - Number of items to skip before
  returning results. Defaults to `0`.

**Response:**

Response format is identical to "Search Links".

**Errors:**

- `404 Not Found` - Invalid list type specified in the path.

**Example Request (Unread Links):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/lists/unread?limit=20"
```

**Example Request (Starred Links with Search):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/lists/starred?search=programming&includeRead=true&limit=10"
```

**Example Request (Tagged Links in Unread List):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/lists/unread?tag=technology&tag=programming&limit=50"
```

**Example Request (All Links with Pagination):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/lists/all?limit=20&offset=20"
```

### Search Links

Search for links across your entire library with advanced filtering and
sorting options. This endpoint searches through link titles, summaries,
content, URLs, and author names.

**Endpoint:** `GET /api/v1/links`

**Note:** This endpoint shares the same path as "Get a Link by URL".
When the `url` parameter is provided, it returns a single link. When
search parameters (like `search`, `tag`, `starred`, etc.) are provided
or no parameters are given, it returns a list of links matching the
search criteria.

**Query Parameters:**

- **`search`** (string, optional) - Search query text. Searches across
  title, summary, content, URL, and author.
- **`tag`** (string, optional) - Tag to filter by. This parameter can
  be specified multiple times. Only links with at least one of the
  specified tags will be returned.
- **`starred`** (boolean, optional) - Filter by starred status. `true`
  returns only starred links, `false` returns only unstarred links.
- **`read`** (boolean, optional) - Filter by read status. `true`
  returns only read links, `false` returns only unread links.
- **`tagged`** (boolean, optional) - Filter by whether links have
  tags. `true` returns only tagged links, `false` returns only untagged
  links.
- **`highlighted`** (boolean, optional) - Filter by whether links have
  highlights. `true` returns only links with highlights, `false` returns
  only links without highlights.
- **`wordCountMin`** (integer, optional) - Minimum word count to
  filter by.
- **`wordCountMax`** (integer, optional) - Maximum word count to
  filter by.
- **`addedAfter`** (string, optional) - ISO-8601 timestamp. Only
  return links added after this date.
- **`addedBefore`** (string, optional) - ISO-8601 timestamp. Only
  return links added before this date.
- **`readAfter`** (string, optional) - ISO-8601 timestamp. Only return
  links read after this date.
- **`readBefore`** (string, optional) - ISO-8601 timestamp. Only
  return links read before this date.
- **`sort`** (string, optional) - Sort order for results. Valid
  values:
  - `newestSaved` - Newest saved first (default)
  - `oldestSaved` - Oldest saved first
  - `newestRead` - Newest read first
  - `oldestRead` - Oldest read first
  - `shortest` - Shortest articles first
  - `longest` - Longest articles first
  - `titleA` - Title ascending (A-Z)
  - `titleZ` - Title descending (Z-A)
- **`limit`** (integer, optional) - Maximum number of links to return
  per page. Must be between 1 and 1000. Defaults to `20` if not
  specified.
- **`offset`** (integer, optional) - Number of items to skip before
  returning results. Defaults to `0`.

**Response:**

Returns an object containing:

- **`data`** (array) - Array of link objects matching the search
  criteria.
- **`hasMore`** (boolean) - Whether there are more links available
  beyond the current page.

**Example Request (Simple Text Search):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links?search=python&limit=20"
```

**Example Request (Search by Multiple Tags):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links?tag=technology&tag=programming&limit=20"
```

**Example Request (Advanced Search with Filters):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links?search=programming&tag=technology&tag=web&starred=true&read=false&sort=newestSaved&limit=10"
```

**Example Request (Date Range Search):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links?addedAfter=2025-01-01T00:00:00Z&addedBefore=2025-01-31T23:59:59Z&sort=oldestSaved"
```

**Example Request (Word Count Filter):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links?wordCountMin=1000&wordCountMax=5000&sort=longest"
```

**Example Response:**

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
    },
    {
      "id": "def456",
      "url": "https://example.com/another",
      "title": "Another Article",
      "summary": "Another summary.",
      "author": "Jane Smith",
      "tags": ["technology"],
      "wordCount": 800,
      "starred": true,
      "highlighted": true,
      "addedAt": "2025-01-14T08:15:00Z",
      "modifiedAt": "2025-01-14T08:15:00Z",
      "readAt": "2025-01-15T12:00:00Z"
    }
  ],
  "hasMore": true
}
```

### Add a Link

Add a new link to your library, or update an existing link if one with
the same URL already exists. The link will be created or updated with
the provided metadata, or GoodLinks will attempt to fetch metadata
automatically if not provided.

**Endpoint:** `POST /api/v1/links`

**Request Body:**

The request body must be a JSON object with the following fields:

- **`url`** (string, required) - The URL of the link to add. Must be a
  valid HTTP or HTTPS URL. Maximum length is 2000 characters.
- **`title`** (string, optional) - The title for the link. Maximum
  length is 200 characters. Newlines will be replaced with spaces and
  the text will be trimmed.
- **`summary`** (string, optional) - A summary or description for the
  link. Maximum length is 400 characters. Newlines will be replaced with
  spaces and the text will be trimmed.
- **`tags`** (array of strings, optional) - Tags to associate with the
  link. Each tag must be a non-empty string with a maximum length of 100
  characters.
- **`read`** (boolean, optional) - Whether to mark the link as read
  immediately. Defaults to `false`. If `true`, the link's `readAt`
  timestamp will be set to the current time.
- **`starred`** (boolean, optional) - Whether to add the link to the
  starred list. Defaults to `false`.
- **`addedAt`** (string, optional) - ISO-8601 timestamp indicating
  when the link was saved. Only used when creating a new link. If not
  provided, defaults to the current time. If provided, must not be in
  the future (will be clamped to current time). When updating an
  existing link, this field is ignored.

**Response:**

Returns the created or updated link object with all metadata fields,
including the `id`. If a link with the same URL already exists, it will
be updated with the provided fields. Fields not provided in the request
will preserve their existing values (except for `addedAt`, which is only
set when creating a new link).

**Example Request:**

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

**Example Request (Minimal):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}' \
  http://localhost:9428/api/v1/links
```

**Example Request (With Custom Date):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "title": "Example Article",
    "addedAt": "2025-01-15T10:30:00Z"
  }' \
  http://localhost:9428/api/v1/links
```

**Example Response:**

```json
{
  "id": "abc123",
  "url": "https://example.com/article",
  "title": "Example Article Title",
  "summary": "This is a brief summary of the article.",
  "author": "John Doe",
  "tags": ["technology", "programming"],
  "starred": false,
  "highlighted": false,
  "addedAt": "2025-01-15T10:30:00Z",
  "modifiedAt": "2025-01-15T10:30:00Z",
  "readAt": "2025-01-16T14:20:00Z"
}
```

### Edit a Link

Update an existing link's metadata. Only the fields provided in the
request will be updated; all other fields will remain unchanged.

**Endpoint:** `PATCH /api/v1/links/{id}`

**Path Parameters:**

- **`id`** (string, required) - The ID of the link to update.

**Request Body:**

The request body must be a JSON object with the following optional
fields:

- **`title`** (string, optional) - The title for the link. Maximum
  length is 200 characters. Newlines will be replaced with spaces and
  the text will be trimmed.
- **`summary`** (string, optional) - A summary or description for the
  link. Maximum length is 400 characters. Newlines will be replaced with
  spaces and the text will be trimmed.
- **`starred`** (boolean, optional) - Whether to add the link to the
  starred list or remove it.
- **`read`** (boolean, optional) - Whether to mark the link as read or
  unread. If set to `true`, the link's `readAt` timestamp will be set to
  the current time. If set to `false`, the `readAt` timestamp will be
  cleared.
- **`addedTags`** (array of strings, optional) - Tags to add to the
  link's existing tags. Tags that are already present are not
  duplicated. Each tag must be a non-empty string with a maximum length
  of 100 characters.
- **`removedTags`** (array of strings, optional) - Tags to remove from
  the link's existing tags. Tags that don't exist are ignored.
- **`tags`** (array of strings, optional) - Replace all tags on the
  link with the specified tags. If an empty array is provided, all tags
  are removed. Each tag must be a non-empty string with a maximum length
  of 100 characters. Note: If `tags` is provided, `addedTags` and
  `removedTags` will be ignored.

**Response:**

Returns the updated link object with all metadata fields.

**Errors:**

- `404 Not Found` - The link ID does not exist.

**Example Request (Update Title and Summary):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Article Title",
    "summary": "Updated summary of the article."
  }' \
  http://localhost:9428/api/v1/links/abc123
```

**Example Request (Mark as Read and Starred):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "read": true,
    "starred": true
  }' \
  http://localhost:9428/api/v1/links/abc123
```

**Example Request (Add Tags):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "addedTags": ["technology", "programming"]
  }' \
  http://localhost:9428/api/v1/links/abc123
```

**Example Request (Remove Tags):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "removedTags": ["programming"]
  }' \
  http://localhost:9428/api/v1/links/abc123
```

**Example Request (Replace All Tags):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "tags": ["design", "ui"]
  }' \
  http://localhost:9428/api/v1/links/abc123
```

**Example Response:**

```json
{
  "id": "abc123",
  "url": "https://example.com/article",
  "title": "Updated Article Title",
  "summary": "Updated summary of the article.",
  "author": "John Doe",
  "tags": ["technology", "programming"],
  "starred": true,
  "highlighted": false,
  "addedAt": "2025-01-15T10:30:00Z",
  "modifiedAt": "2025-01-16T15:45:00Z",
  "readAt": "2025-01-16T15:45:00Z"
}
```

### Delete Links

Delete one or more links. Links are moved to trash and can be recovered.

**Endpoint:** `DELETE /api/v1/links`

**Query Parameters:**

- **`id`** (string, required) - Link ID to delete. This parameter can
  be specified multiple times. Must contain at least one link ID.

**Response:**

Returns `204 No Content` with no response body.

**Errors:**

- `404 Not Found` - One or more link IDs do not exist (only returned
  if all link IDs are invalid).

**Example Request (Delete Single Link):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X DELETE \
  "http://localhost:9428/api/v1/links?id=abc123"
```

**Example Request (Delete Multiple Links):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X DELETE \
  "http://localhost:9428/api/v1/links?id=abc123&id=def456&id=ghi789"
```

### Get Article Content

Retrieve the article content of a link in HTML, plaintext, or markdown
format.

**Endpoint:** `GET /api/v1/links/{id}/content`

**Path Parameters:**

- **`id`** (string, required) - The unique identifier of the link.

**Query Parameters:**

- **`format`** (string, optional) - The format of the content to
  return. Valid values:
  - `html` - Returns the article content as HTML (default).
  - `plaintext` - Returns the article content as plain text.
  - `markdown` - Returns the article content as Markdown.
- **`autoDownload`** (boolean, optional) - Defaults to `true`. Set it
  to `false` to skip downloading and only return already cached article
  content.

**Response:**

Returns the article content in the requested format. The response
content type depends on the format:

- `html` - `text/html`.
- `plaintext` - `text/plain`.
- `markdown` - `text/markdown`.

**Errors:**

- `404 Not Found` - Link with the specified ID does not exist or the
  link has no content available.

**Example Request (HTML Format):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links/abc123/content?format=html"
```

**Example Request (Disable Auto-Download):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links/abc123/content?format=html&autoDownload=false"
```

**Example Request (Plaintext Format):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links/abc123/content?format=plaintext"
```

**Example Request (Markdown Format):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links/abc123/content?format=markdown"
```

## Lists

### Get Lists

Retrieve all visible lists in your library.

**Endpoint:** `GET /api/v1/lists`

**Response:**

Returns an array of list objects. Each object contains:

- **`id`** (string) - Unique identifier for the list.
- **`name`** (string) - The name of the list.

**Example Request:**

```bash
curl -H "Authorization: Bearer your-api-token" \
  http://localhost:9428/api/v1/lists
```

**Example Response:**

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

## Tags

### Get Tags

Retrieve all tags in your library. Only tags that have at least one link
are returned.

**Endpoint:** `GET /api/v1/tags`

**Response:**

Returns an array of tags (strings). For hierarchical tags, this includes
the full path (e.g., `technology/programming`).

**Example Request:**

```bash
curl -H "Authorization: Bearer your-api-token" \
  http://localhost:9428/api/v1/tags
```

**Example Response:**

```json
["design", "technology", "technology/programming"]
```

## Highlights

### Highlight Metadata

Highlights returned by the API include the following fields:

- **`id`** (string) - Unique identifier for the highlight.
- **`linkID`** (string) - The ID of the link this highlight belongs
  to.
- **`content`** (string) - The highlighted text content in plain text
  format.
- **`markdownContent`** (string) - The highlighted text content in
  markdown format.
- **`note`** (string, nullable) - An optional note or annotation
  associated with the highlight.
- **`createdAt`** (string) - ISO-8601 timestamp indicating when the
  highlight was created.

**Example highlight object:**

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

### Search Highlights

Search for highlights across your library. This endpoint searches
through highlight content and notes, and supports filtering and sorting
options.

**Endpoint:** `GET /api/v1/highlights`

**Query Parameters:**

- **`q`** (string, optional) - Search query text. Searches through
  highlight content and notes.
- **`linkID`** (string, optional) - Filter highlights by link ID. Only
  highlights belonging to the specified link will be returned.
- **`content`** (string, optional) - Filter highlights by content
  containing this text.
- **`note`** (string, optional) - Filter highlights by note containing
  this text.
- **`createdAfter`** (string, optional) - ISO-8601 timestamp. Only
  return highlights created after this date.
- **`createdBefore`** (string, optional) - ISO-8601 timestamp. Only
  return highlights created before this date.
- **`sort`** (string, optional) - Sort order for results. Valid
  values:
  - `newest` - Newest highlights first (default)
  - `oldest` - Oldest highlights first
  - `linkID` - Sort by link ID
  - `content` - Sort by content alphabetically
  - `note` - Sort by note alphabetically
- **`limit`** (integer, optional) - Maximum number of highlights to
  return per page. Must be between 1 and 1000. Defaults to `20` if not
  specified.
- **`offset`** (integer, optional) - Number of items to skip before
  returning results. Defaults to `0`.

**Response:**

Returns an object containing:

- **`data`** (array) - Array of highlight objects matching the search
  criteria.
- **`hasMore`** (boolean) - Whether there are more highlights
  available beyond the current page.

**Example Request (Simple Text Search):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/highlights?q=important&limit=20"
```

**Example Request (Filter by Link):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/highlights?linkID=abc123&sort=newest"
```

**Example Request (Date Range Search):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/highlights?createdAfter=2025-01-01T00:00:00Z&createdBefore=2025-01-31T23:59:59Z&sort=oldest"
```

**Example Request (Advanced Search):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/highlights?q=programming&linkID=abc123&note=insight&sort=newest&limit=10"
```

**Example Response:**

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
    },
    {
      "id": "highlight456",
      "linkID": "abc123",
      "content": "Another highlighted section with programming concepts.",
      "markdownContent": "Another highlighted section with `programming` concepts.",
      "note": null,
      "createdAt": "2025-01-14T08:15:00Z"
    }
  ],
  "hasMore": true
}
```

### Edit a Highlight

Update an existing highlight's metadata. Only the fields provided in the
request will be updated; all other fields will remain unchanged.

**Endpoint:** `PATCH /api/v1/highlights/{id}`

**Path Parameters:**

- **`id`** (string, required) - The ID of the highlight to update.

**Request Body:**

The request body must be a JSON object with the following optional
field:

- **`note`** (string, optional) - The note for the highlight.

**Response:**

Returns the updated highlight object with all metadata fields.

**Errors:**

- `404 Not Found` - The highlight ID does not exist.

**Example Request (Set Note):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "note": "This is an important insight about the highlighted text."
  }' \
  http://localhost:9428/api/v1/highlights/highlight123
```

**Example Request (Clear Note):**

```bash
curl -H "Authorization: Bearer your-api-token" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "note": ""
  }' \
  http://localhost:9428/api/v1/highlights/highlight123
```

**Example Response:**

```json
{
  "id": "highlight123",
  "linkID": "abc123",
  "content": "This is an important quote from the article.",
  "markdownContent": "This is an **important** quote from the article.",
  "note": "This is an important insight about the highlighted text.",
  "createdAt": "2025-01-15T10:30:00Z"
}
```

### Export Highlights

Export highlights from a link using the export format template
configured in GoodLinks settings.

**Endpoint:** `GET /api/v1/links/{id}/highlights/export`

**Path Parameters:**

- **`id`** (string, required) - The unique identifier of the link.

**Response:**

Returns the highlights export content as Markdown. The response content
type is `text/markdown`. The format follows your configured export
template, which can be customized using Mustache templating.

**Errors:**

- `404 Not Found` - Link with the specified ID does not exist or the
  link has no highlights.

**Example Request:**

```bash
curl -H "Authorization: Bearer your-api-token" \
  "http://localhost:9428/api/v1/links/abc123/highlights/export"
```
