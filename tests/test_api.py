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
    assert len(client.get("/hardware/cpus").json()) == 3
    assert len(client.get("/hardware/gpus").json()) == 3
    assert len(client.get("/hardware/rams").json()) == 2
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


def test_upgrade_advice_returns_one_option_per_component(client):
    response = client.post("/optimizer/upgrade-advice", json=VALID_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["baseline_score"] == 88
    assert {option["component"] for option in body["options"]} == {"cpu", "gpu", "ram"}


def test_upgrade_advice_unknown_component_returns_404(client):
    response = client.post("/optimizer/upgrade-advice", json={**VALID_PAYLOAD, "cpu_id": 999})

    assert response.status_code == 404


def test_share_roundtrip_returns_the_same_build(client):
    create_response = client.post("/optimizer/share", json=VALID_PAYLOAD)
    assert create_response.status_code == 200
    slug = create_response.json()["slug"]
    assert slug

    fetch_response = client.get(f"/optimizer/share/{slug}")
    assert fetch_response.status_code == 200
    assert fetch_response.json() == VALID_PAYLOAD


def test_share_unknown_component_returns_404(client):
    response = client.post("/optimizer/share", json={**VALID_PAYLOAD, "ram_id": 999})

    assert response.status_code == 404


def test_share_unknown_slug_returns_404(client):
    response = client.get("/optimizer/share/not-a-real-slug")

    assert response.status_code == 404
