#!flask/bin/python
from app.performance_summary import app
from flask_bootstrap import Bootstrap
Bootstrap(app)

if __name__ == "__main__":
    app.run(debug=True, host='10.182.131.21', port=5011)
