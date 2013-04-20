"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views



# Examples list page
app.add_url_rule('/examples', 'list_examples', view_func=views.list_examples, methods=['GET', 'POST'])

# Examples list page (cached)
app.add_url_rule('/examples/cached', 'cached_examples', view_func=views.cached_examples, methods=['GET'])


# Edit an example
app.add_url_rule('/examples/<int:example_id>/edit', 'edit_example', view_func=views.edit_example, methods=['GET', 'POST'])

# Delete an example
app.add_url_rule('/examples/<int:example_id>/delete', view_func=views.delete_example, methods=['POST'])


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

