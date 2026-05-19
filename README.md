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

## Examples

```sh
./goodlinks links list --read false --search python --limit 20
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

By default, JSON API responses are converted to aligned tabular rows with a
header row. Columns are padded with tabs to common tab stops across the full
response:

- links default: `STARRED TITLE URL TAGS READAT`
- lists default: `ID`
- tags default: `TAG`
- highlights default: `CONTENT CREATEDAT`

Use `--json` to pretty-print the original JSON response. Use `--raw` for
non-JSON bodies such as article content and highlight exports, or when you
want the exact response body. Use `-0` to terminate tabular records with NUL
instead of newline.

Use `-O` with comma-separated lowercase column names to select tabular columns:

```sh
./goodlinks -O id,title,url links list
./goodlinks -O id,name lists list
./goodlinks -O id,content,note highlights list
```
