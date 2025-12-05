import os
import sys

# 1/ klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '1'))

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
