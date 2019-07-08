
from db import get_db, get_db_no_app


def analysis_url():
    db = get_db_no_app()
    urls = db.execute(
        'select url from url_record where status = 0'
    )
    db.commit()
    # for url in urls:
    #     res = urlparse(tuple(url)[0])
    #
    #     netlocs = db.execute(
    #         "select netloc from url_analysis where scheme = ? and netloc = ?",
    #         (res[0], res[1])
    #     ).fetchall()
    #     db.commit()
    #
    #     if netlocs.__len__()==0:
    #         db.execute(
    #             'INSERT INTO url_analysis (scheme, netloc)'
    #             ' VALUES (?, ?)',
    #             (res[0], res[1])
    #         )
    #         db.commit()
    #
    #     for netloc in netlocs:
    #         print(tuple(netloc)[0])
    #
    #     pass

analysis_url()
