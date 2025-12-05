import os
import sys

# 1/ klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '1'))

from app import create_app

print("Creating Flask app...")
app = create_app()
print("Flask app created successfully!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
