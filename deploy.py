import os
import subprocess
import logging
import tempfile
import shutil
import sys
from urllib.parse import urlparse
import time

logger = logging.getLogger(__name__)

class DeploymentManager:
    """
    Class to handle the deployment of a Flask application from GitHub
    """
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.logs = []
    
    def _log(self, message):
        """
        Add message to logs and print to console
        """
        self.logs.append(message)
        logger.info(message)
    
    def _run_command(self, command, cwd=None):
        """
        Run a shell command and capture output
        """
        self._log(f"Running command: {' '.join(command)}")
        try:
            # For pipenv requirements command with redirect, use shell=True
            if isinstance(command, list) and len(command) >= 3 and command[0] == "pipenv" and command[1] == "requirements" and ">" in command[2]:
                cmd_str = " ".join(command)
                process = subprocess.Popen(
                    cmd_str,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    text=True,
                    cwd=cwd
                )
            else:
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=cwd
                )
            
            # Stream output in real time and capture logs
            if process.stdout is not None and process.stderr is not None:
                while True:
                    output = process.stdout.readline()
                    error = process.stderr.readline()
                    
                    if output:
                        self._log(output.strip())
                    if error:
                        self._log(f"ERROR: {error.strip()}")
                        
                    # Break if process is done
                    if output == '' and error == '' and process.poll() is not None:
                        break
            
            return_code = process.poll()
            if return_code is not None and return_code != 0:
                raise subprocess.CalledProcessError(return_code, command)
            
            return True
        except subprocess.CalledProcessError as e:
            self._log(f"Command failed with code {e.returncode}")
            raise
    
    def _validate_github_url(self, url):
        """
        Validate that the URL is a GitHub repository URL
        """
        parsed = urlparse(url)
        
        # Basic validation
        if parsed.netloc not in ['github.com', 'www.github.com']:
            raise ValueError("Not a valid GitHub URL")
        
        # Extract owner and repo
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise ValueError("URL does not appear to be a valid repository path")
        
        owner = path_parts[0]
        repo = path_parts[1]
        
        # Ensure it's not just a user profile
        if not repo:
            raise ValueError("URL points to a user profile, not a repository")
        
        # Prepare clone URL
        if url.endswith('.git'):
            return url
        else:
            return f"https://github.com/{owner}/{repo}.git"
    
    def _check_if_flask_app(self, directory):
        """
        Check if the repository contains a Flask application
        """
        # Check for common Flask app indicators
        indicators = [
            os.path.exists(os.path.join(directory, 'app.py')),
            os.path.exists(os.path.join(directory, 'wsgi.py')),
            os.path.exists(os.path.join(directory, 'main.py')),
            os.path.exists(os.path.join(directory, 'run.py')),
            os.path.exists(os.path.join(directory, 'application.py'))
        ]
        
        # Check for Flask in requirements.txt
        req_path = os.path.join(directory, 'requirements.txt')
        if os.path.exists(req_path):
            with open(req_path, 'r') as f:
                if 'flask' in f.read().lower():
                    return True
        
        # Check for Flask in Pipfile
        pipfile_path = os.path.join(directory, 'Pipfile')
        if os.path.exists(pipfile_path):
            with open(pipfile_path, 'r') as f:
                if 'flask' in f.read().lower():
                    return True
        
        return any(indicators)
    
    def _find_app_entrypoint(self, directory):
        """
        Find the main application entry point
        """
        possible_files = ['app.py', 'main.py', 'wsgi.py', 'run.py', 'application.py']
        
        for filename in possible_files:
            filepath = os.path.join(directory, filename)
            if os.path.exists(filepath):
                # Check if file contains Flask app definition
                with open(filepath, 'r') as f:
                    content = f.read()
                    if 'Flask(__name__)' in content or 'Flask(' in content:
                        return filename
        
        # Fallback to searching for any Python file with Flask in it
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r') as f:
                        content = f.read()
                        if 'Flask(__name__)' in content or 'Flask(' in content:
                            return os.path.relpath(filepath, directory)
        
        return None
    
    def _install_dependencies(self, directory):
        """
        Install Python dependencies from requirements.txt or Pipfile
        """
        req_path = os.path.join(directory, 'requirements.txt')
        pipfile_path = os.path.join(directory, 'Pipfile')
        
        if os.path.exists(pipfile_path):
            self._log("Pipfile detected, installing dependencies with pipenv")
            # Check if pipenv is installed, if not install it
            try:
                self._run_command(["pipenv", "--version"], cwd=directory)
            except:
                self._log("Installing pipenv")
                self._run_command([sys.executable, "-m", "pip", "install", "pipenv"], cwd=directory)
            
            # Install dependencies using pipenv with the Python version available in Replit
            self._log("Installing dependencies using pipenv with Python " + sys.version.split()[0])
            # Specify the current Python interpreter to pipenv
            self._run_command(["pipenv", "--python", sys.executable, "install"], cwd=directory)
            
            # Create a requirements.txt file for Replit compatibility
            self._log("Creating requirements.txt from Pipfile for Replit compatibility")
            try:
                # Run pipenv requirements and save to requirements.txt
                process = subprocess.Popen(
                    ["pipenv", "requirements"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=directory
                )
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    # Write the output to requirements.txt
                    req_file_path = os.path.join(directory, "requirements.txt")
                    with open(req_file_path, "w") as f:
                        f.write(stdout)
                    self._log("Successfully created requirements.txt from Pipfile")
                else:
                    raise subprocess.CalledProcessError(process.returncode, ["pipenv", "requirements"])
            except:
                self._log("WARNING: Could not automatically create requirements.txt from Pipfile")
                # Manually install the common Flask dependencies
                self._run_command([sys.executable, "-m", "pip", "install", "Flask", "gunicorn"], cwd=directory)
        
        elif os.path.exists(req_path):
            self._log("Installing dependencies from requirements.txt")
            self._run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=directory)
        else:
            self._log("No requirements.txt or Pipfile found, installing Flask only")
            self._run_command([sys.executable, "-m", "pip", "install", "Flask"], cwd=directory)
    
    def _update_code_for_replit(self, directory, app_file):
        """
        Update code to ensure it works properly on Replit
        """
        file_path = os.path.join(directory, app_file)
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if there's a run or main block that needs to be updated
        if 'if __name__ == "__main__"' in content or 'if __name__ == \'__main__\'' in content:
            self._log(f"Updating {app_file} to run on correct host/port")
            
            lines = content.split('\n')
            updated_lines = []
            in_main_block = False
            modified = False
            
            for line in lines:
                if 'if __name__ == "__main__"' in line or 'if __name__ == \'__main__\'' in line:
                    in_main_block = True
                    updated_lines.append(line)
                elif in_main_block and ('.run(' in line or '.run()' in line):
                    # Replace with correct host/port
                    modified = True
                    updated_lines.append('    app.run(host="0.0.0.0", port=5000, debug=True)')
                else:
                    updated_lines.append(line)
            
            if modified:
                with open(file_path, 'w') as f:
                    f.write('\n'.join(updated_lines))
            else:
                # If we didn't find a run() call but found the main block,
                # add the proper run line at the end of the main block
                in_main_block = False
                updated_lines = []
                
                for line in lines:
                    updated_lines.append(line)
                    if 'if __name__ == "__main__"' in line or 'if __name__ == \'__main__\'' in line:
                        in_main_block = True
                    elif in_main_block and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                        # First non-indented line after main block
                        updated_lines.insert(len(updated_lines) - 1, '    app.run(host="0.0.0.0", port=5000, debug=True)')
                        in_main_block = False
                
                with open(file_path, 'w') as f:
                    f.write('\n'.join(updated_lines))
        else:
            # No main block found, add one
            with open(file_path, 'a') as f:
                f.write('\n\nif __name__ == "__main__":\n')
                f.write('    app.run(host="0.0.0.0", port=5000, debug=True)\n')
    
    def _copy_deployed_files(self, source_dir):
        """
        Copy deployed files to the current directory
        """
        # Copy everything except .git and .venv directories
        for item in os.listdir(source_dir):
            if item == '.git' or item == '.venv' or item.startswith('.virtualenvs'):
                continue
                
            source_item = os.path.join(source_dir, item)
            dest_item = os.path.join(self.base_dir, item)
            
            # Handle existing files/dirs
            if os.path.exists(dest_item):
                if os.path.isdir(dest_item):
                    shutil.rmtree(dest_item)
                else:
                    os.remove(dest_item)
            
            # Copy file or directory
            if os.path.isdir(source_item):
                shutil.copytree(source_item, dest_item)
            else:
                shutil.copy2(source_item, dest_item)
    
    def deploy(self, repo_url, branch="main"):
        """
        Deploy a Flask application from a GitHub repository
        
        Args:
            repo_url (str): GitHub repository URL
            branch (str): Branch to clone, defaults to "main"
            
        Returns:
            dict: Deployment results with success status, logs, and error message if applicable
        """
        self.logs = []
        temp_dir = None
        
        try:
            # Reset logs
            self._log(f"Starting deployment of {repo_url} ({branch} branch)")
            
            # Validate GitHub URL
            repo_url = self._validate_github_url(repo_url)
            self._log(f"Validated repository URL: {repo_url}")
            
            # Create temporary directory for cloning
            temp_dir = tempfile.mkdtemp()
            self._log(f"Created temporary directory: {temp_dir}")
            
            # Clone the repository
            self._log(f"Cloning repository {repo_url}, branch {branch}")
            clone_cmd = ["git", "clone", "-b", branch, repo_url, temp_dir]
            self._run_command(clone_cmd)
            
            # Check if it's a Flask app
            if not self._check_if_flask_app(temp_dir):
                raise ValueError("The repository does not appear to contain a Flask application")
            
            # Find the main app file
            app_file = self._find_app_entrypoint(temp_dir)
            if not app_file:
                raise ValueError("Could not find Flask application entry point")
            
            self._log(f"Found Flask application entry point: {app_file}")
            
            # Install dependencies
            self._install_dependencies(temp_dir)
            
            # Update code to work on Replit
            self._update_code_for_replit(temp_dir, app_file)
            
            # Copy files to current directory
            self._log("Copying deployed files to application directory")
            self._copy_deployed_files(temp_dir)
            
            self._log("Deployment completed successfully")
            
            return {
                "success": True,
                "logs": self.logs,
                "entry_point": app_file
            }
            
        except Exception as e:
            self._log(f"Deployment failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "logs": self.logs
            }
        finally:
            # Clean up
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                self._log("Cleaned up temporary directory")
