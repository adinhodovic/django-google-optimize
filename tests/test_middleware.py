def test_request_middleware(client):
    client.cookies["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    response = client.get("/test")
    assert response.wsgi_request.google_optimize == {"redesign": "new_design"}


def test_template_middleware(client):
    client.cookies["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    response = client.get("/test")
    assert response.content == b"new_design\n"
