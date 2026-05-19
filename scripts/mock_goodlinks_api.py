#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


def link(
    *,
    id: str = "a",
    url: str = "https://example.com/a",
    title: str = "A",
    starred: bool = True,
    read_at: str | None = "2025-01-15T10:30:00Z",
    tags: list[str] | None = None,
) -> dict:
    return {
        "id": id,
        "url": url,
        "title": title,
        "starred": starred,
        "readAt": read_at,
        "tags": tags if tags is not None else ["one"],
    }


def response_for(path: str, scenario: str) -> object:
    parsed = urlparse(path)

    if parsed.path.endswith("/highlights"):
        return {
            "data": [
                {
                    "id": "h1",
                    "linkID": "a",
                    "content": (
                        "This is a very long highlighted passage that should "
                        "be shortened to fit in a narrow terminal window."
                    ),
                    "note": "",
                    "createdAt": "2025-01-15T10:30:00Z",
                }
            ],
            "hasMore": False,
        }

    if parsed.path.endswith("/lists"):
        return [{"id": "all", "name": "All"}, {"id": "starred", "name": "Starred"}]

    if parsed.path.endswith("/tags"):
        return ["one", "two"]

    if scenario == "empty-columns":
        return {
            "data": [
                link(id="a", title="A", starred=False, read_at=None, tags=[]),
                link(id="b", url="https://example.com/b", title="B", starred=False, read_at=None, tags=[]),
            ],
            "hasMore": False,
        }

    if scenario == "long":
        return {
            "data": [
                link(
                    url="https://www.example.com/a/very/long/path/that/should/expand/on/wide/terminals",
                    title="A much longer article title that should still keep reasonable priority over URL",
                    tags=["technology", "swift"],
                )
            ],
            "hasMore": False,
        }

    if scenario == "short-title-long-url":
        return {
            "data": [
                link(
                    url="https://www.example.com/a/very/long/path/that/can/use/extra/space/when/title/fits",
                    title="Short title",
                    tags=["technology"],
                )
            ],
            "hasMore": False,
        }

    return {"data": [link()], "hasMore": False}


class Handler(BaseHTTPRequestHandler):
    scenario = "default"

    def do_GET(self) -> None:
        body = json.dumps(response_for(self.path, self.scenario)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        self.do_GET()

    def do_PATCH(self) -> None:
        self.do_GET()

    def do_DELETE(self) -> None:
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args: object) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a mock GoodLinks API server.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=19428)
    parser.add_argument(
        "--scenario",
        choices=["default", "empty-columns", "long", "short-title-long-url"],
        default="default",
    )
    args = parser.parse_args()

    Handler.scenario = args.scenario
    HTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
