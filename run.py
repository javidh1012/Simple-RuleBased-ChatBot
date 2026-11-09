"""
run.py - Single-command launcher for Student Academic Assistant.
Starts the Flask chatbot application at http://127.0.0.1:5000.
"""

import os
from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print("🎓 STUDENT ACADEMIC ASSISTANT - FLASK CHATBOT")
    print("=" * 70)
    print("• Architecture: Python Flask + HTML5 + Bootstrap 5 + Vanilla JS")
    print("• Dataset: Kaggle Student Academic Performance (2,000 students)")
    print("• Rule Engine: 100% Deterministic Python Conditional Statements")
    print(f"• Local Web App: http://127.0.0.1:{port}")
    print("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=True)
