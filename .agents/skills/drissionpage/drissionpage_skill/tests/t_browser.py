"""浏览器控制模块测试"""

import unittest
from drissionpage_skill import DrissionPageSkill
from drissionpage_skill.exceptions import BrowserError, ElementNotFoundError


class TestBrowser(unittest.TestCase):
    """浏览器控制模块测试类"""
    
    def setUp(self):
        """测试前设置"""
        # 使用无头模式运行浏览器，避免测试时弹出浏览器窗口
        self.skill = DrissionPageSkill(headless=True)
    
    def tearDown(self):
        """测试后清理"""
        self.skill.close()
    
    def test_browser_start_stop(self):
        """测试浏览器启动和关闭"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 关闭浏览器
        self.skill.stop_browser()
    
    def test_new_tab(self):
        """测试新建标签页"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 新建标签页并访问URL
        url = "https://httpbin.org/get"
        tab = self.skill.new_tab(url)
        
        # 验证标签页对象被创建
        self.assertIsNotNone(tab)
    
    def test_navigate(self):
        """测试页面导航"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 访问URL
        url = "https://httpbin.org/get"
        self.skill.navigate(url)
        
        # 获取页面标题，验证页面是否加载成功
        title = self.skill.get_page_title()
        self.assertIsInstance(title, str)
    
    def test_refresh(self):
        """测试页面刷新"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 访问URL
        url = "https://httpbin.org/get"
        self.skill.navigate(url)
        
        # 刷新页面
        self.skill.refresh()
    
    def test_page_source(self):
        """测试获取页面源代码"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 访问URL
        url = "https://httpbin.org/get"
        self.skill.navigate(url)
        
        # 获取页面源代码
        source = self.skill.get_page_source()
        
        # 验证页面源代码是字符串
        self.assertIsInstance(source, str)
        # 验证页面源代码包含预期内容
        self.assertIn("httpbin.org", source)
    
    def test_page_title(self):
        """测试获取页面标题"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 访问URL
        url = "https://httpbin.org/get"
        self.skill.navigate(url)
        
        # 获取页面标题
        title = self.skill.get_page_title()
        
        # 验证页面标题是字符串
        self.assertIsInstance(title, str)
    
    def test_find_element(self):
        """测试查找元素"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 访问URL
        url = "https://httpbin.org/html"
        self.skill.navigate(url)
        
        # 查找元素 - 使用body元素作为测试，因为它肯定存在
        try:
            element = self.skill.find_element("body")
            # 验证元素被找到
            self.assertIsNotNone(element)
        except ElementNotFoundError:
            # 如果元素未找到，测试失败
            self.fail("元素未找到")
    
    def test_find_elements(self):
        """测试查找多个元素"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 访问URL
        url = "https://httpbin.org/html"
        self.skill.navigate(url)
        
        # 查找多个元素
        elements = self.skill.find_elements("a")
        
        # 验证元素列表被返回
        self.assertIsInstance(elements, list)
    
    def test_get_element_text(self):
        """测试获取元素文本"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 访问URL
        url = "https://httpbin.org/html"
        self.skill.navigate(url)
        
        # 获取元素文本 - 使用body元素作为测试，因为它肯定存在
        try:
            text = self.skill.get_element_text("body")
            # 验证文本被获取
            self.assertIsInstance(text, str)
        except ElementNotFoundError:
            # 如果元素未找到，测试失败
            self.fail("元素未找到")
    
    def test_element_not_found(self):
        """测试元素未找到情况"""
        # 启动浏览器
        self.skill.start_browser()
        
        # 访问URL
        url = "https://httpbin.org/html"
        self.skill.navigate(url)
        
        # 查找不存在的元素，应该抛出ElementNotFoundError
        with self.assertRaises(ElementNotFoundError):
            self.skill.find_element("#non_existent_element")


if __name__ == "__main__":
    unittest.main()
