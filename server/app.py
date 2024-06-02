import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Mengizinkan permintaan dari React

# Data preprocessing
data_2017 = pd.read_excel('./dataset/2017.xlsx')
data_2018 = pd.read_excel('./dataset/2018.xlsx')
data_2019 = pd.read_excel('./dataset/2019.xlsx')
data_2020 = pd.read_excel('./dataset/2020.xlsx')
data_2021 = pd.read_excel('./dataset/2021.xlsx')

# Gabungkan data dari semua tahun
data = pd.concat([data_2017, data_2018, data_2019, data_2020, data_2021])
data = data.replace('-', np.nan)
data = data.fillna(0)

data_encoded = pd.get_dummies(data, columns=['Provinsi'])

# Pisahkan fitur (X) dan target (y)
X = data_encoded.drop(['Cakalang', 'Tongkol', 'Tuna', 'Udang '], axis=1)  # Hapus spasi di nama kolom 'Udang '
y_cakalang = data_encoded['Cakalang']
y_tongkol = data_encoded['Tongkol']
y_tuna = data_encoded['Tuna']
y_udang = data_encoded['Udang ']  # Hapus spasi di nama kolom 'Udang '

# Split data menjadi training set dan testing set
X_train, X_test, y_train_cakalang, y_test_cakalang = train_test_split(X, y_cakalang, test_size=0.2, random_state=42)
X_train, X_test, y_train_tongkol, y_test_tongkol = train_test_split(X, y_tongkol, test_size=0.2, random_state=42)
X_train, X_test, y_train_tuna, y_test_tuna = train_test_split(X, y_tuna, test_size=0.2, random_state=42)
X_train, X_test, y_train_udang, y_test_udang = train_test_split(X, y_udang, test_size=0.2, random_state=42)

# Scaling Fitur
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Membuat model Random Forest
rf_cakalang = RandomForestRegressor(n_estimators=100, random_state=42)
rf_tongkol = RandomForestRegressor(n_estimators=100, random_state=42)
rf_tuna = RandomForestRegressor(n_estimators=100, random_state=42)
rf_udang = RandomForestRegressor(n_estimators=100, random_state=42)

# Train model Random Forest
rf_cakalang.fit(X_train, y_train_cakalang)
rf_tongkol.fit(X_train, y_train_tongkol)
rf_tuna.fit(X_train, y_train_tuna)
rf_udang.fit(X_train, y_train_udang)

# Prediksi dengan Random Forest
y_pred_rf_cakalang = rf_cakalang.predict(X_test)
y_pred_rf_tongkol = rf_tongkol.predict(X_test)
y_pred_rf_tuna = rf_tuna.predict(X_test)
y_pred_rf_udang = rf_udang.predict(X_test)
# List of models and their predictions
models = ["Random Forest"]
y_preds = [y_pred_rf_cakalang, y_pred_rf_tongkol, y_pred_rf_tuna, y_pred_rf_udang]
y_tests = [y_test_cakalang, y_test_tongkol, y_test_tuna, y_test_udang] * 2  # Repeat for both models

# List of fish names
fish_names = ["Cakalang", "Tongkol", "Tuna", "Udang"]

for model, y_pred in zip(models, y_preds):
    for fish_name, y_test in zip(fish_names, y_tests):
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
     
     
# Endpoint untuk data asli
@app.route('/api/data')
def get_data():
    dataset_folder = 'dataset'
    data_by_year = {}

    for filename in os.listdir(dataset_folder):
        if filename.endswith('.xlsx'):
            year = filename[:-5]
            filepath = os.path.join(dataset_folder, filename)
            df = pd.read_excel(filepath)
            df = df.replace('-', np.nan)
            df = df.fillna(0)

            # Hapus spasi setelah "Udang" (lakukan sebelum menambahkan kolom tahun)
            df.rename(columns={"Udang ": "Udang"}, inplace=True)

            # Tambahkan kolom tahun
            df['Tahun'] = int(year)

            # Konversi DataFrame ke list of dictionaries
            data_by_year[year] = df.to_dict(orient='records')

    return jsonify(data_by_year)

def get_future_dates(num_days=1):
    base = datetime.today()
    date_list = [base + timedelta(days=x) for x in range(num_days)]
    return [(d.strftime("%Y-%m-%d"), d.strftime("%A")) for d in date_list]

# Endpoint untuk prediksi
@app.route('/api/predictions')
def get_predictions():
    # Data prediksi 14 hari ke depan
    future_dates = get_future_dates()

    # Membuat DataFrame untuk menyimpan prediksi
    predictions = pd.DataFrame(columns=['Tanggal', 'Hari', 'Cakalang_RF', 'Tongkol_RF', 'Tuna_RF', 'Udang_RF'])

    # Melakukan prediksi untuk setiap tanggal
    for date, day in future_dates:
        # Membuat data input untuk prediksi (misalnya, menggunakan rata-rata fitur dari data historis)
        input_data = X.mean().values.reshape(1, -1) 

    # Prediksi dengan Random Forest
    rf_cakalang_pred = rf_cakalang.predict(input_data)[0]
    rf_tongkol_pred = rf_tongkol.predict(input_data)[0]
    rf_tuna_pred = rf_tuna.predict(input_data)[0]
    rf_udang_pred = rf_udang.predict(input_data)[0]

    # Menambahkan prediksi ke DataFrame
    predictions = pd.concat([predictions, pd.DataFrame({
        '1Tanggal': [date],
        '1Hari': [day],
        'Cakalang_RF': [rf_cakalang_pred],
        'Tongkol_RF': [rf_tongkol_pred],
        'Tuna_RF': [rf_tuna_pred],
        'Udang_RF': [rf_udang_pred]
    })], ignore_index=True)
   # Ubah urutan kolom DataFrame
    predictions = predictions[['1Tanggal', '1Hari', 'Cakalang_RF', 'Tongkol_RF', 'Tuna_RF', 'Udang_RF']]

    # Ubah DataFrame prediksi menjadi format JSON
    prediction_data = predictions.to_dict(orient='records')

    return jsonify(prediction_data)

if __name__ == '__main__':
    app.run(debug=True)