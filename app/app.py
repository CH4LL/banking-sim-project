# 1. Import necessary parts from the Flask library
from flask import Flask, render_template, redirect, url_for, session, flash
import subprocess
import sys
import os
import secrets

# 2. Create an instance of the Flask application
#    __name__ tells Flask where to look for resources like templates and static files.
app = Flask(__name__)
# IMPORTANT: Remeber to change this to a real random key in production
app.secret_key = secrets.token_hex(16)

# 3. Define a "route" - what happens when someone visits the main URL ('/')
@app.route('/')
def index():
    #render main page
    page_title = "Banking Simulation Home"
    # Get results from session if they exist, otherwise default to None
    simulation_results = session.pop('simulation_results', None)
    return render_template('index.html', title=page_title, results=simulation_results)

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    # Runs test data generation and stores results in session
    print("received request to run simulation...")
    # Construct the absolute path to the script
    # __file__ is the path to app.py
    # os.path.dirname gets the directory containing app.py (i.e., banking_sim/app)
    # os.path.abspath ensures we have a full path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, '..', 'scripts', 'generate_test_data.py')
    print(f"Attempting to run script: {script_path}")

    try:
        # Run the script using the same Python interpreter that runs Flask
        # sys.executable points to the python.exe within your venv
        process = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,  # Capture stdout and stderr
            text=True,            # Decode output as text (usually UTF-8)
            check=True,           # Raise CalledProcessError if script exits with non-zero code
            timeout=30            # Optional: Prevent hanging indefinitely (in seconds)
        )

        # Process the output (printed lines from the script)
        output_lines = process.stdout.strip().splitlines()
        # Convert captured strings to integers (or floats if needed)
        results = [int(line) for line in output_lines if line.strip().isdigit()]
        print(f"Script finished successfully. Output: {results}")

        # Store results in the session
        session['simulation_results'] = results
        flash('Simulation ran successfully!', 'success') # Optional success message

    except FileNotFoundError:
        print(f"Error: Script not found at {script_path}")
        flash(f'Error: Script not found at {script_path}', 'error')
    except subprocess.CalledProcessError as e:
        print(f"Error during script execution: {e}")
        print(f"Stderr: {e.stderr}")
        flash(f'Error running simulation script: {e.stderr}', 'error')
    except subprocess.TimeoutExpired:
        print("Error: Script execution timed out.")
        flash('Error: Simulation script took too long to run.', 'error')
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        flash(f'An unexpected error occurred: {e}', 'error')

    # Redirect back to the homepage regardless of success/failure
    return redirect(url_for('index'))

# 5. Boilerplate code to make the app runnable directly with "python app/app.py"
if __name__ == '__main__':
    # 6. Start the Flask development server
    #    debug=True enables auto-reloading when code changes and provides detailed error pages.
    #    host='0.0.0.0' makes the server accessible from other devices on your network (useful for testing).
    #                  If you omit it, it usually defaults to '127.0.0.1' (localhost), only accessible on your machine.
    app.run(debug=True, host='0.0.0.0')