from __future__ import annotations

import threading

import requests

from tools.mock_api.server import create_server


def test_mock_api_supports_smoke_endpoints():
    server = create_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        login = requests.post(
            f"{base_url}/user/login",
            json={"phone": "13800138000", "code": "123456"},
            timeout=5,
        ).json()
        assert login["code"] == 0
        assert login["data"]["token"]

        user = requests.get(
            f"{base_url}/user/info",
            headers={"Authorization": f"Bearer {login['data']['token']}"},
            timeout=5,
        ).json()
        assert user["code"] == 0
        assert user["data"]["user_id"]

        products = requests.get(
            f"{base_url}/product/search",
            params={"keyword": "手机"},
            timeout=5,
        ).json()
        assert products["code"] == 0
        assert len(products["data"]["products"]) > 0

        categories = requests.get(
            f"{base_url}/product/category/list",
            params={"parent_id": 0},
            timeout=5,
        ).json()
        assert categories["code"] == 0
        assert len(categories["data"]) >= 5

        orders = requests.get(f"{base_url}/order/list", timeout=5).json()
        assert orders["code"] == 0
        assert "orders" in orders["data"]

        added = requests.post(
            f"{base_url}/cart/add",
            json={"product_id": 10001, "spec_id": 20001, "quantity": 1},
            timeout=5,
        ).json()
        assert added["code"] == 0

        cart = requests.get(f"{base_url}/cart/list", timeout=5).json()
        assert cart["code"] == 0
        assert len(cart["data"]["items"]) > 0
    finally:
        server.shutdown()
        server.server_close()
