import datetime
from .models import Pos, User, Manual, KONDISI_SIAGA, KATEGORI_SIAGA
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import HiddenField, RadioField, SubmitField, FloatField, IntegerField
from wtforms import DateField, DateTimeField, StringField, SelectField
from wtforms.widgets import TextArea
from wtfpeewee.orm import model_form
from wtforms.validators import DataRequired

PosForm = model_form(Pos, exclude=('cdate', 'mdate', 'ch_t', 'tma_t', 'trend_tma', 'sampling_tma', 'tma_trend'))
#print(hasattr(PosForm, 'extra_filters'))
UserForm = model_form(User, exclude=('cdate', 'mdate', 'last_seen'))

class ArusInformasiForm(FlaskForm):
    img_arus_informasi = FileField('img_arus_informasi', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'gif'], 'File Gambar')
    ])
    
    
class PengungsianForm(FlaskForm):
    nama = StringField()
    desa = StringField(default='')
    kecamatan = StringField(default='')
    kabupaten = StringField(default='')
    kapasitas_tampung = IntegerField(default=0)
    fasilitas = StringField(default='')
    elevasi = IntegerField(default=0)
    lonlat = StringField(default='')
    
    
class ManualForm(FlaskForm):
    pos_id = HiddenField('Pos Hidrologi', validators=[DataRequired()])
    tanggal = DateField('Tanggal', validators=[DataRequired()])
    jam = RadioField('Jam', choices=[('07', '07'), ('12', '12'), ('18', '18')])
    tma = FloatField('TMA')
    ch = FloatField('Curah Hujan')
    vol = FloatField()
    submit = SubmitField('Simpan')
    
class SiagaForm(FlaskForm):
    tanggal = DateTimeField('Tanggal Perubahan', default=datetime.datetime.now)
    kategori = SelectField('Indikator', choices=KATEGORI_SIAGA)
    kondisi = SelectField('Kondisi Sekarang', choices=KONDISI_SIAGA)
    catatan = StringField('Catatan', widget=TextArea())
    user = HiddenField('user')
    submit = SubmitField('Simpan')