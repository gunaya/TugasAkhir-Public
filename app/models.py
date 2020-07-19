from app import db
from datetime import datetime

class tb_dataset(db.Model):
    dataset_id = db.Column(db.Integer, primary_key=True)
    nama_dataset = db.Column(db.String(255))
    lokasi = db.Column(db.String(255))
    # kelas = db.relationship('Kelas', backref='dataset', lazy='dynamic')
    # hasil_pelatihan = db.relationship('Hasil pelatihan', backref='dataset', lazy='dynamic')

    def __repr__(self):
        return '<Dataset {}>'.format(self.nama_dataset)


class tb_kelas(db.Model):
    kelas_id = db.Column(db.Integer, primary_key=True)
    nama_kelas = db.Column(db.String(255))
    jumlah = db.Column(db.Integer)
    dataset_id = db.Column(db.Integer, db.ForeignKey('tb_dataset.dataset_id'))

    def __repr__(self):
        return '<Kelas {}>'.format(self.nama_kelas)


class tb_hasil_pelatihan(db.Model):
    hasil_pelatihan_id = db.Column(db.Integer, primary_key = True)
    nama = db.Column(db.String(255))
    lokasi_model = db.Column(db.String(255))
    acc = db.Column(db.String(255))
    loss = db.Column(db.String(255))
    val_acc = db.Column(db.String(255))
    val_loss = db.Column(db.String(255))
    optimizer = db.Column(db.String(255))
    pretrained = db.Column(db.String(255))
    tanggal = db.Column(db.DateTime)
    # dataset_id = db.Column(db.Integer, db.ForeignKey('tb_dataset.dataset_id'))
    nama_dataset = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

