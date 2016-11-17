import json
import requests
import sqlite3

from flask import Flask, render_template, request, Response
from reddit_predictor import get_prediction
app = Flask(__name__)

DB_PATH = '../reddit_data.db'
conn = sqlite3.connect(DB_PATH)
curs = conn.cursor()

@app.route('/')
def hello_world():
    return render_template("base.html")

@app.route("/basic", methods=["GET"])
def search_reddits():
    query = request.args.get('query')
    page = request.args.get('page')
    perpage = request.args.get('perpage')
    pagination, totalpages = False, None
    if query:
        sql = "SELECT * from reddit_posts where title like '%' || ? || '%' OR subreddit like '%' || ? || '%'"
        sql_args = (query, query)
        if page and perpage:
            sql += ' LIMIT ?, ?'
            sql_args += (int(perpage) * int(page), perpage)
            total_sql = "SELECT count(*) from reddit_posts where title like '%' || ? || '%'"
            count = curs.execute(total_sql, (query, ))
            total = count.fetchone()[0]
            pagination = True
            totalpages = (total / int(perpage)) + 1

        resp = curs.execute(sql, sql_args)
        results = dictfetchall(resp)

        return render_template("search.html", show_results=True, results=results,
                               query=query, pagination=pagination, totalpages=totalpages)
    else:
        return render_template('search.html')

@app.route("/intermediate", methods=["GET"])
def test_algo():
    chosen_subreddit = request.args.get('subreddit')
    post_id = request.args.get('postid')
    subreddits = get_subreddits()

    if chosen_subreddit:
        resp = curs.execute("SELECT * from reddit_posts where subreddit = ?", (chosen_subreddit,))
        posts = dictfetchall(resp)
        return render_template("testalgo.html", subreddits=subreddits,
                               posts=posts, chosen_subreddit=chosen_subreddit)

    if post_id:
        resp = curs.execute("SELECT * from reddit_posts where id = ?", (post_id,))
        post = dictfetchall(resp)[0]
        input_dict = {
            'title': post['title'],
            'subreddit': post['subreddit'],
            'domain': post['domain']
        }
        prediction = get_prediction(input_dict)
        return render_template("testalgo.html", subreddits=subreddits,
                               chosen_post=post, prediction=prediction)

    return render_template("testalgo.html", subreddits=subreddits)

@app.route("/advance", methods=["GET"])
def advance():
    external_subreddit = request.args.get('external_subreddit')
    subreddits = get_subreddits()

    if external_subreddit:
        posts = fetch_posts(external_subreddit)
        return render_template("testalgo_advance.html", external_subreddit=external_subreddit,
                               subreddits=subreddits,
                               external_posts=posts)

    return render_template("testalgo_advance.html", subreddits=subreddits)


@app.route("/predictor", methods=["POST"])
def predictor():
    predict_input = {
        'title': request.form.get('title'),
        'domain': request.form.get('domain'),
        'subreddit': request.form.get('subreddit')
    }
    response = {'prediction': get_prediction(predict_input)}
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype="application/json"
    )

# Helper functions

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_subreddits():
    resp = curs.execute("SELECT subreddit from subreddits")
    subreddits = [i[0] for i in resp]
    return subreddits

def fetch_posts(subreddit):
    '''
    Fetches posts from the reddit API
    '''
    url = 'https://www.reddit.com/r/%s/new.json' % subreddit
    resp = requests.get(url)
    resp = json.loads(resp.text)

    if resp.get('error') == 403:
        return []

    posts = []

    children = resp.get('data', {}).get('children', [])

    for child in children:
        posts.append({
            'subreddit': child['data']['subreddit'],
            'title': child['data']['title'],
            'domain': child['data']['domain'],
            'id': child['data']['id'],
            'ups': child['data']['ups']
        })

    return posts
