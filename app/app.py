from flask import Flask, render_template, request, redirect, flash
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
# Secret key di sini
app.secret_key = os.getenv("SECRET_KEY")

# Ambil variabel environment dari file .env (dibaca Docker)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Fungsi koneksi ke PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host='db',
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Welcome Page
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Halaman Daftar Tempat Makan
@app.route('/places')
def show_places():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM places ORDER BY id ASC;')
    places = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', places=places)

# Tambah Data Tempat Makan
@app.route('/add', methods=['POST'])
def add_place():
    name = request.form['name']
    location = request.form['location']
    food_type = request.form['food_type']
    rating = request.form['rating']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO places (name, location, food_type, rating) VALUES (%s, %s, %s, %s)',
                (name, location, food_type, rating))
    conn.commit()
    flash("✅ Berhasil menambahkan tempat makan.")
    cur.close()
    conn.close()
    return redirect('/places')

# Hapus Data Tempat Makan
@app.route('/delete/<int:id>')
def delete_place(id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Cek apakah data ada
    cur.execute('SELECT * FROM places WHERE id = %s', (id,))
    place = cur.fetchone()

    if not place:
        flash("❌ Data tidak ditemukan.", "error")
    else:
        cur.execute('DELETE FROM places WHERE id = %s', (id,))
        conn.commit()
        flash("🗑️ Data berhasil dihapus.", "success")

    cur.close()
    conn.close()
    return redirect('/places')

# Edit Data Tempat Makan
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_place(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        food_type = request.form['food_type']
        rating = request.form['rating']

        cur.execute('UPDATE places SET name = %s, location = %s, food_type = %s, rating = %s WHERE id = %s',
                    (name, location, food_type, rating, id))
        conn.commit()
        flash("✏️ Data berhasil diperbarui.")
        cur.close()
        conn.close()
        return redirect('/places')

    cur.execute('SELECT * FROM places WHERE id = %s', (id,))
    place = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit.html', place=place)

# Jalankan aplikasi Flask di dalam Docker container
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)