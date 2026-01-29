from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import pymysql
from datetime import datetime
from fpdf import FPDF

app_Ahkam = Flask(__name__)
app_Ahkam.secret_key = "Ahkam_rahasia_123"

def hitung_nilai_akhir_Ahkam(tugas, uts, uas):
    return (int(tugas) + int(uts) + int(uas)) // 3

def koneksi_database_Ahkam():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="", 
        database="rapot_Ahkam",
        cursorclass=pymysql.cursors.DictCursor
    )

@app_Ahkam.route('/')
def halaman_utama_Ahkam():
    nama_cari = request.args.get('search_nama', '')
    db_Ahkam = koneksi_database_Ahkam()
    with db_Ahkam.cursor() as kursor_Ahkam:
        sql_Ahkam = """
            SELECT n.*, s.nama, m.nama_mapel 
            FROM nilai_Ahkam n
            JOIN siswa_Ahkam s ON n.nis = s.nis
            JOIN mapel_Ahkam m ON n.id_mapel = m.id_mapel
            WHERE s.nama LIKE %s
        """
        kursor_Ahkam.execute(sql_Ahkam, ('%' + nama_cari + '%',))
        data_Ahkam = kursor_Ahkam.fetchall()
    db_Ahkam.close()
    return render_template('index_Ahkam.html', daftar_nilai_Ahkam=data_Ahkam, keyword=nama_cari)


@app_Ahkam.route('/halaman_cetak_Ahkam')
def halaman_cetak_Ahkam():
    nama_cari = request.args.get('search_nama', '')
    
    
    if not nama_cari or nama_cari.strip() == "":
        flash("Silakan cari nama siswa terlebih dahulu sebelum mencetak!", "warning")
        return redirect(url_for('halaman_utama_Ahkam'))

    db_Ahkam = koneksi_database_Ahkam()
    tanggal = datetime.now().strftime("%d %B %Y")
    
    with db_Ahkam.cursor() as kursor_Ahkam:
        sql_Ahkam = """
            SELECT 
                s.nama, m.nama_mapel,
                MAX(CASE WHEN n.semester = '1' THEN n.id_nilai END) AS id_1,
                MAX(CASE WHEN n.semester = '1' THEN n.nilai_tugas END) AS tugas_1,
                MAX(CASE WHEN n.semester = '1' THEN n.nilai_uts END) AS uts_1,
                MAX(CASE WHEN n.semester = '1' THEN n.nilai_uas END) AS uas_1,
                MAX(CASE WHEN n.semester = '1' THEN n.nilai_akhir END) AS akhir_1,
                MAX(CASE WHEN n.semester = '1' THEN n.deskripsi END) AS deskripsi_1,
                MAX(CASE WHEN n.semester = '2' THEN n.id_nilai END) AS id_2,
                MAX(CASE WHEN n.semester = '2' THEN n.nilai_tugas END) AS tugas_2,
                MAX(CASE WHEN n.semester = '2' THEN n.nilai_uts END) AS uts_2,
                MAX(CASE WHEN n.semester = '2' THEN n.nilai_uas END) AS uas_2,
                MAX(CASE WHEN n.semester = '2' THEN n.nilai_akhir END) AS akhir_2,
                MAX(CASE WHEN n.semester = '2' THEN n.deskripsi END) AS deskripsi_2
            FROM siswa_Ahkam s
            JOIN nilai_Ahkam n ON s.nis = n.nis
            JOIN mapel_Ahkam m ON n.id_mapel = m.id_mapel
            WHERE s.nama LIKE %s
            GROUP BY s.nama, m.nama_mapel
        """
        kursor_Ahkam.execute(sql_Ahkam, ('%' + nama_cari + '%',))
        data_Ahkam = kursor_Ahkam.fetchall()
        
        if not data_Ahkam:
            flash(f"Data siswa '{nama_cari}' tidak ditemukan!", "danger")
            return redirect(url_for('halaman_utama_Ahkam'))
            
        nama_siswa = data_Ahkam[0]['nama']
        
    db_Ahkam.close()
    return render_template('cetak_Ahkam.html', 
                           daftar_nilai_Ahkam=data_Ahkam, 
                           nama_siswa=nama_siswa, 
                           tanggal_sekarang=tanggal)

