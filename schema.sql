DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS bendungan;
DROP TABLE IF EXISTS periodik;
DROP TABLE IF EXISTS pengungsian;
DROP TABLE IF EXISTS pos;
DROP TABLE IF EXISTS personil;


CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	fullname TEXT NULL,
	role INTEGER DEFAULT 1, /*# 1 UPB, 2 Pengamat/Juru*/
	pos_id INTEGER NULL
);

INSERT INTO user (username, password, fullname) 
	VALUES ('upb1', 'demo', 'Unit Pengelola Bendungan 1');
INSERT INTO user (username, password, fullname, role) 
	VALUES ('juru1', 'demo', 'Petugas Bendungan 1', 2);

CREATE TABLE bendungan (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nama TEXT UNIQUE NOT NULL,
	cnama TEXT NULL,
	lonlat TEXT NULL,
	man FLOAT NULL, /* # Muka Air Normal */
	mamin FLOAT NULL, /* # Muka Air Minim */
	mamax FLOAT NULL /* # Muka Air Maximum */
);

INSERT INTO bendungan (nama) VALUES ('Logung');

CREATE TABLE periodik (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	pos_id INTEGER NOT NULL,
	sampling INTEGER, /* # waktu data */
	tma FLOAT, /* # nilai Tinggi Muka Air */
	vol FLOAT /* # hasil hitung dari Lengkung Kapasitas */
);

CREATE TABLE pengungsian (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nama VARCHAR(100) UNIQUE NOT NULL,
	desa VARCHAR(50),
	kecamatan VARCHAR(50),
	kabupaten VARCHAR(50),
	lonlat VARCHAR(100) NULL,
	elevasi FLOAT,
	kapasitas INTEGER
);

CREATE TABLE pos (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nama VARCHAR(50) UNIQUE NOT NULL,
	tipe INTEGER DEFAULT 1, /* # 1 PCH, 2 PDA, 3 Klimat */
   	lonlat VARCHAR(100) NULL,
	elevasi INTEGER NULL
);

CREATE TABLE personil (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nama VARCHAR(50) NOT NULL,
	user_id INTEGER NULL,
	wa VARCHAR(50) NULL,
	nik VARCHAR(50) NULL,
	desa VARCHAR(50) NULL,
	kecamatan VARCHAR(50) NULL,
	kabupaten VARCHAR(50) NULL
);


