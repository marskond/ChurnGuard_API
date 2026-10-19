from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    """Тест 1: Проверяет, что приложение запускается и модель загружена"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model_loaded": True}

def test_predict_validation():
    """Тест 2: Проверяет, что Pydantic отклоняет некорректные данные (защита модели)"""
    bad_data = {
        "tenure_months": -10,  # Отрицательный стаж недопустим
        "monthly_charges": 50.0,
        "contract_type_encoded": 1
    }
    response = client.post("/predict", json=bad_data)
    assert response.status_code == 422  # Ошибка валидации Unprocessable Entity

def test_predict_success():
    """Тест 3: Проверяет успешный прогноз и структуру ответа (Happy Path)"""
    good_data = {
        "tenure_months": 12,
        "monthly_charges": 85.5,
        "contract_type_encoded": 1
    }
    response = client.post("/predict", json=good_data)
    
    # Проверяем статус код
    assert response.status_code == 200
    
    # Проверяем, что в ответе есть нужные ключи
    response_json = response.json()
    assert "churn_predicted" in response_json
    assert "churn_probability" in response_json
    assert "message" in response_json
    
    # Проверяем типы данных
    assert isinstance(response_json["churn_predicted"], bool)
    assert isinstance(response_json["churn_probability"], float)