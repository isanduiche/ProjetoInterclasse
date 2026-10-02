from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database import Time, db_session


def select_todos():
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()
    return times

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