import time
import validators

from db import get_db_no_app


def export(user_id, status, remark, tag):
    db = get_db_no_app()
    urls = db.execute(
        'select url from url_record where status = 0'
    )
    db.commit()
    start = time.perf_counter()
    with open('export', 'r') as f:
        for l in f:
            url = l.rstrip('\n').rstrip().split('\t')[0]
            if validators.url(url):
                db.execute(
                    'INSERT INTO url_record (url, user_id, status, remark, tag)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (url, user_id, status, remark, tag)
                )
                db.commit()

    end = time.process_time()
    times = (end-start)

export(1, 0, 'batch', 'default')