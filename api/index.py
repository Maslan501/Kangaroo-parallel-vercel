"""
Bitcoin Puzzle Monitor API - Vercel Deployment
Includes Kangaroo v2.2+ Enhanced Monitoring Dashboard
"""

from flask import Flask, jsonify, render_template, send_from_directory, make_response
import os
import json
import glob
from datetime import datetime

app = Flask(__name__)

# Base directory for data files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_FILES_DIR = os.path.join(BASE_DIR, 'work_files')
SEARCH_ENGINE_DIR = os.path.join(BASE_DIR, 'search_engine')


# Helper functions
def get_work_files():
    """Get all Kangaroo work files"""
    try:
        work_files = glob.glob(os.path.join(WORK_FILES_DIR, 'kangaroo_work_*.json'))
        return work_files
    except:
        return []


def parse_work_file(file_path):
    """Parse a Kangaroo work file and extract statistics"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Extract puzzle number from filename
        filename = os.path.basename(file_path)
        parts = filename.replace('kangaroo_work_puzzle', '').replace('.json', '').split('_')
        puzzle_num = parts[0]
        zone = parts[1] if len(parts) > 1 else 'unknown'
        
        # Calculate progress
        range_width = data.get('range_end', 0) - data.get('range_start', 0)
        total_jumps = data.get('total_jumps', 0)
        
        if range_width > 0:
            expected_ops = 2 * int(range_width ** 0.5)
            progress = min(100, (total_jumps / expected_ops * 100) if expected_ops > 0 else 0)
        else:
            progress = 0
        
        return {
            'puzzle_num': puzzle_num,
            'zone': zone,
            'iterations': data.get('iterations', 0),
            'total_jumps': total_jumps,
            'dp_count': data.get('dp_count', 0),
            'num_kangaroos': data.get('num_kangaroos', 0),
            'tame_points': data.get('tame_points_count', 0),
            'wild_points': data.get('wild_points_count', 0),
            'progress': round(progress, 2),
            'timestamp': data.get('timestamp', ''),
            'range_bits': range_width.bit_length() if range_width > 0 else 0,
            'file_path': os.path.basename(file_path)
        }
    except Exception as e:
        return {'error': str(e), 'file_path': os.path.basename(file_path)}


def get_found_keys():
    """Get list of found keys"""
    found_file = os.path.join(WORK_FILES_DIR, 'FOUND_KEYS_KANGAROO.txt')
    
    if not os.path.exists(found_file):
        return []
    
    keys = []
    try:
        with open(found_file, 'r') as f:
            content = f.read()
        
        sections = content.split('='*80)
        for section in sections:
            if 'PUZZLE' in section and 'SOLVED' in section:
                lines = section.strip().split('\n')
                key_info = {}
                
                for line in lines:
                    if 'PUZZLE #' in line:
                        key_info['puzzle'] = line.split('#')[1].split()[0]
                    elif 'Timestamp:' in line:
                        key_info['timestamp'] = line.split('Timestamp:')[1].strip()
                    elif 'Private Key (Hex):' in line:
                        key_info['private_key_hex'] = line.split('Private Key (Hex):')[1].strip()
                    elif 'Address:' in line:
                        key_info['address'] = line.split('Address:')[1].strip()
                
                if key_info:
                    keys.append(key_info)
    except:
        pass
    
    return keys


# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    try:
        html = render_template('dashboard.html')
        response = make_response(html)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        return f"Error rendering template: {str(e)}", 500


@app.route('/test')
def test():
    """API test page"""
    return render_template('test_api.html')


@app.route('/simple')
def simple():
    """Simple test route"""
    return "<h1>Hello from Flask!</h1><p>This is a simple HTML response.</p>"


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '2.2+'})


@app.route('/api/status')
def api_status():
    """API endpoint for current search status"""
    work_files = get_work_files()
    
    active_searches = []
    for file_path in work_files:
        search_info = parse_work_file(file_path)
        if 'error' not in search_info:
            active_searches.append(search_info)
    
    # Sort by puzzle number
    active_searches.sort(key=lambda x: int(x['puzzle_num']))
    
    # Get found keys
    found_keys = get_found_keys()
    
    # Overall statistics
    total_jumps = sum(s['total_jumps'] for s in active_searches)
    total_dps = sum(s['dp_count'] for s in active_searches)
    avg_progress = sum(s['progress'] for s in active_searches) / len(active_searches) if active_searches else 0
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'active_searches': len(active_searches),
        'found_keys': len(found_keys),
        'total_jumps': total_jumps,
        'total_dps': total_dps,
        'avg_progress': round(avg_progress, 2),
        'searches': active_searches,
        'solved': found_keys
    })


@app.route('/api/search/<puzzle_num>')
def api_search_detail(puzzle_num):
    """API endpoint for specific search details"""
    work_files = get_work_files()
    
    for file_path in work_files:
        if f'puzzle{puzzle_num}_' in file_path:
            search_info = parse_work_file(file_path)
            return jsonify(search_info)
    
    return jsonify({'error': 'Search not found'}), 404


@app.route('/api/config')
def api_config():
    """API endpoint for configuration info"""
    return jsonify({
        'version': '2.2+',
        'algorithm': 'Enhanced Pollard\'s Kangaroo',
        'features': [
            'Multiple kangaroos (4 tame + 4 wild)',
            '32-way exponential jump distribution',
            'Work save/resume functionality',
            'Real-time progress tracking',
            'Distinguished point optimization'
        ],
        'target_puzzles': [135, 140, 145, 150, 155, 160],
        'search_zones': {
            'high': '20-30%',
            'medium': '40-50%',
            'low': '65-85%'
        }
    })


# For local testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
