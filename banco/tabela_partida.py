from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import Partida, db_session, Time


def select_todos():
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_sql = (
        select(Partida, TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
    )
    partida_casa = db_session.execute(partidas_sql).all()
    return partida_casa

def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    qtd_total = db_session.execute(partidas_sql).scalar()
    return qtd_total
print(select_quantidade_total())


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