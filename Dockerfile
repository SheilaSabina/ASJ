# Gunakan image Python versi 3.9
FROM python:3.9-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt ke container
COPY requirements.txt .

# Install semua dependensi Python dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file app kamu ke dalam container
COPY ./app /app

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
