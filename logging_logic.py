# Configure daily rotating logging
from logging.handlers import TimedRotatingFileHandler
import logging
import traceback
from flask import request, session, make_response

def configure_logging(app):
    log_handler = TimedRotatingFileHandler(
    filename='app2_daily.log',
    when='midnight',            # Rotate at midnight
    interval=1,                 # Every 1 day
    backupCount=7              # Keep 7 days of logs
    )
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(log_handler)

    @app.before_request
    def log_before_request():
        user = session.get('user')
        method = request.method
        path = request.path
        try:
            if method == "GET":
                params = dict(request.args)
            else:
                params = dict(request.form)
            if 'pwd' in params:
                params['pwd'] = '***'
            logging.info(f"[BEFORE] User: {user} | Method: {method} | Path: {path} | Params: {params}")
        except Exception as e:
            logging.warning(f"[BEFORE] Failed to log request: {e}")

    @app.after_request
    def log_after_request(response):
        user = session.get('user')
        path = request.path
        logging.info(f"[AFTER] User: {user} | Response Status: {response.status} | Path: {path}")
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        user = session.get('user')
        path = request.path
        stack = traceback.format_exc()
        status_code = getattr(e, 'code', 500)
        logging.error(f"[ERROR] User: {user} | Path: {path} | Exception: {str(e)} | Status Code: {status_code} | Stack Trace:{stack}")
        return make_response(f"Internal Server Error: {str(e)}", status_code)