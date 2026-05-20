# goodlinks-cli

A zsh CLI for the local GoodLinks HTTP API described in
[`docs/goodlinks-api.md`](docs/goodlinks-api.md).

## Requirements

- `zsh`
- `curl`
- `jq`
- GoodLinks 3.2 or later with the API enabled

## Setup

```sh
chmod +x ./goodlinks
./goodlinks config set-token "your-api-token"
```

You can also avoid writing a config file:

```sh
GOODLINKS_TOKEN="your-api-token" ./goodlinks links list
```

The default base URL is `http://localhost:9428/api/v1`. Override it with
`GOODLINKS_BASE_URL` or `--base-url`.

## Proxy mode

For agent or automation workflows, you can keep the GoodLinks API token outside
the agent sandbox by running a trusted local proxy that injects the
`Authorization: Bearer <token>` header. Point `goodlinks` at the proxy and use
`--no-auth` so the CLI does not read a token or send an authorization header:

```sh
GOODLINKS_TOKEN="your-api-token" caddy run --config Caddyfile
```

```sh
./goodlinks --no-auth --base-url http://127.0.0.1:19428/api/v1 links list --read false
```

You can also enable tokenless mode with an environment variable:

```sh
GOODLINKS_NO_AUTH=1 GOODLINKS_BASE_URL=http://127.0.0.1:19428/api/v1 ./goodlinks tags list
```

The included `Caddyfile` forwards requests to GoodLinks at
`http://localhost:9428/api/v1` and adds the API token. It does not enforce
read-only access or an endpoint allowlist. Only use `--no-auth` with a proxy
you trust.

## Examples

```sh
./goodlinks links list --read false --search python --limit 20
./goodlinks --no-auth --base-url http://127.0.0.1:19428/api/v1 links list --read false
./goodlinks -O id,title,url links list --read false
./goodlinks -O id links list --read false | tail -n +2 | cut -f1
./goodlinks -0 -O id links list --read false | cut -z -f1 | tail -z -n +2 | xargs -0 -n1 echo
./goodlinks --json links list --read false
./goodlinks links get --id abc123
./goodlinks links get-url --url "https://example.com/article"
./goodlinks links add --url "https://example.com/article" --tag technology --starred true
./goodlinks links update --id abc123 --add-tag programming --remove-tag draft
./goodlinks links delete --id abc123 --id def456
./goodlinks --raw links content --id abc123 --format markdown

./goodlinks lists list
./goodlinks lists get --list starred --include-read true

./goodlinks tags list

./goodlinks highlights list --q important --sort newest
./goodlinks highlights update --id highlight123 --note "Key insight"
./goodlinks --raw highlights export --link-id abc123
```

Run `./goodlinks --help` for the complete command surface.

## Output

By default, JSON API responses are converted to tabular rows with a header row.
When writing to a terminal, columns are separated with ` │ ` and long values
are shortened to keep each row on one line. When writing to a pipe or file,
columns are padded with tabs to common tab stops across the full response:
Terminal output includes a horizontal ruler below the header row.
Terminal column headers are never truncated; if the requested columns cannot
fit, the command exits with a terminal-too-narrow error.
In terminal link output, the URL column is proportionally capped so title text
keeps priority while wider terminals still show more of each URL.
Timestamp columns shorten date-first as space tightens, down to `YYMMDD`.

- links default: `STARRED TITLE URL TAGS READAT`
- lists default: `ID`
- tags default: `TAG`
- highlights default: `CONTENT CREATEDAT`

Use `--json` to pretty-print the original JSON response. Use `--raw` for
non-JSON bodies such as article content and highlight exports, or when you
want the exact response body. Use `-0` to terminate tabular records with NUL
instead of newline.

Default output omits columns that have no values in the current response. Use
`-O` to keep specific columns even when their values are empty.

Use `-O` with comma-separated lowercase column names to select tabular columns:

```sh
./goodlinks -O id,title,url links list
./goodlinks -O id,name lists list
./goodlinks -O id,content,note highlights list
```
