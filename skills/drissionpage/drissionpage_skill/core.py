"""核心技能模块"""

from typing import Dict, Any, Optional, Union, List
from .browser import BrowserClient
from .network import NetworkClient
from .exceptions import DrissionPageSkillError
from .utils import setup_logger

logger = setup_logger(__name__)


class DrissionPageSkill:
    """
    DrissionPage技能模块
    
    集成网络请求和浏览器控制功能，提供统一的API接口
    """
    
    def __init__(self, timeout: int = 30, headless: bool = False):
        """
        初始化DrissionPage技能模块
        
        Args:
            timeout: 请求超时时间（秒）
            headless: 是否以无头模式运行浏览器
        """
        self.timeout = timeout
        self.headless = headless
        self.network_client = NetworkClient(timeout=timeout)
        self.browser_client = BrowserClient(headless=headless)
    
    # 网络请求方法
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
        """
        return self.network_client.get(url, params=params, headers=headers, cookies=cookies)
    
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
        """
        return self.network_client.post(url, data=data, json=json, headers=headers, 
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
        """
        return self.network_client.put(url, data=data, json=json, headers=headers, 
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
        """
        return self.network_client.delete(url, headers=headers, cookies=cookies)
    
    # 浏览器控制方法
    def start_browser(self):
        """
        启动浏览器
        """
        self.browser_client.start()
    
    def stop_browser(self):
        """
        关闭浏览器
        """
        self.browser_client.stop()
    
    def new_tab(self, url: Optional[str] = None) -> Any:
        """
        新建标签页
        
        Args:
            url: 可选的初始URL
        
        Returns:
            新标签页对象
        """
        return self.browser_client.new_tab(url)
    
    def switch_tab(self, index: Optional[int] = None, title: Optional[str] = None) -> Any:
        """
        切换标签页
        
        Args:
            index: 标签页索引
            title: 标签页标题
        
        Returns:
            切换后的标签页对象
        """
        return self.browser_client.switch_tab(index=index, title=title)
    
    def close_tab(self, index: Optional[int] = None, title: Optional[str] = None):
        """
        关闭标签页
        
        Args:
            index: 标签页索引
            title: 标签页标题
        """
        self.browser_client.close_tab(index=index, title=title)
    
    def navigate(self, url: str):
        """
        访问URL
        
        Args:
            url: 要访问的URL
        """
        self.browser_client.navigate(url)
    
    def refresh(self):
        """
        刷新当前页面
        """
        self.browser_client.refresh()
    
    def go_back(self):
        """
        后退到上一页
        """
        self.browser_client.go_back()
    
    def go_forward(self):
        """
        前进到下一页
        """
        self.browser_client.go_forward()
    
    def find_element(self, selector: str, timeout: int = 10) -> Any:
        """
        查找元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（秒）
        
        Returns:
            元素对象
        """
        return self.browser_client.find_element(selector, timeout=timeout)
    
    def find_elements(self, selector: str, timeout: int = 10) -> List[Any]:
        """
        查找多个元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（秒）
        
        Returns:
            元素对象列表
        """
        return self.browser_client.find_elements(selector, timeout=timeout)
    
    def click_element(self, selector: str):
        """
        点击元素
        
        Args:
            selector: 元素选择器
        """
        self.browser_client.click_element(selector)
    
    def input_text(self, selector: str, text: str):
        """
        输入文本
        
        Args:
            selector: 元素选择器
            text: 要输入的文本
        """
        self.browser_client.input_text(selector, text)
    
    def get_element_text(self, selector: str) -> str:
        """
        获取元素文本
        
        Args:
            selector: 元素选择器
        
        Returns:
            元素文本
        """
        return self.browser_client.get_element_text(selector)
    
    def get_element_attribute(self, selector: str, attribute: str) -> str:
        """
        获取元素属性
        
        Args:
            selector: 元素选择器
            attribute: 属性名
        
        Returns:
            属性值
        """
        return self.browser_client.get_element_attribute(selector, attribute)
    
    def submit_form(self, selector: str):
        """
        提交表单
        
        Args:
            selector: 表单选择器
        """
        self.browser_client.submit_form(selector)
    
    def get_page_source(self) -> str:
        """
        获取当前页面源代码
        
        Returns:
            页面源代码
        """
        return self.browser_client.get_page_source()
    
    def get_page_title(self) -> str:
        """
        获取当前页面标题
        
        Returns:
            页面标题
        """
        return self.browser_client.get_page_title()
    
    # 工具方法
    def close(self):
        """
        关闭所有资源
        """
        self.stop_browser()
        self.network_client.close()
    
    def __enter__(self):
        """
        上下文管理器入口
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器出口
        """
        self.close()
