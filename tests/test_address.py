def test_create_and_get(client):
    payload = {
        "name": "Home",
        "street": "123 Example St",
        "city": "TestCity",
        "latitude": 12.9716,
        "longitude": 77.5946
    }
    r = client.post("/api/v1/addresses/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data['name'] == 'Home'
    addr_id = data['id']

    r2 = client.get(f"/api/v1/addresses/{addr_id}")
    assert r2.status_code == 200
    assert r2.json()["city"] == "TestCity"

def test_nearby(client):
    p1 = {"name":"A","street":"s","city":"c","latitude":0.0,"longitude":0.0}
    p2 = {"name":"B","street":"s","city":"c","latitude":0.1,"longitude":0.1}
    p3 = {"name":"C","street":"s","city":"c","latitude":10.0,"longitude":10.0}
    client.post("/api/v1/addresses/", json=p1)
    client.post("/api/v1/addresses/", json=p2)
    client.post("/api/v1/addresses/", json=p3)

    r = client.get("/api/v1/addresses/nearby?lat=0&lon=0&distance_km=20")
    assert r.status_code == 200
    names = [a['name'] for a in r.json()]
    assert 'A' in names and 'B' in names and 'C' not in names
