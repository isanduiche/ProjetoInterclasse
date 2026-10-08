from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from database import Jogador, db_session, Time


def select_todos():
    # 1 - Montar o select
    # Join(Tabela que eu quero juntar, condição = chaves estrangeira igual chave primaria)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    # 2 - Excutar o select
    # Usar Scalars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()
    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_session.execute(jogadores_sql).scalar()
    return qtd_total
print(select_quantidade_total())

def salvar(nome, numero_camisa, posicao, time_id):
    try:
        novo_jogador = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))

        db_session.add(novo_jogador)
        db_session.commit()
        flash('Jogador adicionado com sucesso!', 'success')

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f'Erro ao cadastrar esse jogador: {e}')
        flash('Erro ao cadastrar esse jogador!', 'error')
    except Exception as e:
        db_session.rollback()
        print(f'Erro inesperado: {e}')
        flash('Erro inesperado!', 'error')

