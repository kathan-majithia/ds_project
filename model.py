import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler

def train_model(df):

    features = ['TxnFee(ETH)', 'hour', 'day_of_week', 'fee_ratio']
    X = df[features].fillna(0)
    y = df['is_whale']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\nMODEL PERFORMANCE")
    print(f"Accuracy: {acc:.2%}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Whale']))

    importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n📊 Feature Importance:")
    print(importance)

    model.scaler = scaler
    model.accuracy = acc
    model.X_test = X_test
    model.y_test = y_test
    
    return model

def evaluate_model(model, df):
    
    return {
        'accuracy': model.accuracy,
        'test_size': len(model.y_test),
        'whale_predictions': sum(model.predict(model.X_test))
    }