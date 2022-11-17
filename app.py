import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from dateutil import relativedelta
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://heitorsarmento:qwerty.123@db4free.net/guia_vacinas"

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")

mail = Mail(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


class Vacinas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    origem = db.Column(db.String(1000), nullable=False)
    beneficio = db.Column(db.String(1000), nullable=False)
    periodo_aplicacao = db.Column(db.String(1000), nullable=False)
    mes_aplicacao = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f'<Vacina {self.nome}>'


@app.route("/")
def index():
    return render_template("index.html")


#TODO: incluir session, salvar vacinas ja aplicadas


@app.route("/guia", methods=["GET", "POST"])
def guia():
    if request.method == "POST":
        nomeBebe = request.form.get("nomeBebe")
        nomeMae = request.form.get("nomeMae")
        email = request.form.get("email")

        # TODO: melhorar manipulação de datas

        dataNascBebe = datetime.strptime(request.form.get("dataNascBebe"),
                                         "%Y-%m-%d")
        dataAtual = datetime.strptime(str(date.today()), "%Y-%m-%d")
        deltaIdadeBebe = relativedelta.relativedelta(dataAtual, dataNascBebe)
        idadeBebe = deltaIdadeBebe.months + (deltaIdadeBebe.years * 12)
        diasBebe = deltaIdadeBebe.days + (deltaIdadeBebe.months *
                                          30) + (deltaIdadeBebe.years * 365)

        lista_vacinas = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/0/%') +
            Vacinas.mes_aplicacao.like('%/1/%'))
        lista_vacinas2 = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/2/%'))
        lista_vacinas3 = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/3/%'))
        lista_vacinas4 = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/4/%'))
        lista_vacinas5 = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/5/%'))
        lista_vacinas6 = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/6/%'))
        lista_vacinas7 = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/7/%'))
        lista_vacinas8 = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/9/%'))
        lista_vacinas9 = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/12/%'))
        lista_vacinas10 = Vacinas.query.filter(
            Vacinas.mes_aplicacao.like('%/15/%'))

        if request.form.get("termos") == "on":
            user = User(nome=nomeMae, email=email)
            db.session.add(user)
            db.session.commit()

            msg = Message("Olá %s, você está recebendo o Guia de Vacinação!" %
                          (nomeMae.upper()),
                          sender=("Guia de Vacinação - HeitorMS",
                                  os.environ.get("MAIL_USERNAME")),
                          recipients=[email])
            msg.html = render_template("guia_email.html",
                                       lista_vacinas=lista_vacinas,
                                       lista_vacinas2=lista_vacinas2,
                                       lista_vacinas3=lista_vacinas3,
                                       lista_vacinas4=lista_vacinas4,
                                       lista_vacinas5=lista_vacinas5,
                                       lista_vacinas6=lista_vacinas6,
                                       lista_vacinas7=lista_vacinas7,
                                       lista_vacinas8=lista_vacinas8,
                                       lista_vacinas9=lista_vacinas9,
                                       lista_vacinas10=lista_vacinas10,
                                       nomeBebe=nomeBebe,
                                       nomeMae=nomeMae,
                                       idadeBebe=idadeBebe,
                                       diasBebe=diasBebe)
            mail.send(msg)

        return render_template("guia.html",
                               lista_vacinas=lista_vacinas,
                               lista_vacinas2=lista_vacinas2,
                               lista_vacinas3=lista_vacinas3,
                               lista_vacinas4=lista_vacinas4,
                               lista_vacinas5=lista_vacinas5,
                               lista_vacinas6=lista_vacinas6,
                               lista_vacinas7=lista_vacinas7,
                               lista_vacinas8=lista_vacinas8,
                               lista_vacinas9=lista_vacinas9,
                               lista_vacinas10=lista_vacinas10,
                               nomeBebe=nomeBebe,
                               nomeMae=nomeMae,
                               idadeBebe=idadeBebe,
                               diasBebe=diasBebe)
