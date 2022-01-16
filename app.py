
from cgitb import text
from email import message
from enum import unique
from sqlite3 import Date
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime , event, DDL
from sqlalchemy.sql import func ,select
from datetime import datetime
from datetime import timedelta
from sqlalchemy.sql.expression import cast

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug == True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nenene134@localhost/lexus'
else:
    app.debug == False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class korisnik(db.Model):
    __tablename__ = 'korisnik'
    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.Date)

    def __init__(self, datum):
        self.datum = datum 

class dnevnik(db.Model):
    __tablename__ = 'dnevnik'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    biljeska = db.Column(db.String(200))

    def __init__(self,created_date,biljeska):
        self.created_date = created_date
        self.biljeska = biljeska

class kilaza(db.Model):
    __tablename__ = 'kilaza'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    kilaza = db.Column(db.Integer)

    def __init__(self,created_date,kilaza):
        self.created_date = created_date
        self.kilaza = kilaza

class jelovnik(db.Model):
    __tablename__ = 'jelovnik'
    id = db.Column(db.Integer, primary_key=True)
    jelo = db.Column(db.String(200))
    kolicina = db.Column(db.Integer)

    def __init__(self,jelo,kolicina):
        self.jelo = jelo
        self.kolicina = kolicina

class udarci(db.Model):
    __tablename__ = 'udarci'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    broj_udaraca = db.Column(db.Integer)

    def __init__(self,created_date,broj_udaraca):
        self.created_date = created_date
        self.broj_udaraca = broj_udaraca

@app.route('/')

def index():
    podaci = db.session.query(korisnik.id , korisnik.datum).all()
    return render_template('index.html', data = podaci)

@app.route('/datum_zadnjeg_ciklusa', methods=['POST'])
#prva funkcija za unos početka trudnoće
def submit():
    if request.method == 'POST':
        datum = request.form['datum']
        if datum == '':
            podaci = db.session.query(korisnik.id,korisnik.datum).all()
            return render_template('index.html', data = podaci , message ='Polje Datum ne može biti prazno!')
        if db.session.query(korisnik).count() >= 1:
            podaci = db.session.query(korisnik.id,korisnik.datum).all()
            return render_template('index.html', data = podaci , message ='Već je unešen datum! Promijenite postojeći datum.')
        data = korisnik(datum)
        db.session.add(data)
        db.session.commit()
        podaci = db.session.query(korisnik.id,korisnik.datum).all()
        return render_template('index.html',  data = podaci)

@app.route('/unesi_biljeske', methods=['POST'])
#dodavanje bilješki u bazu 
def unesi_biljeske():
    opis = request.form['opis']
    if opis == "":
        podaci = db.session.query(dnevnik.created_date,dnevnik.biljeska).all()
        return render_template('biljeske.html',data = podaci , message = 'Polje Bilješka ne može biti prazno!') 
    created_date = datetime.now()
    podatak = dnevnik(created_date,opis)
    db.session.add(podatak)
    db.session.commit()
    podaci = db.session.query(dnevnik.created_date,dnevnik.biljeska).all()
    return render_template('biljeske.html',data = podaci) 

@app.route('/unesi_kilazu', methods=['POST'])
#dodavanje kilaže u bazu podataka
def unesi_kilazu():
    if request.method == 'POST':
        kilaza_broj =request.form['kile']
        if kilaza_broj == '':
            podaci = db.session.query(kilaza.created_date,kilaza.kilaza).all()
            return render_template('kilaza.html',data = podaci,message = "Polje Kilaža ne može biti prazno!") 
        created_date = datetime.now()
        data = kilaza(created_date,kilaza_broj)
        db.session.add(data)
        db.session.commit()
        podaci = db.session.query(kilaza.created_date,kilaza.kilaza).all()
        return render_template('kilaza.html',data = podaci)


