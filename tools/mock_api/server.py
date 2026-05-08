"""Local mock API for deterministic smoke-test execution.

The server intentionally covers only the endpoints exercised by
API_Automation/cases with the smoke marker. It is not a replacement for a
staging backend.
"""
from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse


TOKEN = "mock-token-13800138000"

PRODUCTS = [
    {
        "id": 10001,
        "name": "Mock iPhone 15",
        "price": 5999,
        "images": ["https://example.test/products/10001.png"],
        "specs": [{"id": 20001, "name": "Default", "stock": 99}],
    },
    {
        "id": 10002,
        "name": "Mock Android Phone",
        "price": 2999,
        "images": ["https://example.test/products/10002.png"],
        "specs": [{"id": 20002, "name": "Default", "stock": 99}],
    },
]

CATEGORIES = [
    {"id": 1, "name": "Digital", "parent_id": 0},
    {"id": 2, "name": "Home", "parent_id": 0},
    {"id": 3, "name": "Sports", "parent_id": 0},
    {"id": 4, "name": "Books", "parent_id": 0},
    {"id": 5, "name": "Beauty", "parent_id": 0},
    {"id": 11, "name": "Phones", "parent_id": 1},
    {"id": 12, "name": "Headphones", "parent_id": 1},
    {"id": 13, "name": "Accessories", "parent_id": 1},
]

DEFAULT_CART_ITEM = {
    "cart_item_id": 50001,
    "product_id": 10001,
    "spec_id": 20001,
    "quantity": 1,
    "selected": True,
    "price": 5999,
}


def success(data: Any = None, msg: str = "ok") -> dict[str, Any]:
    return {"code": 0, "msg": msg, "data": {} if data is None else data}


def error(code: int, msg: str, data: Any = None) -> dict[str, Any]:
    return {"code": code, "msg": msg, "data": {} if data is None else data}


class MockAPIHandler(BaseHTTPRequestHandler):
    server_version = "iOSAutomationMockAPI/1.0"

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler method
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/health":
            self._write_json(success({"status": "ok"}))
            return

        if parsed.path == "/user/info":
            self._write_json(
                success(
                    {
                        "user_id": 100001,
                        "id": 100001,
                        "phone": "13800138000",
                        "nickname": "Mock User",
                    }
                )
            )
            return

        if parsed.path == "/product/search":
            keyword = query.get("keyword", [""])[0]
            products = [] if "not_exist" in keyword else PRODUCTS
            self._write_json(success({"products": products, "total": len(products)}))
            return

        if parsed.path == "/product/category/list":
            parent_id = int(query.get("parent_id", ["0"])[0])
            categories = [item for item in CATEGORIES if item["parent_id"] == parent_id]
            self._write_json(success(categories))
            return

        if parsed.path == "/order/list":
            status = query.get("status", ["all"])[0]
            orders = [
                {
                    "order_no": "MOCK_ORDER_001",
                    "status": "pending",
                    "total_amount": 5999,
                    "items": [DEFAULT_CART_ITEM],
                }
            ]
            if status != "all":
                orders = [order for order in orders if order["status"] == status]
            self._write_json(success({"orders": orders, "total": len(orders)}))
            return

        if parsed.path == "/cart/list":
            self._write_json(success({"items": [DEFAULT_CART_ITEM]}))
            return

        if parsed.path == "/cart/summary":
            self._write_json(success({"item_count": 1, "total_price": 5999}))
            return

        if parsed.path == "/cart/count":
            self._write_json(success({"count": 1}))
            return

        self._write_json(error(404, f"Unhandled path: {parsed.path}"), status=404)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler method
        parsed = urlparse(self.path)
        body = self._read_json()

        if parsed.path in {"/user/login", "/user/login/password"}:
            phone = body.get("phone", "13800138000")
            self._write_json(success({"token": TOKEN, "phone": phone}))
            return

        if parsed.path == "/cart/add":
            item = {
                **DEFAULT_CART_ITEM,
                "product_id": body.get("product_id", 10001),
                "spec_id": body.get("spec_id", 20001),
                "quantity": body.get("quantity", 1),
            }
            self._write_json(success({"item": item}))
            return

        if parsed.path in {"/cart/clear", "/cart/select", "/cart/select/all"}:
            self._write_json(success())
            return

        self._write_json(error(404, f"Unhandled path: {parsed.path}"), status=404)

    def do_PUT(self) -> None:  # noqa: N802 - stdlib handler method
        parsed = urlparse(self.path)

        if parsed.path.startswith("/cart/item/"):
            self._write_json(success({"item": DEFAULT_CART_ITEM}))
            return

        if parsed.path == "/user/profile":
            body = self._read_json()
            self._write_json(success({"nickname": body.get("nickname", "Mock User")}))
            return

        self._write_json(error(404, f"Unhandled path: {parsed.path}"), status=404)

    def do_DELETE(self) -> None:  # noqa: N802 - stdlib handler method
        parsed = urlparse(self.path)

        if parsed.path.startswith("/cart/item/") or parsed.path.startswith("/user/address/"):
            self._write_json(success())
            return

        self._write_json(error(404, f"Unhandled path: {parsed.path}"), status=404)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def _write_json(self, payload: dict[str, Any], status: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def create_server(host: str = "127.0.0.1", port: int = 8010) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), MockAPIHandler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local API smoke mock server.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8010)
    args = parser.parse_args()

    server = create_server(args.host, args.port)
    print(f"Mock API listening on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
