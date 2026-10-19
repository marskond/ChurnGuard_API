import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

def train_and_save_model():
    print("Генерация синтетических данных для обучения")
    # Создаем данные: 1000 клиентов, 3 признака
    X, y = make_classification(
        n_samples=1000, 
        n_features=3, 
        n_informative=2,
        n_redundant=1,
        n_repeated=0,
        random_state=42
    )
    
    print("Обучение модели RandomForest")
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    
    # Сохраняем модель в файл
    model_filename = "model.joblib"
    joblib.dump(model, model_filename)
    print(f"Модель успешно обучена и сохранена в {model_filename}")

if __name__ == "__main__":
    train_and_save_model()