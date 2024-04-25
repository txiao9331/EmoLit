# http://127.0.0.1:5000/bestchoice_doc/

# http://10.10.10.143:5000/bestchoice_doc/

from flask import Flask, abort, request, render_template
import pymysql
import os
import math
from collections import defaultdict
from flask_basicauth import BasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)

swaggerui_blueprint = get_swaggerui_blueprint(
    base_url='/bestchoice_doc',
    api_url='/static/bookapi.yaml',
)
app.register_blueprint(swaggerui_blueprint)

def create_db_conn():
    db_conn = pymysql.connect(host="localhost"
                            , user="root"
                            , password=os.getenv('mysql_xt')
                            , database="littmental" 
                            , cursorclass=pymysql.cursors.DictCursor)
    return db_conn

@app.route('/v1')
def index():
    return render_template('index.html')

MAX_PAGE_SIZE = 30

@app.route("/v1/books")
def books():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_details = int(request.args.get('include_details', 0)) 
    db_conn=create_db_conn()

    with db_conn.cursor() as cursor:
        cursor.execute("""
                        select 
                            b.title as Title,
                            b.title_id,
                            author,
                            genre as genres,
                            publish_date,
                            pages,
                            format,
                            rating,
                            c.award
                        from book_info b
                        join choice_award c
                        on b.award_id = c.award_id
                        LIMIT %s OFFSET %s
            """,(page_size, (page - 1) * page_size))
        books = cursor.fetchall()

        books = [remove_null_fields(book) for book in books]
        title_ids = [book['title_id'] for book in books]

        more_infos_dict = defaultdict(list)

        if include_details:
            cursor.execute("""
                            select
                                title_id,
                                description
                            from book_info 
                            where title_id in (%s)
                            """% ','.join(['%s'] * len(title_ids)), title_ids)
            more_infos = cursor.fetchall()
            for info in more_infos:
                more_info = remove_null_fields(info)
                more_infos_dict[info['title_id']].append(more_info)

        for book in books:
            book['more_info'] = more_infos_dict.get(book['title_id'], [])

    query = "SELECT COUNT(*) AS total FROM book_info"  
    last_page = get_last_page(query,page_size)

    db_conn.close() 

    return {
        'books': books,
        'next_page': f'/books?page={page+1}&page_size={page_size}&include_details={include_details}',
        'last_page': f'/books?page={last_page}&page_size={page_size}&include_details={include_details}',
    }


@app.route("/v1/books/<int:title_id>")
def book(title_id):
    include_details = int(request.args.get('include_details', 0)) 
    db_conn=create_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute("""
                        select 
                            b.title as Title,
                            b.title_id,
                            author,
                            genre as genres,
                            publish_date,
                            pages,
                            format,
                            rating,
                            c.award
                        from book_info b
                        join choice_award c
                        on b.award_id = c.award_id
                        where b.title_id=%s
            """,(title_id,))
        book = cursor.fetchone()

        if book:
            book = remove_null_fields(book)
        else:
            abort(404)

        if include_details:
            # fetch more information
            cursor.execute("""
                            select
                                description
                            from book_info 
                            where title_id=%s
                            """,(title_id,))
            more_info = cursor.fetchone()
        else:
            more_info = {}

        book['more_info'] = more_info

    db_conn.close()
    return book

@app.route("/v1/awardslist")
def awardslist():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_details = int(request.args.get('include_details', 0)) 
    db_conn=create_db_conn()

    with db_conn.cursor() as cursor:
        cursor.execute("""
                        select *
                        from choice_award
                        LIMIT %s OFFSET %s
            """,(page_size, (page - 1) * page_size))
        awardslist = cursor.fetchall()
        awardslist = [remove_null_fields(list) for list in awardslist]

        award_ids = [award['award_id'] for award in awardslist]

        if include_details:
                # Fetch books associated with each award using the award IDs
                award_ids = [award['award_id'] for award in awardslist]
                if award_ids:
                    placeholders = ','.join(['%s'] * len(award_ids))
                    cursor.execute(f"""
                        SELECT 
                            title_id,
                            title,
                            author,
                            genre,
                            rating,
                            votes,
                            award_id
                        FROM book_info
                        WHERE award_id IN ({placeholders})
                    """, tuple(award_ids))
                    more_infos = cursor.fetchall()
                    # Map books to their respective awards
                    more_infos_dict = defaultdict(list)
                    for info in more_infos:
                        more_info = remove_null_fields(info)
                        more_infos_dict[info['award_id']].append(more_info)

                    # Attach book details to each award entry
                    for award in awardslist:
                        award['books'] = more_infos_dict.get(award['award_id'], [])

    query = "SELECT COUNT(*) AS total FROM choice_award"  
    last_page = get_last_page(query,page_size)

    db_conn.close() 

    return {
        'best_choice_award': awardslist,
        'next_page': f'/books?page={page+1}&page_size={page_size}&include_details={include_details}',
        'last_page': f'/books?page={last_page}&page_size={page_size}&include_details={include_details}',
    }


@app.route("/v1/awardslist/<int:year>")
def award(year):
    include_details = int(request.args.get('include_details', 0)) 
    db_conn=create_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute("""
                        select *
                        from choice_award
                        where year=%s
            """,(year))
        awards = cursor.fetchall()
        awards = [remove_null_fields(award) for award in awards]
        if include_details:
            # Fetch books associated with each award using the award IDs
            award_ids = [award['award_id'] for award in awards]
            placeholders = ','.join(['%s'] * len(award_ids))
            cursor.execute(f"""
                    SELECT 
                            title_id,
                            title,
                            author,
                            award_id
                    FROM book_info
                    WHERE award_id IN ({placeholders})
                """, tuple(award_ids))
            books = cursor.fetchall()

            # Map books to their respective awards
            books_dict = {}
            for book in books:
                book = remove_null_fields(book)
                if book['award_id'] not in books_dict:
                    books_dict[book['award_id']] = []
                books_dict[book['award_id']].append(book)

            # Attach book details to each award entry
            for award in awards:
                award['books'] = books_dict.get(award['award_id'], [])
    db_conn.close()
    return awards


@app.route("/v1/reviews/<int:title_id>")
def reviews(title_id):
    # include_details = int(request.args.get('include_details', 0)) 
    db_conn=create_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute("""
                        select *
                        from reviews
                        where title_id=%s
            """,(title_id,))
        review = cursor.fetchone()

        if review:
            review = remove_null_fields(review)
        else:
            abort(404)

    db_conn.close()
    return review



def remove_null_fields(obj):
    return {k:v for k, v in obj.items() if v is not None}

def get_last_page(query,page_size):
    db_conn=create_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(query)    
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
    db_conn.close()
    return last_page   

if __name__ == '__main__':
    app.run(debug=True)
