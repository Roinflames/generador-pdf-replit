import os
import logging

from flask import Flask, render_template, request, redirect, url_for, flash, session
from deploy import DeploymentManager

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret")

# Create deployment manager
deployment_manager = DeploymentManager()

@app.route('/', methods=['GET'])
def index():
    """
    Main page with a form to input GitHub repository URL.
    """
    return render_template('index.html')

@app.route('/deploy', methods=['POST'])
def deploy():
    """
    Handle deployment form submission.
    """
    repo_url = request.form.get('repo_url')
    branch = request.form.get('branch', 'main')
    
    if not repo_url:
        flash('Please provide a valid GitHub repository URL', 'danger')
        return redirect(url_for('index'))
    
    logger.debug(f"Deploying repo: {repo_url}, branch: {branch}")
    
    try:
        # Store info in session for results page
        session['repo_url'] = repo_url
        session['branch'] = branch
        
        # Clone repo and set up the app
        result = deployment_manager.deploy(repo_url, branch)
        
        if result['success']:
            flash('Deployment successful!', 'success')
            session['deployment_logs'] = result['logs']
            return redirect(url_for('success'))
        else:
            flash(f'Deployment failed: {result["error"]}', 'danger')
            session['error_message'] = result['error']
            session['deployment_logs'] = result['logs']
            return redirect(url_for('error'))
            
    except Exception as e:
        logger.exception("Deployment failed with exception")
        flash(f'Unexpected error: {str(e)}', 'danger')
        session['error_message'] = str(e)
        return redirect(url_for('error'))

@app.route('/success')
def success():
    """
    Show success page with deployment details.
    """
    if 'repo_url' not in session:
        return redirect(url_for('index'))
        
    return render_template(
        'success.html',
        repo_url=session.get('repo_url'),
        branch=session.get('branch'),
        logs=session.get('deployment_logs', [])
    )

@app.route('/error')
def error():
    """
    Show error page with deployment error details.
    """
    if 'error_message' not in session:
        return redirect(url_for('index'))
        
    return render_template(
        'error.html',
        repo_url=session.get('repo_url'),
        branch=session.get('branch'),
        error=session.get('error_message'),
        logs=session.get('deployment_logs', [])
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