@app.route('/unesi_jelo', methods=['POST'])
#dodavanje novog jela u bazu podataka
def unesi_jelo():
    if request.method == 'POST':
        jelo = request.form['jelo']
        kolicina = request.form['kolicina']
        if jelo == '' or kolicina == '':
            podaci = db.session.query(jelovnik.id,jelovnik.jelo,jelovnik.kolicina).all()
            return render_template('jelovnik.html',data = podaci,message = "Polja Jelo i Količina ne mogu biti prazni!")
        data = jelovnik(jelo,kolicina)
        db.session.add(data)
        db.session.commit()
        podaci = db.session.query(jelovnik.id,jelovnik.jelo,jelovnik.kolicina).all()
        return render_template('jelovnik.html',data = podaci)

@app.route('/unesi_udarce', methods=['POST'])
#dodavanje novih udaraca u bazu podataka
def unesi_udarce():
    if request.method == 'POST':
        created_date = datetime.now()
        br_udaraca = request.form['udarci']
        if br_udaraca == '':
            podaci = db.session.query(udarci.created_date,udarci.broj_udaraca).all()
            return render_template('udarci.html',data = podaci,message="Polje Broj udaraca ne može biti prazno!")
        data = udarci(created_date,br_udaraca)
        db.session.add(data)
        db.session.commit()
        podaci = db.session.query(udarci.created_date,udarci.broj_udaraca).all()
        return render_template('udarci.html',data = podaci)

#update funckije
@app.route('/update_datuma', methods=['POST'])

def update_datuma():
    if request.method == 'POST':
        id_broj = request.form["id"]
        datum = request.form["datum"]
        if datum == '':
            podaci = db.session.query(korisnik.id,korisnik.datum).all()
            return render_template('index.html', data = podaci , message ='Polje Datum ne može biti prazno!')
        db.session.query(korisnik).filter(korisnik.id == id_broj).update({"datum": (datum)})
        db.session.commit()
        podaci = db.session.query(korisnik.id , korisnik.datum).all()
        return render_template('index.html',data = podaci)

@app.route('/update_biljeski', methods=['POST'])

def update_biljeski():
    if request.method == 'POST':
        datum = request.form["datumivrijeme"]
        opis = request.form["opis"]
        if opis == "":
            podaci = db.session.query(dnevnik.created_date,dnevnik.biljeska).all()
            return render_template('biljeske.html',data = podaci , message = 'Polje Bilješka ne može biti prazno!')
        db.session.query(dnevnik).filter(dnevnik.created_date == datum).update({"biljeska":(opis)})
        db.session.commit()
        podaci = db.session.query(dnevnik.created_date,dnevnik.biljeska).all()
        return render_template('biljeske.html',data = podaci)

@app.route('/update_jelovnika', methods=['POST'])

def update_jelovnika():
    if request.method == 'POST':
        id_num = request.form["id"]
        jelo = request.form["jelo"]
        kolicina = request.form["kolicina"]
        if jelo == '' or kolicina == '':
            podaci = db.session.query(jelovnik.id,jelovnik.jelo,jelovnik.kolicina).all()
            return render_template('jelovnik.html',data = podaci,message = "Polja Jelo i Količina ne mogu biti prazni!")
        db.session.query(jelovnik).filter(jelovnik.id == id_num).update({"jelo":(jelo)})
        db.session.query(jelovnik).filter(jelovnik.id == id_num).update({"kolicina":(kolicina)})
        db.session.commit()
        podaci = db.session.query(jelovnik.id,jelovnik.jelo,jelovnik.kolicina).all()
        return render_template('jelovnik.html',data = podaci)

@app.route('/update_udaraca', methods=['POST'])
def update_udaraca():
    if request.method == 'POST':
        datum = request.form["datum"]
        udarci_broj = request.form["udarci"]
        if udarci_broj == '':
            podaci = db.session.query(udarci.created_date,udarci.broj_udaraca).all()
            return render_template('udarci.html',data = podaci,message="Polje Broj udaraca ne može biti prazno!")
        db.session.query(udarci).filter(udarci.created_date == datum).update({"broj_udaraca":(udarci_broj)})
        db.session.commit()
        podaci = db.session.query(udarci.created_date,udarci.broj_udaraca).all()
        return render_template('udarci.html',data = podaci)

