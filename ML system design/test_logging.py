import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_get_all_students():
    print("Testing GET /students")
    response = requests.get(f"{BASE_URL}/students")
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_post_student():
    print("\nTesting POST /students")
    student_data = {
        "school": "GP",
        "sex": "F",
        "age": 17,
        "address": "U",
        "Medu": 4,
        "Fedu": 3
    }
    response = requests.post(f"{BASE_URL}/students", json=student_data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    return response.json().get("inserted_id")

def test_get_student_by_id(valid_id, invalid_id="123abc"):
    print("\nTesting GET /students/<valid_id>")
    response = requests.get(f"{BASE_URL}/students/{valid_id}")
    print("Status Code:", response.status_code)
    print("Response:", response.json())

    print("\nTesting GET /students/<invalid_id> (should fail)")
    response = requests.get(f"{BASE_URL}/students/{invalid_id}")
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def main():
    test_get_all_students()
    student_id = test_post_student()
    if student_id:
        test_get_student_by_id(student_id)

if __name__ == "__main__":
    main()
