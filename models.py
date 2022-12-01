import datetime

import peewee as pw
from flask_login import UserMixin
from playhouse.flask_utils import FlaskDB
from werkzeug.security import check_password_hash, generate_password_hash

db = FlaskDB()

SIAGA_LOGUNG = {
    'puncak': 94,
    'awas': 93.75, # merah
    'siaga': 92.75, # Kuning
    'spillway': 88.5 # Hijau
}

class KV(db.Model):
    k = pw.CharField(unique=True)
    v = pw.CharField(null=True)
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    mdate = pw.DateTimeField(null=True)
    
class Pos(db.Model):
    nama = pw.CharField(unique=True, max_length=50)
    tipe = pw.IntegerField(default=1) # 1 PCH, 2 PDA, 3 Klimat */
    lonlat = pw.CharField(max_length=100, null=True)
    elevasi = pw.IntegerField(null=True)
    ch_t = pw.FloatField(default=0) # Curah hujan dari jam 7 tadi
    tma_t = pw.FloatField() # TMA sesuai waktu kolom 'sampling'
    sampling_tma = pw.DateTimeField(null=True)
    tma_trend = pw.CharField(max_length=1) # N-aik, T-urun
    sh = pw.FloatField(null=True)
    sk = pw.FloatField(null=True)
    sm = pw.FloatField(null=True)
    is_aktif = pw.BooleanField(default=False)
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    mdate = pw.DateTimeField(null=True)

    def __str__(self):
        return self.nama
    
    def __unicode__(self):
        return self.nama


class User(UserMixin, db.Model):
    username = pw.CharField(unique=True, max_length=25)
    password = pw.CharField(max_length=100, null=True)
    role = pw.IntegerField(default=1)
    pos = pw.ForeignKeyField(Pos, null=True)
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    mdate = pw.DateTimeField(null=True)
    last_seen = pw.DateTimeField(null=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __unicode__(self):
        return self.username


class Bendungan(db.Model):
    nama = pw.CharField(unique=True, max_length=100)
    cnama = pw.CharField(null=True)
    lonlat = pw.CharField(null=True)
    man = pw.FloatField(null=True) # Muka Air Normal 
    mamin = pw.FloatField(null=True) # Muka Air Minim 
    mamax = pw.FloatField(null=True) # Muka Air Maximum
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    mdate = pw.DateTimeField(null=True)

    def __unicode__(self):
        return self.nama


class Manual(db.Model):
    pos = pw.ForeignKeyField(Pos, backref='manuals')
    sampling = pw.DateTimeField() # waktu data */
    ch = pw.FloatField(null=True) # Curah Hujan (mm)
    tma = pw.FloatField(null=True) # nilai Tinggi Muka Air (m) */
    vol = pw.FloatField(null=True) # hasil hitung dari Lengkung Kapasitas */
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    mdate = pw.DateTimeField(null=True)

    def __unicode__(self):
        return self.sampling


class Periodik(db.Model):
    pos = pw.ForeignKeyField(Pos, backref='periodiks')
    sampling = pw.DateTimeField() # waktu data */
    ch = pw.FloatField(null=True) # Curah Hujan (mm)
    tma = pw.FloatField(null=True) # nilai Tinggi Muka Air (meter) */
    vol = pw.FloatField(null=True) # hasil hitung dari Lengkung Kapasitas */
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    mdate = pw.DateTimeField(null=True)

    def __unicode__(self):
        return self.sampling


class Pengungsian(db.Model):
    nama = pw.CharField(unique=True, max_length=100)
    desa = pw.CharField(null=True)
    kecamatan = pw.CharField(null=True)
    kabupaten = pw.CharField(null=True)
    elevasi = pw.IntegerField(null=True)
    kapasitas_tampung = pw.IntegerField(null=True)
    fasilitas = pw.CharField(null=True)
    lonlat = pw.CharField(null=True)
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    mdate = pw.DateTimeField(null=True)

    def __unicode__(self):
        return self.nama


class Personil(db.Model):
    nama = pw.CharField(max_length=50)
    user = pw.ForeignKeyField(User, backref='user')
    wa = pw.CharField(null=True)
    nik = pw.CharField(unique=True)
    desa = pw.CharField(null=True)
    kecamatan = pw.CharField(null=True)
    kabupaten = pw.CharField(null=True)
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    mdate = pw.DateTimeField(null=True)

    def __unicode__(self):
        return self.nama
    
    
KONDISI_SIAGA = ((0, 'Normal'), (1, 'Abnormal'), (2, 'Waspada'), 
                 (3, 'Siaga'), (4, 'Awas'))
KATEGORI_SIAGA = (
    (1, 'Peluapan / Over Topping'),
    (2, 'Rembesan / Piping'),
    (3, 'Didih Pasir'),
    (4, 'Lubang Benam'),
    (5, 'Retakan pada Tubuh Bendungan'),
    (6, 'Penurunan / Settlement'),
    (7, 'Longsoran pada Tubuh Bendungan'),
    (8, 'Retakan pada Struktur Beton'),
    (9, 'Akibat Gempa Bumi'))

class IndikatorSiaga(db.Model):
    kategori = pw.IntegerField()
    obyek_pantau = pw.CharField()
    hasil_pantau = pw.CharField()
    kondisi = pw.IntegerField(default=0) # 0 Normal, 1: Abnormal, 2:Waspada, 3: Siaga, 4: Awas
    pemberitahuan = pw.CharField()
    tindakan = pw.CharField()
    bahanalat = pw.CharField()
    pencatatan = pw.CharField()
    penanggungjawab = pw.CharField()
    
    
class StatusLog(db.Model):
    tanggal = pw.DateTimeField()
    kategori = pw.IntegerField()
    kondisi = pw.IntegerField()
    catatan = pw.CharField()
    user = pw.CharField()
    cdate = pw.DateTimeField(default=datetime.datetime.now)
    mdate = pw.DateTimeField(null=True)
    