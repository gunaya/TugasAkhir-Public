# IDENTIFIKASI TULISAN TANGAN MENGGUNAKAN METODE CONVOLUTIONAL NEURAL NETWORK DENGAN ARSITEKTUR VGG19

Identifikasi tulisan tangan merupakan proses yang dilakukan untuk mengenali kepemilikan dari sebuah tulisan tangan. Penelitian pada tugas akhir ini menggunakan Metode Convolutional Neural Network dengan Arsitektur VGG-19. Proses pelatihan menggunakan transfer learning untuk memanfaatkan kemampuan arsitektur VGG-19. Percobaan dalam penelitian ini menggunakan percobaan pada parameter learning rate dan epoch, serta percobaan incremental learning. Proses identifikasi menggunakan model terbaik dari hasil pelatihan jaringan. Melalui penelitian ini, diharapakan identifikasi tulisan tangan dapat diimplementasikan kedalam bidang terkait.

## PYTHON ENVIRONMENT

Tugas akhir ini menggunakan python 3.5. Environment dapat diunduh dengan menjalankan perintah sebagai berikut.

### Anaconda

```
conda env create -f environment.yml
```
atau
```
conda create --name <env_name> --file requirements.txt
```

### Pip

```
pip install -r requirements.txt
```

## DATABASE & DATASET

Sistem dapat dijalankan setelah mengatur database, mendaftarkan nama kelas, jumlah citra, dan path dari dataset yang digunakan. Dataset didaftarkan pada folder dataset

## MENJALANKAN SISTEM

Sistem dijalankan dengan menggunakan perintah sebagai berikut.

```
flask run
```


## AUTHOR

* **I WAYAN GUNAYA** (https://github.com/gunaya)



## ACKNOWLEDGEMENTS

* Hat tip to anyone whose code was used
* Stackoverflow
* Medium
* Inspiration
* etc
