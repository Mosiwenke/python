"""
第43章: 日志与配置管理
=============================

日志与配置管理.
- logging
- configparser
- json配置
"""

import logging


def logging_config():
    """日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:%(message)s'
    )
    logging.info("日志信息")


def log_levels():
    """日志级别"""
    logging.debug("调试")
    logging.info("信息")
    logging.warning("警告")
    logging.error("错误")
    logging.critical("严重")


def config_parser():
    """配置解析"""
    import configparser
    
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'debug': 'true'}
    config['database'] = {'host': 'localhost'}
    
    print(f"host: {config['database']['host']}")


if __name__ == "__main__":
    print("=" * 50)
    print("43. 日志与配置")
    print("=" * 50)
    logging_config()
    print("\n--- 级别 ---")
    log_levels()
    print("\n--- 配置 ---")
    config_parser()
    print("=" * 50)