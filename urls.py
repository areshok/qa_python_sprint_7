BASE_URL = "https://qa-scooter.praktikum-services.ru"

API_VERSION = "v1"

URLS = {
    "api": {
        "courier": {
            "login": f"{BASE_URL}/api/{API_VERSION}/courier/login",
            "create": f"{BASE_URL}/api/{API_VERSION}/courier",
            "delete": f"{BASE_URL}/api/{API_VERSION}/courier/",
        },
        "order": {
            "create": f"{BASE_URL}/api/{API_VERSION}/orders",
            "list": f"{BASE_URL}/api/{API_VERSION}/orders"
        },
    },
}
