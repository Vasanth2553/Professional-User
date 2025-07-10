import requests

auth_headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTAsInVzZXJuYW1lIjoiS2FydGhpayIsImlhdCI6MTc1MTQzMTc5MywiZXhwIjoxNzUyMDM2NTkzfQ.UPSglj1wXR63Ft8tZZwia8kDEGjWzQ7peUsGiz2TtRk"}
base_url="http://localhost:8001"

def test_hire_professional():
    # Get a professional user
    pro_list = requests.get(f"{base_url}/api/professionalslist/", headers=auth_headers)
    assert pro_list.status_code == 200
    pro_id = pro_list.json()[0]["user"]  # or "id" depending on your model

    # Hire that professional
    response = requests.post(f"{base_url}/api/hire/", json={
        "user": 1,  # assumed logged-in user ID
        "professional_user": pro_id
    }, headers=auth_headers)

    assert response.status_code == 200 or response.status_code == 201
    assert "success" in response.json().get("message", "").lower()