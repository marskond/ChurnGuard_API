from locust import HttpUser, task, between

class ChurnGuardUser(HttpUser):
    # Имитируем задержку между запросами от 1 до 3 секунд (как реальный человек)
    wait_time = between(1, 3)

    @task(1)
    def health_check(self):
        """Легкий запрос: проверка здоровья (20% нагрузки)"""
        self.client.get("/health")

    @task(3)
    def predict_churn(self):
        """Тяжелый запрос: предсказание модели (80% нагрузки)"""
        # Реалистичные данные для нагрузки
        payload = {
            "tenure_months": 24,
            "monthly_charges": 95.0,
            "contract_type_encoded": 2
        }
        # Делаем POST запрос. Если вернется не 2xx, Locust засчитает это как Failure
        with self.client.post("/predict", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Получен неожиданный статус код: {response.status_code}")