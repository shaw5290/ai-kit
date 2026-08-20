"""浏览器控制模块"""

from DrissionPage import Chromium
from typing import Optional, List, Dict, Any, Union
from .exceptions import BrowserError, ElementNotFoundError, PageLoadError
from .utils import setup_logger, validate_url

logger = setup_logger(__name__)


class BrowserClient:
    """
    浏览器控制客户端
    
    基于DrissionPage封装的浏览器控制功能，支持浏览器实例管理、标签页管理、页面操作、元素操作等
    """
    
    def __init__(self, headless: bool = False):
        """
        初始化浏览器客户端
        
        Args:
            headless: 是否以无头模式运行浏览器
        """
        self.headless = headless
        self.browser = None
        self.current_tab = None
    
    def start(self):
        """
        启动浏览器
        
        Raises:
            BrowserError: 浏览器启动失败
        """
        try:
            logger.info("启动浏览器")
            # 注意：DrissionPage的Chromium构造函数可能不接受headless参数
            # 这里使用默认初始化，不设置headless参数
            self.browser = Chromium()
            # 如果需要设置无头模式，可能需要使用其他方法
            # 例如：self.browser.set.headless(self.headless)
            self.current_tab = self.browser.latest_tab
            logger.info("浏览器启动成功")
        except Exception as e:
            logger.error(f"浏览器启动失败: {str(e)}")
            raise BrowserError(f"浏览器启动失败: {str(e)}")
    
    def stop(self):
        """
        关闭浏览器
        """
        if self.browser:
            try:
                logger.info("关闭浏览器")
                self.browser.quit()
                self.browser = None
                self.current_tab = None
                logger.info("浏览器关闭成功")
            except Exception as e:
                logger.error(f"浏览器关闭失败: {str(e)}")
    
    def new_tab(self, url: Optional[str] = None) -> Any:
        """
        新建标签页
        
        Args:
            url: 可选的初始URL
        
        Returns:
            新标签页对象
        
        Raises:
            BrowserError: 浏览器未启动
        """
        if not self.browser:
            raise BrowserError("浏览器未启动")
        
        try:
            if url and validate_url(url):
                logger.info(f"新建标签页并访问: {url}")
                tab = self.browser.new_tab(url)
            else:
                logger.info("新建空白标签页")
                tab = self.browser.new_tab()
            
            self.current_tab = tab
            return tab
        except Exception as e:
            logger.error(f"新建标签页失败: {str(e)}")
            raise BrowserError(f"新建标签页失败: {str(e)}")
    
    def switch_tab(self, index: Optional[int] = None, title: Optional[str] = None) -> Any:
        """
        切换标签页
        
        Args:
            index: 标签页索引
            title: 标签页标题
        
        Returns:
            切换后的标签页对象
        
        Raises:
            BrowserError: 浏览器未启动或标签页未找到
        """
        if not self.browser:
            raise BrowserError("浏览器未启动")
        
        try:
            if title:
                logger.info(f"根据标题切换标签页: {title}")
                tab = self.browser.get_tab(title=title)
            elif index is not None:
                logger.info(f"根据索引切换标签页: {index}")
                tabs = self.browser.tabs
                if 0 <= index < len(tabs):
                    tab = tabs[index]
                else:
                    raise BrowserError(f"标签页索引超出范围: {index}")
            else:
                raise BrowserError("必须提供标签页索引或标题")
            
            self.current_tab = tab
            return tab
        except Exception as e:
            logger.error(f"切换标签页失败: {str(e)}")
            raise BrowserError(f"切换标签页失败: {str(e)}")
    
    def close_tab(self, index: Optional[int] = None, title: Optional[str] = None):
        """
        关闭标签页
        
        Args:
            index: 标签页索引
            title: 标签页标题
        
        Raises:
            BrowserError: 浏览器未启动或标签页未找到
        """
        if not self.browser:
            raise BrowserError("浏览器未启动")
        
        try:
            if title:
                logger.info(f"关闭标题为: {title} 的标签页")
                tab = self.browser.get_tab(title=title)
                tab.close()
            elif index is not None:
                logger.info(f"关闭索引为: {index} 的标签页")
                tabs = self.browser.tabs
                if 0 <= index < len(tabs):
                    tabs[index].close()
                else:
                    raise BrowserError(f"标签页索引超出范围: {index}")
            else:
                raise BrowserError("必须提供标签页索引或标题")
        except Exception as e:
            logger.error(f"关闭标签页失败: {str(e)}")
            raise BrowserError(f"关闭标签页失败: {str(e)}")
    
    def navigate(self, url: str):
        """
        访问URL
        
        Args:
            url: 要访问的URL
        
        Raises:
            BrowserError: 浏览器未启动
            PageLoadError: 页面加载失败
        """
        if not self.browser or not self.current_tab:
            raise BrowserError("浏览器未启动")
        
        if not validate_url(url):
            raise PageLoadError(f"无效的URL: {url}")
        
        try:
            logger.info(f"访问URL: {url}")
            self.current_tab.get(url)
            logger.info("页面加载成功")
        except Exception as e:
            logger.error(f"页面加载失败: {str(e)}")
            raise PageLoadError(f"页面加载失败: {str(e)}")
    
    def refresh(self):
        """
        刷新当前页面
        
        Raises:
            BrowserError: 浏览器未启动
        """
        if not self.browser or not self.current_tab:
            raise BrowserError("浏览器未启动")
        
        try:
            logger.info("刷新当前页面")
            self.current_tab.refresh()
            logger.info("页面刷新成功")
        except Exception as e:
            logger.error(f"页面刷新失败: {str(e)}")
            raise BrowserError(f"页面刷新失败: {str(e)}")
    
    def go_back(self):
        """
        后退到上一页
        
        Raises:
            BrowserError: 浏览器未启动
        """
        if not self.browser or not self.current_tab:
            raise BrowserError("浏览器未启动")
        
        try:
            logger.info("后退到上一页")
            self.current_tab.back()
            logger.info("后退成功")
        except Exception as e:
            logger.error(f"后退失败: {str(e)}")
            raise BrowserError(f"后退失败: {str(e)}")
    
    def go_forward(self):
        """
        前进到下一页
        
        Raises:
            BrowserError: 浏览器未启动
        """
        if not self.browser or not self.current_tab:
            raise BrowserError("浏览器未启动")
        
        try:
            logger.info("前进到下一页")
            self.current_tab.forward()
            logger.info("前进成功")
        except Exception as e:
            logger.error(f"前进失败: {str(e)}")
            raise BrowserError(f"前进失败: {str(e)}")
    
    def find_element(self, selector: str, timeout: int = 10) -> Any:
        """
        查找元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（秒）
        
        Returns:
            元素对象
        
        Raises:
            BrowserError: 浏览器未启动
            ElementNotFoundError: 元素未找到
        """
        if not self.browser or not self.current_tab:
            raise BrowserError("浏览器未启动")
        
        try:
            logger.info(f"查找元素: {selector}")
            # 注意：DrissionPage的元素选择器语法可能与预期不同
            # 尝试使用不同的选择器语法
            
            # 1. 尝试直接使用选择器
            element = self.current_tab.ele(selector)
            if element:
                logger.info("元素查找成功")
                return element
            
            # 2. 尝试使用tag:前缀
            element = self.current_tab.ele(f"tag:{selector}")
            if element:
                logger.info("元素查找成功")
                return element
            
            # 3. 尝试使用css:前缀
            element = self.current_tab.ele(f"css:{selector}")
            if element:
                logger.info("元素查找成功")
                return element
            
            # 如果所有尝试都失败，抛出异常
            raise ElementNotFoundError(f"元素未找到: {selector}")
        except ElementNotFoundError:
            raise
        except Exception as e:
            logger.error(f"查找元素失败: {str(e)}")
            raise ElementNotFoundError(f"查找元素失败: {str(e)}")
    
    def find_elements(self, selector: str, timeout: int = 10) -> List[Any]:
        """
        查找多个元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（秒）
        
        Returns:
            元素对象列表
        
        Raises:
            BrowserError: 浏览器未启动
        """
        if not self.browser or not self.current_tab:
            raise BrowserError("浏览器未启动")
        
        try:
            logger.info(f"查找多个元素: {selector}")
            # 注意：DrissionPage的元素选择器语法可能与预期不同
            # 尝试使用不同的选择器语法
            
            # 1. 尝试直接使用选择器
            elements = self.current_tab.eles(selector)
            if elements:
                logger.info(f"找到 {len(elements)} 个元素")
                return elements
            
            # 2. 尝试使用tag:前缀
            elements = self.current_tab.eles(f"tag:{selector}")
            if elements:
                logger.info(f"找到 {len(elements)} 个元素")
                return elements
            
            # 3. 尝试使用css:前缀
            elements = self.current_tab.eles(f"css:{selector}")
            if elements:
                logger.info(f"找到 {len(elements)} 个元素")
                return elements
            
            # 如果所有尝试都失败，返回空列表
            logger.info("未找到元素，返回空列表")
            return []
        except Exception as e:
            logger.error(f"查找多个元素失败: {str(e)}")
            raise BrowserError(f"查找多个元素失败: {str(e)}")
    
    def click_element(self, selector: str):
        """
        点击元素
        
        Args:
            selector: 元素选择器
        
        Raises:
            BrowserError: 浏览器未启动
            ElementNotFoundError: 元素未找到
        """
        element = self.find_element(selector)
        try:
            logger.info(f"点击元素: {selector}")
            element.click()
            logger.info("元素点击成功")
        except Exception as e:
            logger.error(f"点击元素失败: {str(e)}")
            raise BrowserError(f"点击元素失败: {str(e)}")
    
    def input_text(self, selector: str, text: str):
        """
        输入文本
        
        Args:
            selector: 元素选择器
            text: 要输入的文本
        
        Raises:
            BrowserError: 浏览器未启动
            ElementNotFoundError: 元素未找到
        """
        element = self.find_element(selector)
        try:
            logger.info(f"向元素输入文本: {selector}")
            element.input(text)
            logger.info("文本输入成功")
        except Exception as e:
            logger.error(f"输入文本失败: {str(e)}")
            raise BrowserError(f"输入文本失败: {str(e)}")
    
    def get_element_text(self, selector: str) -> str:
        """
        获取元素文本
        
        Args:
            selector: 元素选择器
        
        Returns:
            元素文本
        
        Raises:
            BrowserError: 浏览器未启动
            ElementNotFoundError: 元素未找到
        """
        element = self.find_element(selector)
        try:
            text = element.text
            logger.info(f"获取元素文本成功: {text}")
            return text
        except Exception as e:
            logger.error(f"获取元素文本失败: {str(e)}")
            raise BrowserError(f"获取元素文本失败: {str(e)}")
    
    def get_element_attribute(self, selector: str, attribute: str) -> str:
        """
        获取元素属性
        
        Args:
            selector: 元素选择器
            attribute: 属性名
        
        Returns:
            属性值
        
        Raises:
            BrowserError: 浏览器未启动
            ElementNotFoundError: 元素未找到
        """
        element = self.find_element(selector)
        try:
            value = element.attr(attribute)
            logger.info(f"获取元素属性成功: {attribute} = {value}")
            return value
        except Exception as e:
            logger.error(f"获取元素属性失败: {str(e)}")
            raise BrowserError(f"获取元素属性失败: {str(e)}")
    
    def submit_form(self, selector: str):
        """
        提交表单
        
        Args:
            selector: 表单选择器
        
        Raises:
            BrowserError: 浏览器未启动
            ElementNotFoundError: 表单未找到
        """
        form = self.find_element(selector)
        try:
            logger.info(f"提交表单: {selector}")
            form.submit()
            logger.info("表单提交成功")
        except Exception as e:
            logger.error(f"表单提交失败: {str(e)}")
            raise BrowserError(f"表单提交失败: {str(e)}")
    
    def get_page_source(self) -> str:
        """
        获取当前页面源代码
        
        Returns:
            页面源代码
        
        Raises:
            BrowserError: 浏览器未启动
        """
        if not self.browser or not self.current_tab:
            raise BrowserError("浏览器未启动")
        
        try:
            logger.info("获取页面源代码")
            source = self.current_tab.html
            logger.info("获取页面源代码成功")
            return source
        except Exception as e:
            logger.error(f"获取页面源代码失败: {str(e)}")
            raise BrowserError(f"获取页面源代码失败: {str(e)}")
    
    def get_page_title(self) -> str:
        """
        获取当前页面标题
        
        Returns:
            页面标题
        
        Raises:
            BrowserError: 浏览器未启动
        """
        if not self.browser or not self.current_tab:
            raise BrowserError("浏览器未启动")
        
        try:
            title = self.current_tab.title
            logger.info(f"获取页面标题成功: {title}")
            return title
        except Exception as e:
            logger.error(f"获取页面标题失败: {str(e)}")
            raise BrowserError(f"获取页面标题失败: {str(e)}")
