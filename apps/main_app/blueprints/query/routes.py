from flask import render_template, request
from . import query_app
from .models import QueryHandler


@query_app.route('/', methods=["GET"])
def handle_index():
    return render_template('query_index.html')

@query_app.route('/billboard_query', methods=["GET"])
def billboard_get_handler():
    return render_template('billboard_query_form.html')


@query_app.route('/billboard_query', methods=["POST"])
def billboard_post_handler():
    result = QueryHandler.process_user_input({
        'min_price': request.form['min_price'],
        'max_price': request.form['max_price'],
        'city': request.form['city'],
        'min_quality': request.form['min_quality'],
        'max_quality': request.form['max_quality'],
        'min_size': request.form['min_size'],
        'max_size': request.form['max_size']
    })
    if result.status:
        return render_template('billboard_query_result.html', search_results=result.result)
    return render_template('billboard_query_form.html', error=result.error_message)
