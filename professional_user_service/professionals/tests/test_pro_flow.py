import requests

auth_headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
base_url = "http://localhost:8001"

def test_become_professional():
    response = requests.post(f"{base_url}/api/professionals/", json={
        "category": "Developer",
        "service": "Web development",
        "experience": 1,
        "projects": "CRUD operation,Doono",
        "skills": "Java,Springboot"
    }, headers=auth_headers)
    print(response.status_code, response.json())
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["service"] == "Web development"

def test_list_professionals():
    response = requests.get(f"{base_url}/api/professionalslist/", headers=auth_headers)
    print(response.status_code, response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(pro["service"] == "Web development" for pro in data)
