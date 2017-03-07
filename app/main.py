#!flask/bin/python
from app.performance_summary import app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
