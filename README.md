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
