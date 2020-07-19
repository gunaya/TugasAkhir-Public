from flask import jsonify, json
from app import app
import json
import pickle
from flaskext.mysql import MySQL

mysql = MySQL()
# mysql configuratoin
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = ''
app.config['MYSQL_DATABASE_DB']         = 'db_iden_tulisantangan'
mysql.init_app(app)

# queries
################################## query tb_hasil_pelatihan
def getHasil():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT*, (SELECT COUNT(*) FROM tb_kelas WHERE dataset_id=tb_hasil_pelatihan.`dataset_id` ) AS jumlah_kelas FROM tb_hasil_pelatihan ORDER BY TIMESTAMP DESC")
    data = cursor.fetchall()
    payload = []
    content = {}
    if data is not None:
        for item in data:
            content = {
                'hasil_pelatihan_id'    : item[0],
                'nama'                  : item[1],
                'lokasi_model'          : item[2],
                'acc'                   : item[3],
                'loss'                  : item[4],
                'val_acc'               : item[5],
                'val_loss'              : item[6],
                'optimizer'             : item[7],
                'pretrained'            : item[8],
                'nama_dataset'          : item[9],
                'tanggal'               : item[10],
                'timestamp'             : item[11],
                'timer'                 : item[12],
                'ukuran_citra'          : item[13],
                'dataset_id'            : item[14],
                'jumlah_kelas'          : item[16],
            }
            payload.append(content)
            content = {}
        return jsonify(payload)
    else:
        return 'data kosong'

