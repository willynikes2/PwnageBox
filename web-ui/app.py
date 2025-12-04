#!/usr/bin/env python3
"""
============================================================================
PwnageBox Web Controller
============================================================================
Flask application providing:
  - Public portfolio interface (viewable by anyone)
  - Password-protected attack trigger
  - Global rate limiting (45 seconds between attacks)
  - Docker container management for attack execution
============================================================================
"""

import os
import time
import threading
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================
RECRUITER_PASSWORD = os.getenv('RECRUITER_PASSWORD', 'YOURPASSWORD')
RATE_LIMIT_SECONDS = int(os.getenv('RATE_LIMIT_SECONDS', '45'))
PWNBOX_CONTAINER = 'pwnbox'

# =============================================================================
# Flask Application
# =============================================================================
app = Flask(__name__)

# Global state for rate limiting
class AttackState:
    def __init__(self):
        self.last_attack_time = 0
        self.attack_in_progress = False
        self.lock = threading.Lock()
    
    def can_attack(self):
        """Check if enough time has passed since the last attack."""
        with self.lock:
            current_time = time.time()
            time_since_last = current_time - self.last_attack_time
            return time_since_last >= RATE_LIMIT_SECONDS and not self.attack_in_progress
    
    def get_cooldown_remaining(self):
        """Get remaining cooldown time in seconds."""
        with self.lock:
            current_time = time.time()
            time_since_last = current_time - self.last_attack_time
            remaining = RATE_LIMIT_SECONDS - time_since_last
            return max(0, int(remaining))
    
    def start_attack(self):
        """Mark attack as started."""
        with self.lock:
            self.attack_in_progress = True
            self.last_attack_time = time.time()
    
    def end_attack(self):
        """Mark attack as completed."""
        with self.lock:
            self.attack_in_progress = False

attack_state = AttackState()


def restart_pwnbox_container():
    """Restart the pwnbox container to trigger a new attack."""
    try:
        import docker
        client = docker.from_env()
        
        # Find the pwnbox container
        try:
            container = client.containers.get(PWNBOX_CONTAINER)
            logger.info(f"Found container: {container.name} (status: {container.status})")
            
            # Restart the container
            container.restart(timeout=10)
            logger.info(f"Container {PWNBOX_CONTAINER} restarted successfully")
            return True, "Attack chain initiated successfully"
            
        except docker.errors.NotFound:
            logger.error(f"Container {PWNBOX_CONTAINER} not found")
            return False, f"Container '{PWNBOX_CONTAINER}' not found"
            
    except docker.errors.DockerException as e:
        logger.error(f"Docker error: {e}")
        return False, f"Docker error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False, f"Error: {str(e)}"


# =============================================================================
# Routes
# =============================================================================

@app.route('/')
def index():
    """Serve the main portfolio page."""
    return render_template('index.html', 
                          rate_limit=RATE_LIMIT_SECONDS)


@app.route('/status')
def status():
    """Get current system status."""
    cooldown = attack_state.get_cooldown_remaining()
    
    return jsonify({
        'status': 'online',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'can_attack': attack_state.can_attack(),
        'cooldown_remaining': cooldown,
        'attack_in_progress': attack_state.attack_in_progress
    })


@app.route('/launch_attack', methods=['POST'])
def launch_attack():
    """
    Launch the attack chain.
    Requires:
      - Valid password in JSON body
      - Rate limit cooldown to have passed
    """
    # Get JSON payload
    data = request.get_json()
    
    if not data:
        logger.warning("Attack request with no JSON body")
        return jsonify({
            'success': False,
            'error': 'Missing request body'
        }), 400
    
    # Verify password
    password = data.get('password', '')
    
    if password != RECRUITER_PASSWORD:
        logger.warning(f"Invalid password attempt from {request.remote_addr}")
        return jsonify({
            'success': False,
            'error': 'Access Denied: Invalid authorization code'
        }), 401
    
    # Check rate limit
    if not attack_state.can_attack():
        cooldown = attack_state.get_cooldown_remaining()
        
        if attack_state.attack_in_progress:
            return jsonify({
                'success': False,
                'error': 'Attack already in progress',
                'cooldown_remaining': cooldown
            }), 429
        else:
            return jsonify({
                'success': False,
                'error': f'Rate limited. Please wait {cooldown} seconds.',
                'cooldown_remaining': cooldown
            }), 429
    
    # Start the attack
    attack_state.start_attack()
    logger.info(f"Attack initiated by {request.remote_addr}")
    
    # Restart pwnbox container in a separate thread
    def run_attack():
        try:
            success, message = restart_pwnbox_container()
            if not success:
                logger.error(f"Attack failed: {message}")
        finally:
            # Give the container time to complete
            time.sleep(30)
            attack_state.end_attack()
    
    thread = threading.Thread(target=run_attack, daemon=True)
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Attack chain initialized. Check Splunk dashboard for real-time updates.',
        'next_available': RATE_LIMIT_SECONDS
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'pwnagebox-web-ui',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })


# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("PwnageBox Web Controller Starting")
    logger.info(f"Rate Limit: {RATE_LIMIT_SECONDS} seconds")
    logger.info(f"Password Protected: Yes")
    logger.info("=" * 60)
    
    # Run Flask development server (gunicorn used in production)
    app.run(host='0.0.0.0', port=5000, debug=False)
