import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib 
import os
from duckduckgo_search import DDGS

if not os.path.exists('graficos'):
    os.makedirs('graficos')

try:
    df = pd.read_csv('winequality-red.csv', sep=';')
    if df.shape[1] < 2:
         df = pd.read_csv('winequality-red.csv', sep=',')
except Exception as e:
    print(f"Erro ao ler arquivo: {e}")
    exit()

def categorizar(qualidade):
    if qualidade <= 5:
        return 'Ruim'
    elif qualidade == 6:
        return 'Médio'
    else:
        return 'Bom'

df['qualidade_categoria'] = df['quality'].apply(categorizar)
X = df.drop(['quality', 'qualidade_categoria'], axis=1)
y = df['qualidade_categoria']

print("Gerando gráficos...")

plt.figure(figsize=(8, 6))
sns.boxplot(x='qualidade_categoria', y='alcohol', data=df, palette="Reds")
plt.title('Teor Alcoólico vs Qualidade')
plt.tight_layout()
plt.savefig('graficos/1_boxplot.png')
plt.close()

plt.figure(figsize=(10, 8))
numeric_df = df.select_dtypes(include=['float64', 'int64'])
sns.heatmap(numeric_df.corr(), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlação')
plt.tight_layout()
plt.savefig('graficos/2_heatmap.png')
plt.close()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)

print(f"Acurácia: {acc * 100:.2f}%")

plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred, labels=['Ruim', 'Médio', 'Bom'])
sns.heatmap(cm, annot=True, fmt='d', xticklabels=['Ruim', 'Médio', 'Bom'], yticklabels=['Ruim', 'Médio', 'Bom'], cmap='Blues')
plt.ylabel('Verdadeiro')
plt.xlabel('Previsto')
plt.title('Matriz de Confusão')
plt.tight_layout()
plt.savefig('graficos/3_matriz_confusao.png')
plt.close()

joblib.dump(model, 'modelo_vinho.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("Treinamento concluído e gráficos salvos.")