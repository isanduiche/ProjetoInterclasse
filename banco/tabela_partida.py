from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database import Partida, db_session


def select_todos():
    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()
    return partidas

def salvar(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida):
    try:
        nova_partida = Partida(time_casa_id=int(time_casa_id), time_visitante_id=int(time_visitante_id),gols_casa=int(gols_casa), gols_visitante=int(gols_visitante), data_partida=data_partida)

        db_session.add(nova_partida)
        db_session.commit()
        flash('Partida adicionada com sucesso!', 'success')

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f'Erro ao cadastrar esse jogador: {e}')
        flash('Erro ao cadastrar esse jogador!', 'error')
    except Exception as e:
        db_session.rollback()
        print(f'Erro inesperado: {e}')
        flash('Erro inesperado!', 'error')