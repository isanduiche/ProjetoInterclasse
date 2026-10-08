from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from database import Time, db_session, Jogador


def select_todos():
    times_sql = (
        select(Time, func.count(Jogador.id).label('jogadores'))
        .outerjoin(Jogador, Jogador.time_id == Time.id)
        .group_by(Time.id)
    )
    times = db_session.execute(times_sql).all()
    return times

def select_quantidade_total():
    times_sql = select(func.count(Time.id))
    qtd_total = db_session.execute(times_sql).scalar()
    return qtd_total
print(select_quantidade_total())

def salvar(nome, turma, responsavel):
    try:
        novo_time = Time(nome=nome, turma=turma, responsavel=responsavel)

        db_session.add(novo_time)
        db_session.commit()
        flash('Time adicionado com sucesso!', 'success')

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f'Erro ao cadastrar esse time: {e}')
        flash('Erro ao cadastrar esse time!', 'error')
    except Exception as e:
        db_session.rollback()
        print(f'Erro inesperado: {e}')
        flash('Erro inesperado!', 'error')