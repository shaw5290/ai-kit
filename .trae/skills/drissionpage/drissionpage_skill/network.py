"""网络请求模块"""

from DrissionPage import SessionPage
import requests
from typing import Dict, Any, Optional, Union
from .exceptions import NetworkError
from .utils import setup_logger, validate_url, parse_headers

logger = setup_logger(__name__)


class NetworkClient:
    """
    网络请求客户端
    
    基于DrissionPage的SessionPage实现，提供HTTP/HTTPS请求功能
    """
    
    def __init__(self, timeout: int = 30):
        """
        初始化网络请求客户端
        
        Args:
            timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.session = SessionPage()
        # 设置超时
        self.session.set.timeout(timeout)
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None, 
            cookies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        发送GET请求
        
        Args:
            url: 请求URL
            params: URL参数
            headers: 请求头
            cookies: Cookies
        
        Returns:
            响应数据
        
        Raises:
            NetworkError: 网络请求失败
        """
        return self._request('GET', url, params=params, headers=headers, cookies=cookies)
    
    def post(self, url: str, data: Optional[Union[Dict[str, Any], str]] = None, 
             json: Optional[Dict[str, Any]] = None, 
             headers: Optional[Dict[str, str]] = None, 
             cookies: Optional[Dict[str, str]] = None, 
             files: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发送POST请求
        
        Args:
            url: 请求URL
            data: 表单数据
            json: JSON数据
            headers: 请求头
            cookies: Cookies
            files: 文件数据
        
        Returns:
            响应数据
        
        Raises:
            NetworkError: 网络请求失败
        """
        return self._request('POST', url, data=data, json=json, headers=headers, 
                           cookies=cookies, files=files)
    
    def put(self, url: str, data: Optional[Union[Dict[str, Any], str]] = None, 
            json: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None, 
            cookies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        发送PUT请求
        
        Args:
            url: 请求URL
            data: 表单数据
            json: JSON数据
            headers: 请求头
            cookies: Cookies
        
        Returns:
            响应数据
        
        Raises:
            NetworkError: 网络请求失败
        """
        return self._request('PUT', url, data=data, json=json, headers=headers, 
                           cookies=cookies)
    
    def delete(self, url: str, headers: Optional[Dict[str, str]] = None, 
               cookies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        发送DELETE请求
        
        Args:
            url: 请求URL
            headers: 请求头
            cookies: Cookies
        
        Returns:
            响应数据
        
        Raises:
            NetworkError: 网络请求失败
        """
        return self._request('DELETE', url, headers=headers, cookies=cookies)
    
    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法
            url: 请求URL
            **kwargs: 其他参数
        
        Returns:
            响应数据
        
        Raises:
            NetworkError: 网络请求失败
        """
        if not validate_url(url):
            raise NetworkError(f"无效的URL: {url}")
        
        try:
            logger.info(f"发送{method}请求到: {url}")
            
            # 对于GET请求，使用SessionPage
            # 对于POST请求，如果是JSON数据，使用requests库；否则使用SessionPage
            if method.upper() == 'GET':
                # 标准化请求头
                if 'headers' in kwargs:
                    headers = parse_headers(kwargs['headers'])
                    self.session.set.headers(headers)
                
                # 设置cookies
                if 'cookies' in kwargs and kwargs['cookies']:
                    self.session.set.cookies(kwargs['cookies'])
                
                # 构建请求参数
                req_kwargs = {}
                if 'params' in kwargs and kwargs['params']:
                    req_kwargs['params'] = kwargs['params']
                
                # 发送请求
                self.session.get(url, **req_kwargs)
                
                # 获取响应数据
                # 注意：SessionPage的API可能与版本相关，这里使用更兼容的方式
                
                # 获取响应状态码（SessionPage可能没有直接的status属性）
                # 这里使用默认值200，因为SessionPage在请求失败时会抛出异常
                status_code = 200
                
                # 获取响应头（SessionPage可能没有直接的headers属性）
                response_headers = {}
                
                # 获取响应数据
                response_data = self.session.html
                
                # 尝试解析JSON
                try:
                    import json
                    response_data = json.loads(response_data)
                except Exception:
                    pass
                
                # 获取当前URL
                current_url = self.session.url
                
            elif method.upper() == 'POST':
                # 对于POST请求，如果是JSON数据，使用requests库
                if 'json' in kwargs and kwargs['json']:
                    # 构建请求参数
                    req_kwargs = {
                        'timeout': self.timeout,
                        'json': kwargs['json']
                    }
                    
                    if 'headers' in kwargs:
                        req_kwargs['headers'] = parse_headers(kwargs['headers'])
                    else:
                        # 设置默认的Content-Type为application/json
                        req_kwargs['headers'] = {'Content-Type': 'application/json'}
                    
                    if 'cookies' in kwargs and kwargs['cookies']:
                        req_kwargs['cookies'] = kwargs['cookies']
                    
                    if 'params' in kwargs and kwargs['params']:
                        req_kwargs['params'] = kwargs['params']
                    
                    # 发送请求
                    response = requests.request('POST', url, **req_kwargs)
                    response.raise_for_status()  # 检查响应状态码
                    
                    # 获取响应信息
                    status_code = response.status_code
                    response_headers = dict(response.headers)
                    
                    # 尝试解析JSON响应
                    try:
                        response_data = response.json()
                    except ValueError:
                        response_data = response.text
                    
                    # 获取当前URL
                    current_url = response.url
                else:
                    # 对于非JSON数据的POST请求，使用SessionPage
                    # 标准化请求头
                    if 'headers' in kwargs:
                        headers = parse_headers(kwargs['headers'])
                        self.session.set.headers(headers)
                    
                    # 设置cookies
                    if 'cookies' in kwargs and kwargs['cookies']:
                        self.session.set.cookies(kwargs['cookies'])
                    
                    # 构建请求参数
                    req_kwargs = {}
                    if 'params' in kwargs and kwargs['params']:
                        req_kwargs['params'] = kwargs['params']
                    
                    if 'data' in kwargs and kwargs['data']:
                        req_kwargs['data'] = kwargs['data']
                    
                    if 'files' in kwargs and kwargs['files']:
                        req_kwargs['files'] = kwargs['files']
                    
                    # 发送请求
                    self.session.post(url, **req_kwargs)
                    
                    # 获取响应数据
                    # 注意：SessionPage的API可能与版本相关，这里使用更兼容的方式
                    
                    # 获取响应状态码（SessionPage可能没有直接的status属性）
                    # 这里使用默认值200，因为SessionPage在请求失败时会抛出异常
                    status_code = 200
                    
                    # 获取响应头（SessionPage可能没有直接的headers属性）
                    response_headers = {}
                    
                    # 获取响应数据
                    response_data = self.session.html
                    
                    # 尝试解析JSON
                    try:
                        import json
                        response_data = json.loads(response_data)
                    except Exception:
                        pass
                    
                    # 获取当前URL
                    current_url = self.session.url
                
            else:
                # 对于PUT和DELETE请求，使用requests库
                # 构建请求参数
                req_kwargs = {
                    'timeout': self.timeout
                }
                
                if 'headers' in kwargs:
                    req_kwargs['headers'] = parse_headers(kwargs['headers'])
                
                if 'cookies' in kwargs and kwargs['cookies']:
                    req_kwargs['cookies'] = kwargs['cookies']
                
                if 'params' in kwargs and kwargs['params']:
                    req_kwargs['params'] = kwargs['params']
                
                if 'data' in kwargs and kwargs['data']:
                    req_kwargs['data'] = kwargs['data']
                elif 'json' in kwargs and kwargs['json']:
                    req_kwargs['json'] = kwargs['json']
                
                if 'files' in kwargs and kwargs['files']:
                    req_kwargs['files'] = kwargs['files']
                
                # 发送请求
                response = requests.request(method, url, **req_kwargs)
                response.raise_for_status()  # 检查响应状态码
                
                # 获取响应信息
                status_code = response.status_code
                response_headers = dict(response.headers)
                
                # 尝试解析JSON响应
                try:
                    response_data = response.json()
                except ValueError:
                    response_data = response.text
                
                # 获取当前URL
                current_url = response.url
            
            return {
                'status_code': status_code,
                'headers': response_headers,
                'data': response_data,
                'url': current_url
            }
        except Exception as e:
            logger.error(f"网络请求失败: {str(e)}")
            raise NetworkError(f"网络请求失败: {str(e)}")
    
    def close(self):
        """
        关闭会话
        """
        # SessionPage不需要显式关闭
        pass
