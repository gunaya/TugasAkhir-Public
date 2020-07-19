# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, flash, url_for, jsonify, Response, Flask
import gevent
from gevent.pywsgi import WSGIServer
from gevent.queue import Queue
import os
import flask
import json, time
from app import app
from app.queries import *
# from queries import *
from werkzeug.utils import secure_filename


# import fungsi CNN
from app.fungsi import *

ALLOWED_EXTENSIONS_MODEL = set(['h5','hdf5'])
ALLOWED_EXTENSIONS_IMAGE = set(['png', 'jpg', 'jpeg'])
DATASET_NAME = ''
DATASET_ID = 0

subscriptions = []

def allowed_model(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_MODEL
def allowed_image(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE

basedir = os.path.abspath(os.path.dirname(__file__))

# Route Landing Page
@app.route('/test')
def tests():
    insKelas()
    return 'hasil'

@app.route('/')
def index():
    return render_template('/landing/landing.html')

# Route Dashboard
@app.route('/dashboard/')
def dashboard():
    return render_template('/dashboard/index.html')


#####################################################################################################################
######## Req DATABASE ###############################################################################################

@app.route('/api/get-hasil-id/<id>')
def hasil_id(id):
    hasil = getHasilId(id)
    return hasil

@app.route('/api/det-dataset/<id>')
def det_dataset(id):
    hasil = detDataset(id)
    return hasil
    


#####################################################################################################################
######## Route Training #############################################################################################
@app.route('/dashboard/training/')
def dataset():

    return render_template('/dashboard/training/dataset.html')

@app.route('/dashboard/training/prepro')
def prepro():

    return render_template('/dashboard/training/preprocessing.html')

@app.route('/get-dataset', methods=["POST"])
def get_dataset():
    global DATASET_NAME, DATASET_ID
    dataset_name = request.form['dataset']
    DATASET_NAME = request.form['nama_dataset']
    DATASET_ID = request.form['dataset_id']
    images_list = inisialisasi_dataset(dataset_name, DATASET_ID)

    hasil = jsonify({'images' : images_list})
    return hasil

@app.route('/set-augmentasi', methods=['POST'])
def set_augmentasi():
    data_validasi = request.form['data_validasi']
    tinggi_citra = request.form['tinggi_citra']
    lebar_citra = request.form['lebar_citra']

    # set_augmentasi_data(data_validasi, tinggi_citra, lebar_citra)
    training_citra, training_kelas, validasi_citra, validasi_kelas, filename = set_augmentasi_data(data_validasi, tinggi_citra, lebar_citra)
    hasil = jsonify({'t_citra' : training_citra, 't_kelas' : training_kelas, 'v_citra':validasi_citra, 'v_kelas':validasi_kelas, 'filename':filename})
    return hasil

@app.route('/set-model', methods=['POST'])
def set_model():
    global DATASET_NAME, DATASET_ID
    pretrained = request.form['pretrained']
    optimizer = request.form['optimizer']
    n_epoch = request.form['n_epoch']
    nama = request.form['n_nama']
    lr = request.form['lr']
    n_epoch = int(n_epoch)
    epoch = []
    for i in range(n_epoch):
        epoch.append(i+1)

    summary = set_pretrained(pretrained, optimizer, n_epoch, nama, lr)

    # save to db
    insertHasil(summary, DATASET_NAME, DATASET_ID)

    hasil = jsonify({'summary' : summary, 'nama_dataset':DATASET_NAME, 'epoch': epoch})
    return hasil


@app.route('/set-inc', methods=['POST'])
def set_inc():
    global DATASET_NAME, DATASET_ID
    pretrained = request.form['pretrained']
    optimizer = request.form['optimizer']
    n_epoch = request.form['n_epoch']
    nama = request.form['n_nama']
    lr = request.form['lr']
    jumlah = request.form['jumlah_lama']
    n_epoch = int(n_epoch)
    epoch = []
    for i in range(n_epoch):
        epoch.append(i+1)

    summary = set_inc_learning(pretrained, optimizer, n_epoch, nama, lr, jumlah)

    # save to db
    insertHasil(summary, DATASET_NAME, DATASET_ID)

    hasil = jsonify({'summary' : summary, 'nama_dataset':DATASET_NAME, 'epoch': epoch})
    return hasil

#####################################################################################################################
######## Route Testing #############################################################################################
@app.route('/dashboard/testing')
def testing():
    return render_template('/dashboard/testing.html')

# ROUTE TESTING SINGLE
@app.route('/dashboard/testing/single', methods=["GET", "POST"])
def single_testing():
    return render_template('/dashboard/testing/single_test.html')

@app.route('/upload/model', methods=["POST"])
def single_upload():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
	
        files = request.files.getlist('file')
        
        errors = {}
        success = False
        
        for file in files:
            if file and allowed_model(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER_MODEL'], filename))
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'

        if success:
            resp = jsonify({'message' : 'Files successfully uploaded', 'filename':filename, 'code':201})
            resp.status_code = 201
            load_model_pelatihan(filename)
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 400
            return resp


@app.route('/upload/citra', methods=["POST"])
def image_upload():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
	
        files = request.files.getlist('file')
        
        errors = {}
        success = False
        
        for file in files:
            if file and allowed_image(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER_CITRA'], filename))
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'

        if success:
            resp = jsonify({'message' : 'Files successfully uploaded', 'filename':filename, 'code':201})
            load_citra_pengujian(filename)
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 400
            return resp

@app.route('/uji/single', methods=["POST"])
def uji_single():
    lokasi_model = 0
    hasil_id = 0
    height = 0
    width = 0
    if(request.form['lokasi_model']):
        lokasi_model = request.form['lokasi_model']
        hasil_id = request.form['hasil_pelatihan_id']
    else:
        lokasi_model = 0
        height = request.form['height']
        width = request.form['width']

    dataset_id = request.form['dataset_id']

    result, nama_kelas, nilai_akurasi, t = pengujian_single(lokasi_model, dataset_id, hasil_id, height, width)
    print(result)
    hasil = jsonify({'result':result, 'nama_kelas':nama_kelas, 'nilai_akurasi':nilai_akurasi, 'aktivasi':t})
    return hasil

@app.route('/dashboard/testing/batch')
def batch_testing():
    return render_template('/dashboard/testing/batch_test.html')


# ROUTE MENU IDENTIFIKASI
@app.route('/dashboard/identifikasi', methods=["GET", "POST"])
def view_identifikasi():
    return render_template('/dashboard/testing/identifikasi.html')


#######################################################################################################
#######################################################################################################
#######################################################################################################
@app.route('/maintenance')
def maintenance():
    return render_template('/dashboard/misc/maintenance.html')


#######################################################################################################
########################################## API UNTUK MOBILE ###########################################
#######################################################################################################

@app.route('/api/get-dataset')
def dataset_db():
    hasil = getDataset()
    # hasil_json = dict(hasil)
    return hasil

@app.route('/api/create-dataset', methods=["POST"])
def create_dataset():
    nama = request.json
    print(nama['nama_dataset'])
    createDataset(nama['nama_dataset'])
    return nama

@app.route('/api/delete-dataset/<id>', methods=["DELETE"])
def delete_dataset(id):
    deleteDataset(id)
    return 'sukses'

# ---------------------------------------------------------------------------------- ///

@app.route('/api/get-kelas/<id>')
def kelas_db(id):
    hasil = getKelas(id)
    return hasil

@app.route('/api/create-kelas', methods=['POST'])
def create_kelas():
    data = request.json
    createKelas(data['nama_kelas'], data['dataset_id'])
    return 'success'

# ---------------------------------------------------------------------------------- ///

@app.route('/api/tambah-citra', methods=['POST'])
def tambah_citra():
    data = request.json
    jumlah = getJumlah(data['kelas_id'])
    jumlah = jumlah.get_json()

    total = 0
    if(jumlah[0]['jumlah'] == None or jumlah[0]['jumlah'] == 0):
        total = 1
    else:
        total = jumlah[0]['jumlah']
        total = 1 + int(total)

    hasil = tambahCitra(jumlah[0], data['image'], total)
    if(hasil == 'success'):
        updateJumlah(data['kelas_id'], total)
        return 'success'
    else:
        return 'error'

# ---------------------------------------------------------------------------------- ///

@app.route('/api/get-hasil')
def hasil_db():
    hasil = getHasil()
    return hasil

# ---------------------------------------------------------------------------------- ///

@app.route('/api/uji', methods=['POST', 'GET'])
def api_uji():
    if request.method == "POST":
        data = request.json
        print(data['hasil_pelatihan_id'], data['citra'], 'SUKSES')
        hasil_uji, kelas, akurasi, t = pengujian_api(data['hasil_pelatihan_id'], data['citra'])

    hasil = []
    hasil.append({'hasil':hasil_uji, 'nama_kelas':kelas, 'nilai_akurasi':akurasi, 't':t})

    return jsonify(hasil)