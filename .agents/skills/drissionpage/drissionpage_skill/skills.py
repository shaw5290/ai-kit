"""
DrissionPage技能模块

根据官方文档的例子实现各种功能的用法
"""

from typing import Optional, Dict, Any, List
from DrissionPage import Chromium, SessionPage
from .exceptions import DrissionPageSkillError, BrowserError, NetworkError
from .utils import setup_logger

# 配置日志
logger = setup_logger(__name__)


class DrissionPageSkills:
    """
    DrissionPage技能类
    根据官方文档的例子实现各种功能的用法
    """
    
    def __init__(self):
        """
        初始化DrissionPage技能类
        """
        self.browser = None
        self.session = None
    
    def init_browser(self) -> Chromium:
        """
        初始化浏览器对象
        
        Returns:
            Chromium: 浏览器对象
        """
        try:
            logger.info("初始化浏览器对象")
            self.browser = Chromium()
            return self.browser
        except Exception as e:
            logger.error(f"初始化浏览器失败: {str(e)}")
            raise BrowserError(f"初始化浏览器失败: {str(e)}")
    
    def init_session(self) -> SessionPage:
        """
        初始化会话对象
        
        Returns:
            SessionPage: 会话对象
        """
        try:
            logger.info("初始化会话对象")
            self.session = SessionPage()
            return self.session
        except Exception as e:
            logger.error(f"初始化会话失败: {str(e)}")
            raise NetworkError(f"初始化会话失败: {str(e)}")
    
    def baidu_search(self, keyword: str) -> List[str]:
        """
        在百度搜索关键词并返回结果
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            List[str]: 搜索结果标题列表
        """
        try:
            logger.info(f"在百度搜索: {keyword}")
            # 初始化浏览器
            if not self.browser:
                self.init_browser()
            
            # 获取标签页
            tab = self.browser.latest_tab
            
            # 访问百度
            tab.get('https://www.baidu.com')
            
            # 输入关键词
            tab('#kw').input(keyword)
            
            # 点击搜索按钮
            tab('#su').click()
            
            # 获取搜索结果
            links = tab.eles('tag:h3')
            
            # 提取结果标题
            results = []
            for link in links:
                results.append(link.text)
            
            logger.info(f"搜索完成，找到 {len(results)} 个结果")
            return results
        except Exception as e:
            logger.error(f"百度搜索失败: {str(e)}")
            raise DrissionPageSkillError(f"百度搜索失败: {str(e)}")
    
    def http_get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        发送HTTP GET请求
        
        Args:
            url: 请求URL
            headers: 请求头
        
        Returns:
            Dict[str, Any]: 响应结果
        """
        try:
            logger.info(f"发送GET请求: {url}")
            # 初始化会话
            if not self.session:
                self.init_session()
            
            # 发送请求
            if headers:
                self.session.headers = headers
            
            # 访问URL
            self.session.get(url)
            
            # 构建响应结果
            # 注意：SessionPage对象的属性名可能与预期不同
            response = {
                'content': self.session.html
            }
            
            logger.info("GET请求完成")
            return response
        except Exception as e:
            logger.error(f"GET请求失败: {str(e)}")
            raise NetworkError(f"GET请求失败: {str(e)}")
    
    def http_post(self, url: str, data: Optional[Dict[str, Any]] = None, 
                  json: Optional[Dict[str, Any]] = None, 
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        发送HTTP POST请求
        
        Args:
            url: 请求URL
            data: 表单数据
            json: JSON数据
            headers: 请求头
        
        Returns:
            Dict[str, Any]: 响应结果
        """
        try:
            logger.info(f"发送POST请求: {url}")
            # 初始化会话
            if not self.session:
                self.init_session()
            
            # 发送请求
            if headers:
                self.session.headers = headers
            
            # 根据参数类型发送请求
            if json:
                # 使用JSON数据
                self.session.post(url, json=json)
            elif data:
                # 使用表单数据
                self.session.post(url, data=data)
            else:
                # 空请求
                self.session.post(url)
            
            # 构建响应结果
            # 注意：SessionPage对象的属性名可能与预期不同
            response = {
                'content': self.session.html
            }
            
            logger.info("POST请求完成")
            return response
        except Exception as e:
            logger.error(f"POST请求失败: {str(e)}")
            raise NetworkError(f"POST请求失败: {str(e)}")
    
    def browser_navigate(self, url: str) -> str:
        """
        使用浏览器访问网址并返回页面标题
        
        Args:
            url: 访问的URL
        
        Returns:
            str: 页面标题
        """
        try:
            logger.info(f"浏览器访问: {url}")
            # 初始化浏览器
            if not self.browser:
                self.init_browser()
            
            # 获取标签页
            tab = self.browser.latest_tab
            
            # 访问URL
            tab.get(url)
            
            # 获取页面标题
            title = tab.title
            
            logger.info(f"页面访问完成，标题: {title}")
            return title
        except Exception as e:
            logger.error(f"浏览器访问失败: {str(e)}")
            raise BrowserError(f"浏览器访问失败: {str(e)}")
    
    def get_element_text(self, url: str, selector: str) -> str:
        """
        获取指定URL页面中指定元素的文本
        
        Args:
            url: 页面URL
            selector: 元素选择器
        
        Returns:
            str: 元素文本
        """
        try:
            logger.info(f"获取元素文本: {url} - {selector}")
            # 初始化浏览器
            if not self.browser:
                self.init_browser()
            
            # 获取标签页
            tab = self.browser.latest_tab
            
            # 访问URL
            tab.get(url)
            
            # 获取元素 - 尝试多种选择器语法
            # 1. 尝试直接使用选择器
            element = tab.ele(selector)
            if element:
                text = element.text
                logger.info(f"元素文本获取成功: {text[:50]}...")
                return text
            
            # 2. 尝试使用tag:前缀
            element = tab.ele(f"tag:{selector}")
            if element:
                text = element.text
                logger.info(f"元素文本获取成功: {text[:50]}...")
                return text
            
            # 3. 尝试使用css:前缀
            element = tab.ele(f"css:{selector}")
            if element:
                text = element.text
                logger.info(f"元素文本获取成功: {text[:50]}...")
                return text
            
            # 如果所有尝试都失败，抛出异常
            raise DrissionPageSkillError(f"元素未找到: {selector}")
        except Exception as e:
            logger.error(f"获取元素文本失败: {str(e)}")
            raise DrissionPageSkillError(f"获取元素文本失败: {str(e)}")
    
    def close_browser(self):
        """
        关闭浏览器
        """
        try:
            if self.browser:
                logger.info("关闭浏览器")
                self.browser.quit()
                self.browser = None
                logger.info("浏览器关闭成功")
        except Exception as e:
            logger.error(f"关闭浏览器失败: {str(e)}")
            raise BrowserError(f"关闭浏览器失败: {str(e)}")
    
    def close_session(self):
        """
        关闭会话
        """
        try:
            if self.session:
                logger.info("关闭会话")
                # SessionPage不需要显式关闭
                self.session = None
                logger.info("会话关闭成功")
        except Exception as e:
            logger.error(f"关闭会话失败: {str(e)}")
            raise NetworkError(f"关闭会话失败: {str(e)}")
    
    def close_all(self):
        """
        关闭所有资源
        """
        try:
            self.close_browser()
            self.close_session()
            logger.info("所有资源关闭成功")
        except Exception as e:
            logger.error(f"关闭资源失败: {str(e)}")
            raise DrissionPageSkillError(f"关闭资源失败: {str(e)}")


# 导出技能类
__all__ = ['DrissionPageSkills']
