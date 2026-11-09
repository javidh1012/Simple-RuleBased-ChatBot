"""
backend/main.py - Entrypoint mapping to root app.py.
Maintains backward compatibility for runners invoking backend/main.py.
"""

import sys
from pathlib import Path

# Add root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app import app

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print("🎓 STUDENT ACADEMIC ASSISTANT - FLASK CHATBOT")
    print("=" * 70)
    print(f"• Local Web App: http://127.0.0.1:{port}")
    print("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=True)
