from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Инициализация приложения
app = FastAPI(
    title="ChurnGuard API", 
    description="ML-powered Churn Prediction API с гарантией валидации данных",
    version="1.0.0"
)

# 3. Схема валидации входных данных (Контракт API)
class ChurnInput(BaseModel):
    tenure_months: int = Field(..., ge=0, le=100, description="Стаж клиента в месяцах (0-100)")
    monthly_charges: float = Field(..., ge=0.0, le=1000.0, description="Ежемесячный платеж (0-1000)")
    contract_type_encoded: int = Field(..., ge=0, le=2, description="Тип контракта (0: месяц, 1: год, 2: два года)")

# Загрузка модели при старте приложения
try:
    model = joblib.load("model.joblib")
    logger.info("Модель загружена в память")
except Exception as e:
    logger.error(f"Ошибка загрузки модели: {e}")
    raise RuntimeError("Не удалось загрузить модель. Убедитесь, что train.py был запущен.")

# Эндпоинт проверки здоровья
@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": True}

# Основной эндпоинт предсказания
@app.post("/predict")
def predict(input_data: ChurnInput):
    try:
        # Преобразуем входные данные в формат 2D-массива, который ждет sklearn
        features = [[
            input_data.tenure_months,
            input_data.monthly_charges,
            input_data.contract_type_encoded
        ]]
        
        # Делаем предсказание
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1].item() # Вероятность класса "1" (отток)
        
        # Логируем успешное событие
        logger.info(f"Prediction successful | tenure={input_data.tenure_months} | prob={probability:.4f}")
        
        return {
            "churn_predicted": bool(prediction),
            "churn_probability": round(probability, 4),
            "message": "Клиент склонен к оттоку" if prediction else "Клиент лоялен"
        }
        
    except Exception as e:
        logger.error(f"Ошибка при предсказании: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера при обработке запроса")