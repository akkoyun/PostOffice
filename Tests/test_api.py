import pytest
from fastapi.testclient import TestClient
from PostOffice import PostOffice

# Define Test Client
client = TestClient(PostOffice)

# Test WeatherStat Root GET
def test_root():
    
    # Get Response
    response = client.get("/")
    
    # Print Response
    print(response.json())

    # Check Response
    assert response.status_code == 200

    # Check Response
    assert response.json() == {"Service": "PostOffice", "Version": "02.00.00"}