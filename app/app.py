from flask import Flask, render_template, redirect, url_for, session, flash
import subprocess
import sys
import os
import secrets

app = Flask(__name__)
# IMPORTANT: Remeber to change this to a real random key in production
app.secret_key = secrets.token_hex(16)

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
        process = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,  # Capture stdout and stderr
            text=True,            # Decode output as text
            check=True,           # Raise CalledProcessError if script exits with non-zero code
            timeout=30            # Prevent hanging indefinitely
        )

        # Process the output
        output_lines = process.stdout.strip().splitlines()
        # Convert captured strings to integers
        results = [int(line) for line in output_lines if line.strip().isdigit()]
        print(f"Script finished successfully. Output: {results}")

        # Store results in the session
        session['simulation_results'] = results
        flash('Simulation ran successfully!', 'success') # success message

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