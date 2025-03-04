# Business Insights Dashboard Brazilian E-Commerce Public Dataset

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```
streamlit run dashboard.py
```

## Run Streamlit with Auto-Reload (Live Update)
```
streamlit run dashboard.py --server.runOnSave=true
```

## Dashboard Link
Akses dashboard di sini: [Business Insights Dashboard](https://zainals-e-commerce-public-dataset-analysis.streamlit.app/)

## Troubleshooting
### 1. Streamlit Command Not Found
Jika muncul error:
```
streamlit : The term 'streamlit' is not recognized as the name of a cmdlet, function, script file, or operable program.
```
Coba jalankan Streamlit dengan:
```
python -m streamlit run dashboard.py
```
Atau pastikan bahwa Streamlit sudah terinstall:
```
pip install streamlit
```

### 2. Virtual Environment Tidak Aktif
Jika menggunakan virtual environment, pastikan sudah aktif:
- **Anaconda:** `conda activate main-ds`
- **Pipenv:** `pipenv shell`
- **Virtualenv:**
  ```
  python -m venv env
  env\Scripts\activate  # Windows
  source env/bin/activate  # macOS/Linux
  ```

### 3. Restart Streamlit Jika Perubahan Tidak Terdeteksi
Jika perubahan kode tidak langsung muncul, tekan **Ctrl + C** untuk menghentikan server, lalu jalankan ulang:
```
streamlit run dashboard.py
```

