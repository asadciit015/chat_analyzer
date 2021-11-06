import os, json
from flask import Flask, render_template, request, send_from_directory, abort
from parser import HTMLParser, InvalidHtmlException

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route("/process_html", methods=("POST",))
def process_html():
    if request.method == 'POST':
        html_file = request.files['html_file']
        html_string = html_file.read()
        try:
            parser = HTMLParser(html=html_string)
            graph_data = parser.graph_data
        except InvalidHtmlException as e:
            abort(500, e)
        # output_file_name = f"{html_file.name.replace('.html', '.json')}"
        output_file_name = "output.json"
        output_file_path = os.path.join(
            app.config['PARSED_JSON_FOLDER'], output_file_name
        )
        with open(output_file_path, 'w') as f:
            json.dump(graph_data, f, indent=2) 
        
        return send_from_directory(app.config['PARSED_JSON_FOLDER'],
            output_file_name, as_attachment=True
        )
    else:
        abort(404, "Error!")



# @app.route("/run_header_comparability")
# def run_header_comparability():
#     status = {}
#     return {
#         'success': True,
#         'msg': f"{status['files_checked']} files are scanned and {status['files_updated_count']} are updated!",
#         'files_updated': status['files_updated']
#     }
    

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html', error=error), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', error=error), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)