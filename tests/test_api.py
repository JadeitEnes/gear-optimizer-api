VALID_PAYLOAD = {
    "cpu_id": 1,
    "gpu_id": 1,
    "ram_id": 1,
    "resolution_id": 1,
    "usage_purpose": "gaming_balanced",
}


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hardware_endpoints_expose_catalog(client):
    assert len(client.get("/hardware/cpus").json()) == 2
    assert len(client.get("/hardware/gpus").json()) == 2
    assert len(client.get("/hardware/rams").json()) == 1
    assert len(client.get("/hardware/resolutions").json()) == 2


def test_cpu_response_hides_no_expected_field(client):
    cpu = client.get("/hardware/cpus").json()[0]

    assert set(cpu) == {"id", "brand", "model", "cores", "base_clock", "score"}


def test_analyze_returns_full_result(client):
    response = client.post("/optimizer/analyze", json=VALID_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 88
    assert body["level"] == "Profesyonel"
    assert body["advice"]
    assert body["detail"]["cpu"] == "Intel Core i9-13900K"


def test_analyze_unknown_component_returns_404(client):
    response = client.post("/optimizer/analyze", json={**VALID_PAYLOAD, "gpu_id": 999})

    assert response.status_code == 404
    assert "GPU" in response.json()["detail"]


def test_analyze_rejects_unknown_usage_purpose(client):
    response = client.post("/optimizer/analyze", json={**VALID_PAYLOAD, "usage_purpose": "mining"})

    assert response.status_code == 422


def test_analyze_rejects_missing_field(client):
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "ram_id"}
    response = client.post("/optimizer/analyze", json=payload)

    assert response.status_code == 422
