import argparse,yaml
from utils.logger import setup_logging,get_logger
from utils.check_os import check
from utils.install_deps import install_deps
from utils.install_kubernetes import install_k8s
from utils.install_service import install_service

setup_logging()
logger = get_logger(__name__)

def init(conf):
    if check(conf):
        install_deps(conf)
        install_k8s(conf)
        install_service(conf)

if __name__ == "__main__":
    logger.info("laiye private deploy ... ")
    parser = argparse.ArgumentParser(prog="main.py",
                                     description="laiye private deploy program",
                                     usage='%(prog)s [options]')
    parser.add_argument("-c","--config",type=str,help="Path to the configuration file",required=True)
    parser.add_argument('--force',action='store_true', help='Force execution')
    args = parser.parse_args()
    config_file= args.config

    logger.info(f"Config file: {config_file}")
    try:
        with open(f"{config_file}",'r') as f :
            conf = yaml.safe_load(f)
    except Exception as ex:
        logger.error(ex)
        exit(127)
    init(conf)
        

    

    