import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

## 获取数据源
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

## 关闭数据源
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

## 初始化数据源
def init_db():
    db = get_db()

    with open('schema.sql') as f:
        db.executescript(f.read())

## 初始化数据库
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

## 初始化数据
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