def getHasilId(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT*FROM tb_hasil_pelatihan WHERE hasil_pelatihan_id = %s", (id))
    data = cursor.fetchall()
    payload = []
    content = {}
    if data is not None:
        for item in data:
            history = pickle.load(open(item[15], 'rb'))
            print(history)
            # history = '121212'
            content = {
                'hasil_pelatihan_id'    : item[0],
                'nama'                  : item[1],
                'lokasi_model'          : item[2],
                'acc'                   : item[3],
                'loss'                  : item[4],
                'val_acc'               : item[5],
                'val_loss'              : item[6],
                'optimizer'             : item[7],
                'pretrained'            : item[8],
                'nama_dataset'          : item[9],
                'tanggal'               : item[10],
                'timestamp'             : item[11],
                'timer'                 : item[12],
                'ukuran_citra'          : item[13],
                'dataset_id'            : item[14],
                'history'               : history
            }
            payload.append(content)
            content = {}
        return jsonify(payload)
        # return json.dumps(payload)
    else:
        return 'data kosong'

def insertHasil(summary, dataset, dataset_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tb_hasil_pelatihan(
            nama, lokasi_model, acc, loss, val_acc, val_loss, optimizer, pretrained, tanggal, nama_dataset, timer, ukuran_citra, dataset_id, pickle)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            (
                summary['nama_save'], summary['lokasi_simpan'], int(summary['acc']), int(summary['loss']), 
                int(summary['val_acc']), int(summary['val_loss']), summary['optimizer'], summary['pretrain'],
                summary['time'], dataset, int(summary['timer']), summary['ukuran'], dataset_id, summary['pickle']
            ))
    conn.commit()
    conn.close()


################################## query tb_dataset
def getDataset():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT *, (SELECT COUNT(*) FROM tb_kelas WHERE dataset_id=tb_dataset.`dataset_id` ) AS total_kelas FROM tb_dataset")
    data = cursor.fetchall()
    payload = []
    content = {}
    for result in data:
        content = {'dataset_id': result[0], 'nama_dataset': result[1], 'lokasi': result[2], 'total_kelas': result[3]}
        payload.append(content)
        content = {}
    return jsonify(payload)

def detDataset(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT *, (SELECT COUNT(*) FROM tb_kelas WHERE dataset_id=tb_dataset.`dataset_id` ) AS total_kelas FROM tb_dataset WHERE dataset_id = %s", (id))
    data = cursor.fetchall()
    payload = []
    content = {}
    for result in data:
        content = {'dataset_id': result[0], 'nama_dataset': result[1], 'lokasi': result[2], 'total_kelas': result[3]}
        payload.append(content)
        content = {}
    return jsonify(payload)

def createDataset(nama):
    lokasi = nama.replace(" ", "_")
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tb_dataset(nama_dataset, lokasi) VALUES(%s, %s)", (nama, lokasi))
    conn.commit()
    conn.close()

def deleteDataset(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_dataset WHERE dataset_id = %s", (id))
    conn.commit()
    conn.close()

################################## query tb_kelas
def getKelas(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT*FROM tb_kelas WHERE dataset_id = %s", (id))
    data = cursor.fetchall()
    payload = []
    content = {}
    if data is not None:
        for item in data:
            content = {
                'kelas_id'      : item[0],
                'nama_kelas'    : item[1],
                'jumlah'        : item[2],
                'dataset_id'    : item[3]
            }
            payload.append(content)
            content = {}
        return jsonify(payload)
    else:
        return 'data kosong'

def createKelas(kelas, dataset_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tb_kelas(nama_kelas, dataset_id) VALUES(%s, %s)", (kelas, dataset_id))
    conn.commit()
    conn.close()

def getJumlah(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_kelas INNER JOIN tb_dataset ON tb_kelas.`dataset_id` = tb_dataset.`dataset_id` WHERE kelas_id = %s", (id))
    data = cursor.fetchall()
    payload = []
    content = {}
    if data is not None:
        for item in data:
            content = {
                'nama_kelas'   : item[1],
                'jumlah'        : item[2],
                'lokasi'        : item[6]
            }
            payload.append(content)
            content = {}
        return jsonify(payload)
    else:
        return 'data kosong'

def updateJumlah(id, jumlah):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE tb_kelas SET jumlah = %s WHERE kelas_id = %s", (jumlah, id))
    conn.commit()
    conn.close()
    

################################## misq
def insKelas():
    classes = ['000', '007', '013', '016', '017', '019', '025', '026', '037', '058', '059', '060', '061', '062', '063', '064', '066', '084', '085', '087', '088', '089', '090', '091', '092', '093', '094', '107', '108', '109', '110', '111', '112', '113', '114', '117', '118', '119', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '135', '140', '150', '151', '152', '153', '154', '155', '158', '160', '163', '164', '165', '172', '173', '174', '178', '181', '185', '188', '193', '198', '199', '202', '203', '204', '205', '206', '207', '208', '209', '212', '213', '214', '216', '217', '247', '248', '273', '274', '285', '287', '288', '289', '292', '293', '315', '332', '333', '334', '335', '336', '337', '338', '339', '340', '341', '342', '343', '344', '345', '346', '347', '348', '349', '351', '352', '353', '354', '355', '384', '385', '386', '387', '389', '390', '391', '393', '415', '454', '455', '456', '498', '544', '546', '547', '548', '549', '550', '551', '552', '567', '582', '583', '584', '585', '588', '634', '635', '670', '671']
    
    jumlah = [111, 21, 30, 27, 26, 27, 38, 43, 41, 31, 27, 36, 25, 23, 27, 35, 12, 13, 39, 22, 18, 22, 18, 21, 26, 26, 21, 36, 28, 28, 26, 32, 29, 29, 21, 35, 39, 18, 36, 31, 48, 35, 31, 42, 36, 40, 32, 30, 51, 18, 15, 89, 85, 87, 97, 93, 80, 20, 12, 16, 15, 14, 10, 49, 29, 15, 24, 16, 16, 38, 12, 36, 51, 33, 49, 40, 41, 42, 40, 63, 24, 18, 9, 17, 24, 50, 42, 32, 37, 43, 48, 41, 46, 47, 30, 58, 65, 80, 75, 56, 59, 59, 65, 74, 64, 76, 73, 66, 82, 88, 85, 65, 63, 72, 40, 39, 48, 43, 40, 98, 42, 47, 44, 36, 38, 40, 33, 71, 40, 41, 48, 43, 44, 45, 52, 43, 45, 37, 96, 96, 61, 39, 46, 44, 40, 89, 94, 72, 92, 105]

    conn = mysql.connect()
    cursor = conn.cursor()
    for i in range(len(classes)):
        cursor.execute("INSERT INTO tb_kelas(nama_kelas, jumlah, dataset_id) VALUES(%s, %s, %s)", (classes[i], jumlah[i], 6))
        conn.commit()

