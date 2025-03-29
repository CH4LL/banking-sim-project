# 1. Import necessary parts from the Flask library
from flask import Flask, render_template

# 2. Create an instance of the Flask application
#    __name__ tells Flask where to look for resources like templates and static files.
app = Flask(__name__)

# 3. Define a "route" - what happens when someone visits the main URL ('/')
@app.route('/')
def index():
    #"""This function will run when someone accesses the root URL."""
    # 4. Tell Flask to find and return an HTML file named 'index.html'
    #    We'll create this file next. Flask automatically looks in a 'templates' folder.
    #    We can also pass variables to the template, like the page title here.
    page_title = "Banking Simulation Home"
    return render_template('index.html', title=page_title)

# 5. Boilerplate code to make the app runnable directly with "python app/app.py"
if __name__ == '__main__':
    # 6. Start the Flask development server
    #    debug=True enables auto-reloading when code changes and provides detailed error pages.
    #    host='0.0.0.0' makes the server accessible from other devices on your network (useful for testing).
    #                  If you omit it, it usually defaults to '127.0.0.1' (localhost), only accessible on your machine.
    app.run(debug=True, host='0.0.0.0')