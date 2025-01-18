import logging

_configured = False

def setup_logging():
    global _configured
    if _configured:
        return
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(filename)s %(lineno)d %(message)s',
                        handlers=[logging.FileHandler(filename="app.log",mode="w"),logging.StreamHandler()])
    _configured = True

def get_logger(name):
    return logging.getLogger(name)