@app_Ahkam.route('/unduh_pdf_Ahkam/<semester>')
def unduh_pdf_Ahkam(semester):
    nama_cari = request.args.get('search_nama', '')
    smt_val = '1' if semester == 'smt1' else '2'
    db_Ahkam = koneksi_database_Ahkam()
    
    with db_Ahkam.cursor() as kursor_Ahkam:
        sql_Ahkam = """
            SELECT s.nama, m.nama_mapel, n.nilai_tugas, n.nilai_uts, n.nilai_uas, n.nilai_akhir, n.deskripsi
            FROM nilai_Ahkam n
            JOIN siswa_Ahkam s ON n.nis = s.nis
            JOIN mapel_Ahkam m ON n.id_mapel = m.id_mapel
            WHERE s.nama LIKE %s AND n.semester = %s
        """
        kursor_Ahkam.execute(sql_Ahkam, ('%' + nama_cari + '%', smt_val))
        data_Ahkam = kursor_Ahkam.fetchall()
    db_Ahkam.close()

    if not data_Ahkam:
        return "Data tidak tersedia", 404

    pdf = FPDF()
    pdf.add_page()
    
   
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "LAPORAN HASIL BELAJAR SISWA (RAPOT)", 0, 1, 'C')
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, "SMK NEGERI 2 CIMAHI", 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, f"Nama Siswa : {data_Ahkam[0]['nama']}", 0, 1)
    pdf.cell(0, 8, f"Semester   : {'1 (GANJIL)' if smt_val == '1' else '2 (GENAP)'}", 0, 1)
    pdf.ln(2)

    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(50, 10, 'Mata Pelajaran', 1, 0, 'C', True)
    pdf.cell(12, 10, 'Tgs', 1, 0, 'C', True)
    pdf.cell(12, 10, 'UTS', 1, 0, 'C', True)
    pdf.cell(12, 10, 'UAS', 1, 0, 'C', True)
    pdf.cell(15, 10, 'Akhir', 1, 0, 'C', True)
    pdf.cell(88, 10, 'Deskripsi Kemajuan Belajar', 1, 1, 'C', True)

    
    pdf.set_font("Arial", '', 9)
    for d in data_Ahkam:
        pdf.cell(50, 10, str(d['nama_mapel']), 1)
        pdf.cell(12, 10, str(d['nilai_tugas']), 1, 0, 'C')
        pdf.cell(12, 10, str(d['nilai_uts']), 1, 0, 'C')
        pdf.cell(12, 10, str(d['nilai_uas']), 1, 0, 'C')
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(15, 10, str(d['nilai_akhir']), 1, 0, 'C')
        pdf.set_font("Arial", 'I', 8)
        pdf.multi_cell(88, 10, str(d['deskripsi']), 1)
        pdf.set_font("Arial", '', 9)

    
    pdf.ln(10)
    pdf.cell(127, 5, "", 0, 0)
    pdf.cell(63, 5, f"Cimahi, {datetime.now().strftime('%d %B %Y')}", 0, 1, 'C')
    pdf.cell(63, 5, "Orang Tua/Wali,", 0, 0, 'C')
    pdf.cell(64, 5, "", 0, 0)
    pdf.cell(63, 5, "Wali Kelas,", 0, 1, 'C')
    pdf.ln(15)
    pdf.cell(63, 5, "( ............................... )", 0, 0, 'C')
    pdf.cell(64, 5, "", 0, 0)
    pdf.cell(63, 5, "( Kiki Juniantie, S.Pd. )", 0, 1, 'C')

    
    pdf_output = pdf.output()
    if isinstance(pdf_output, str):
        pdf_bytes = pdf_output.encode('latin-1')
    else:
        pdf_bytes = bytes(pdf_output)

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=Rapot_{semester}.pdf"
    return response