@app.route('/update_kilaze', methods=['POST'])
def update_kilaze():
    if request.method == 'POST':
        datum = request.form["datumivrijeme"]
        kile = request.form["kile"]
        if kile == '':
            podaci = db.session.query(kilaza.created_date,kilaza.kilaza).all()
            return render_template('kilaza.html',data = podaci,message = "Polje Kilaža ne može biti prazno!")
        db.session.query(kilaza).filter(kilaza.created_date == datum).update({"kilaza":(kile)})
        db.session.commit()
        podaci = db.session.query(kilaza.created_date,kilaza.kilaza).all()
        return render_template('kilaza.html',data = podaci)

#delete funckije
@app.route('/delete_datuma', methods=['POST'])

def delete_datuma():
    if request.method == 'POST':
        id_broj = request.form["id"]
        datum = request.form["datum"]
        if datum == '':
            podaci = db.session.query(korisnik.id,korisnik.datum).all()
            return render_template('index.html', data = podaci , message ='Polje Datum ne može biti prazno!')
        naden = db.session.query(korisnik).filter(korisnik.id == id_broj).first()
        db.session.delete(naden)
        db.session.commit()
        podaci = db.session.query(korisnik.id , korisnik.datum).all()
        return render_template('index.html',data = podaci)

@app.route('/delete_biljeski', methods=['POST'])

def delete_biljeski():
    if request.method == 'POST':
        datum = request.form["datumivrijeme"]
        opis = request.form["opis"]
        if opis == "":
            podaci = db.session.query(dnevnik.created_date,dnevnik.biljeska).all()
            return render_template('biljeske.html',data = podaci , message = 'Polje Bilješka ne može biti prazno!')
        nadena = db.session.query(dnevnik).filter(dnevnik.created_date == datum).first()
        db.session.delete(nadena)
        db.session.commit()
        podaci = db.session.query(dnevnik.created_date,dnevnik.biljeska).all()
        return render_template('biljeske.html',data = podaci)

@app.route('/delete_jelovnika', methods=['POST'])

def delete_jelovnika():
    if request.method == 'POST':
        id_num = request.form["id"]
        jelo = request.form["jelo"]
        kolicina = request.form["kolicina"]
        if jelo == '' or kolicina == '':
            podaci = db.session.query(jelovnik.id,jelovnik.jelo,jelovnik.kolicina).all()
            return render_template('jelovnik.html',data = podaci,message = "Polja Jelo i Količina ne mogu biti prazni!")
        nadeno = db.session.query(jelovnik).filter(jelovnik.id == id_num).first()
        db.session.delete(nadeno)
        db.session.commit()
        podaci = db.session.query(jelovnik.id,jelovnik.jelo,jelovnik.kolicina).all()
        return render_template('jelovnik.html',data = podaci)


@app.route('/delete_udaraca', methods=['POST'])

def delete_udaraca():
    if request.method == 'POST':
        datum = request.form["datum"]
        udarci_broj = request.form["udarci"]
        if udarci_broj == '':
            podaci = db.session.query(udarci.created_date,udarci.broj_udaraca).all()
            return render_template('udarci.html',data = podaci,message="Polje Broj udaraca ne može biti prazno!")
        nadena = db.session.query(udarci).filter(udarci.created_date == datum).first()
        db.session.delete(nadena)
        db.session.commit()
        podaci = db.session.query(udarci.created_date,udarci.broj_udaraca).all()
        return render_template('udarci.html',data = podaci)

