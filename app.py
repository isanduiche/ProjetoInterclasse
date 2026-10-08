from datetime import  datetime

from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select

from banco import tabela_time, tabela_jogador, tabela_partida
from database import *
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times = tabela_time.select_quantidade_total()
    jogadores = tabela_jogador.select_quantidade_total()
    partidas = tabela_partida.select_quantidade_total()

    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas,
    )


@app.route("/jogadores")
def listar_jogadores():
    jogadores = tabela_jogador.select_todos()

    return render_template("jogadores.html", jogadores=jogadores)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        if not nome:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('novo_jogador'))

        if not numero_camisa:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('novo_jogador'))

        if not posicao:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('novo_jogador'))

        if not time_id:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('novo_jogador'))

        tabela_jogador.salvar(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)

    times = tabela_time.select_todos()
    jogadores = tabela_jogador.select_todos()

    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/times")
def listar_times():
    times = tabela_time.select_todos()

    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        # 1- Pegar os valores do form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        # 2- Verificar se foi digitado
        if not nome:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('novo_time'))

        if not turma:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('novo_time'))

        if not responsavel:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('novo_time'))

        # 3- Salvar no banco
        tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

    # Buscar todos os times no banco
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():

    partidas = tabela_partida.select_todos()
    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        print(data_partida)
        #date_partida = datetime.strptime(data_partida, '%Y-%m-%d').date()

        if not time_casa_id:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('nova_partida'))

        if not time_visitante_id:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('nova_partida'))

        if not gols_casa:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('nova_partida'))

        if not gols_visitante:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('nova_partida'))

        if not data_partida:
            flash('Preencha o campo!', 'error')
            return redirect(url_for('nova_partida'))

        if time_visitante_id == time_casa_id:
            flash('Selecione um time diferente!', 'error')
            return redirect(url_for('nova_partida'))

        tabela_partida.salvar(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    times = tabela_time.select_todos()
    partidas = tabela_partida.select_todos()

    return render_template("partidas.html", partidas=partidas, times=times)


if __name__ == "__main__":
    app.run(debug=True)
