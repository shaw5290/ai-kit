"""工具函数模块"""

import logging
import json
from typing import Dict, Any, Optional


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    配置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
    
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def validate_url(url: str) -> bool:
    """
    验证URL格式是否正确
    
    Args:
        url: 要验证的URL
    
    Returns:
        URL是否有效
    """
    return url.startswith(('http://', 'https://'))


def format_response_data(data: Any) -> str:
    """
    格式化响应数据
    
    Args:
        data: 响应数据
    
    Returns:
        格式化后的响应数据字符串
    """
    if isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False, indent=2)
    elif isinstance(data, (list, tuple)):
        return json.dumps(data, ensure_ascii=False, indent=2)
    else:
        return str(data)


def parse_headers(headers: Optional[Dict[str, str]]) -> Dict[str, str]:
    """
    解析并标准化请求头
    
    Args:
        headers: 原始请求头
    
    Returns:
        标准化后的请求头
    """
    if not headers:
        return {}
    
    # 确保请求头格式正确
    normalized_headers = {}
    for key, value in headers.items():
        normalized_headers[str(key)] = str(value)
    
    return normalized_headers