@app.route('/delete_kilaze', methods=['POST'])
def delete_kilaze():
    if request.method == 'POST':
        datum = request.form["datumivrijeme"]
        kile = request.form["kile"]
        if kile == '':
            podaci = db.session.query(kilaza.created_date,kilaza.kilaza).all()
            return render_template('kilaza.html',data = podaci,message = "Polje Kilaža ne može biti prazno!")
        nadena = db.session.query(kilaza).filter(kilaza.created_date == datum).first()
        db.session.delete(nadena)
        db.session.commit()
        podaci = db.session.query(kilaza.created_date,kilaza.kilaza).all()
        return render_template('kilaza.html',data = podaci)

#meni sa ponovnim zahtjevom za ispis podataka za traženu stranicu
@app.route('/prikazi_biljeske', methods=['POST'])
def biljeske_prikaz():
    podaci = db.session.query(dnevnik.created_date,dnevnik.biljeska).all()
    return render_template('biljeske.html',data = podaci)

@app.route('/kilaza_prikaz', methods=['POST'])
def kilaza_prikaz():
    podaci = db.session.query(kilaza.created_date,kilaza.kilaza).all()
    return render_template('kilaza.html',data = podaci)

@app.route('/jela_prikaz', methods=['POST'])
def jela_prikaz():
    podaci = db.session.query(jelovnik.id,jelovnik.jelo,jelovnik.kolicina).all()
    return render_template('jelovnik.html',data = podaci)
    
@app.route('/udarci_prikaz', methods=['POST'])
def udarci_prikaz():
    podaci = db.session.query(udarci.created_date,udarci.broj_udaraca).all()
    return render_template('udarci.html',data = podaci)

@app.route('/ciklus_prikaz', methods=['POST'])
def ciklus_prikaz():
    podaci = db.session.query(korisnik.id , korisnik.datum).all()
    return render_template('index.html',data = podaci)

@app.route('/statistika_prikaz', methods=['POST'])
def statistika_prikaz():
    for row in db.session.execute(select(korisnik)).first():
        datum = row.datum
    novi_dat = datum + timedelta(270)

    broj = db.session.query(udarci.created_date).count()
    return render_template('statistika.html', datum_rodenja = novi_dat, broj=broj)

@app.route('/biljeske_sort', methods=['POST'])
def biljeske_sort():
    for row in db.session.execute(select(korisnik)).first():
        datum = row.datum
    novi_dat = datum + timedelta(270)
    broj = db.session.query(udarci.created_date).count()
    prvi_datum = request.form["date"]
    drugi_datum = request.form["date1"]

    data = db.session.query(dnevnik.created_date,dnevnik.biljeska).filter(dnevnik.created_date > prvi_datum).filter(dnevnik.created_date < drugi_datum).all()
    return render_template('statistika.html',datum_rodenja = novi_dat, data = data, broj=broj)

@app.route('/kilaza_sort', methods=['POST'])
def kilaza_sort():
    for row in db.session.execute(select(korisnik)).first():
        datum = row.datum
    novi_dat = datum + timedelta(270)
    broj = db.session.query(udarci.created_date).count()
    prvi_datum_kilaza = request.form["date2"]
    drugi_datum_kilaza = request.form["date3"]

    podaci = db.session.query(kilaza.created_date,kilaza.kilaza).filter(kilaza.created_date > prvi_datum_kilaza).filter(kilaza.created_date < drugi_datum_kilaza).all()
    return render_template('statistika.html',datum_rodenja = novi_dat, data1=podaci ,broj=broj)

@app.route('/udarci_sort', methods=['POST'])
def udarci_sort():
    for row in db.session.execute(select(korisnik)).first():
        datum = row.datum
    novi_dat = datum + timedelta(270)

    prvi_datum_udarca = request.form["date4"]
    drugi_datum_udarca = request.form["date5"]

    podaci = db.session.query(udarci.created_date,udarci.broj_udaraca).filter(udarci.created_date > prvi_datum_udarca).filter(udarci.created_date < drugi_datum_udarca).all()
    broj = db.session.query(udarci.created_date).count()
    return render_template('statistika.html',datum_rodenja = novi_dat, data2=podaci, broj=broj)

if __name__ == '__main__':
    
    app.run()