@app_Ahkam.route('/tambah_nilai_Ahkam', methods=['GET', 'POST'])
def tambah_nilai_Ahkam():
    db_Ahkam = koneksi_database_Ahkam()
    if request.method == 'POST':
        nis, id_mapel = request.form['nis'], request.form['id_mapel']
        n_tugas, n_uts, n_uas = request.form['nilai_tugas'], request.form['nilai_uts'], request.form['nilai_uas']
        deskripsi, semester, tahun = request.form['deskripsi'], request.form['semester'], request.form['tahun_ajaran']
        n_akhir = hitung_nilai_akhir_Ahkam(n_tugas, n_uts, n_uas)
        
        with db_Ahkam.cursor() as kursor_Ahkam:
            kursor_Ahkam.execute("SELECT id_nilai FROM nilai_Ahkam ORDER BY id_nilai DESC LIMIT 1")
            last = kursor_Ahkam.fetchone()
            id_baru = "N" + str(int(last['id_nilai'][1:]) + 1).zfill(3) if last else "N001"
            kursor_Ahkam.execute("INSERT INTO nilai_Ahkam VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 (id_baru, nis, id_mapel, n_tugas, n_uts, n_uas, n_akhir, deskripsi, semester, tahun))
        db_Ahkam.commit()
        db_Ahkam.close()
        flash("Data berhasil ditambahkan!", "success")
        return redirect(url_for('halaman_utama_Ahkam'))
    
    with db_Ahkam.cursor() as kursor_Ahkam:
        kursor_Ahkam.execute("SELECT nis, nama FROM siswa_Ahkam")
        siswa = kursor_Ahkam.fetchall()
        kursor_Ahkam.execute("SELECT id_mapel, nama_mapel FROM mapel_Ahkam")
        mapel = kursor_Ahkam.fetchall()
    db_Ahkam.close()
    return render_template('tambah_nilai_Ahkam.html', siswa=siswa, mapel=mapel)

@app_Ahkam.route('/ubah_nilai_Ahkam/<id_nilai>', methods=['GET', 'POST'])
def ubah_nilai_Ahkam(id_nilai):
    db_Ahkam = koneksi_database_Ahkam()
    if request.method == 'POST':
        n_tugas, n_uts, n_uas = request.form['nilai_tugas'], request.form['nilai_uts'], request.form['nilai_uas']
        deskripsi = request.form['deskripsi']
        n_akhir = hitung_nilai_akhir_Ahkam(n_tugas, n_uts, n_uas)
        
        with db_Ahkam.cursor() as kursor_Ahkam:
            sql_update = "UPDATE nilai_Ahkam SET nilai_tugas=%s, nilai_uts=%s, nilai_uas=%s, nilai_akhir=%s, deskripsi=%s WHERE id_nilai=%s"
            kursor_Ahkam.execute(sql_update, (n_tugas, n_uts, n_uas, n_akhir, deskripsi, id_nilai))
        db_Ahkam.commit()
        db_Ahkam.close()
        flash(f"Data {id_nilai} berhasil diperbarui!", "success")
        return redirect(url_for('halaman_utama_Ahkam'))
    
    with db_Ahkam.cursor() as kursor_Ahkam:
        kursor_Ahkam.execute("SELECT * FROM nilai_Ahkam WHERE id_nilai=%s", (id_nilai,))
        data_lama = kursor_Ahkam.fetchone()
    db_Ahkam.close()
    return render_template('ubah_nilai_Ahkam.html', n=data_lama)

@app_Ahkam.route('/hapus_nilai_Ahkam/<id_nilai>')
def hapus_nilai_Ahkam(id_nilai):
    db_Ahkam = koneksi_database_Ahkam()
    with db_Ahkam.cursor() as kursor_Ahkam:
        kursor_Ahkam.execute("DELETE FROM nilai_Ahkam WHERE id_nilai=%s", (id_nilai,))
    db_Ahkam.commit()
    db_Ahkam.close()
    flash("Data berhasil dihapus!", "success")
    return redirect(url_for('halaman_utama_Ahkam'))

if __name__ == '__main__':
    app_Ahkam.run(debug=True)