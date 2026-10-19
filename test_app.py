from fastapi.testclient import TestClient
from app import app

# Создаем тестовый клиент для нашего приложения
client = TestClient(app)

def test_health_check():
    """Тест проверяет, что приложение запускается и модель загружена"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model_loaded": True}

def test_predict_validation():
    """Тест проверяет, что валидация Pydantic отклоняет некорректные данные"""
    bad_data = {
        "tenure_months": -10,
        "monthly_charges": 50.0,
        "contract_type_encoded": 1
    }
    response = client.post("/predict", json=bad_data)
    assert response.status_code == 422  # Ошибка валидации