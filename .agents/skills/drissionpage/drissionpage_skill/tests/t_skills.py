"""
测试DrissionPageSkills类的各种功能
"""

import unittest
from drissionpage_skill import DrissionPageSkills
from drissionpage_skill.exceptions import DrissionPageSkillError, BrowserError, NetworkError


class TestDrissionPageSkills(unittest.TestCase):
    """测试DrissionPageSkills类"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建DrissionPageSkills实例
        self.skills = DrissionPageSkills()
    
    def tearDown(self):
        """清理测试环境"""
        # 关闭所有资源
        try:
            self.skills.close_all()
        except:
            pass
    
    def test_init_browser(self):
        """测试初始化浏览器"""
        # 初始化浏览器
        browser = self.skills.init_browser()
        # 验证浏览器对象被创建
        self.assertIsNotNone(browser)
    
    def test_init_session(self):
        """测试初始化会话"""
        # 初始化会话
        session = self.skills.init_session()
        # 验证会话对象被创建
        self.assertIsNotNone(session)
    
    def test_http_get(self):
        """测试发送HTTP GET请求"""
        # 发送GET请求
        url = "https://httpbin.org/get"
        response = self.skills.http_get(url)
        
        # 验证响应结果
        self.assertIsInstance(response, dict)
        self.assertIn('content', response)
        self.assertIsInstance(response['content'], str)
    
    def test_http_post(self):
        """测试发送HTTP POST请求"""
        # 发送POST请求
        url = "https://httpbin.org/post"
        data = {"key": "value"}
        response = self.skills.http_post(url, data=data)
        
        # 验证响应结果
        self.assertIsInstance(response, dict)
        self.assertIn('content', response)
        self.assertIsInstance(response['content'], str)
    
    def test_http_post_json(self):
        """测试发送HTTP POST请求（JSON数据）"""
        # 发送POST请求
        url = "https://httpbin.org/post"
        json_data = {"name": "test", "value": 123}
        response = self.skills.http_post(url, json=json_data)
        
        # 验证响应结果
        self.assertIsInstance(response, dict)
        self.assertIn('content', response)
        self.assertIsInstance(response['content'], str)
    
    def test_browser_navigate(self):
        """测试浏览器访问网址"""
        # 访问网址
        url = "https://httpbin.org/get"
        title = self.skills.browser_navigate(url)
        
        # 验证页面标题
        self.assertIsInstance(title, str)
    
    def test_get_element_text(self):
        """测试获取元素文本"""
        # 获取元素文本
        url = "https://httpbin.org/html"
        selector = "body"
        text = self.skills.get_element_text(url, selector)
        
        # 验证元素文本
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
    
    def test_close_browser(self):
        """测试关闭浏览器"""
        # 初始化浏览器
        self.skills.init_browser()
        # 关闭浏览器
        self.skills.close_browser()
        # 验证浏览器被关闭
        self.assertIsNone(self.skills.browser)
    
    def test_close_session(self):
        """测试关闭会话"""
        # 初始化会话
        self.skills.init_session()
        # 关闭会话
        self.skills.close_session()
        # 验证会话被关闭
        self.assertIsNone(self.skills.session)
    
    def test_close_all(self):
        """测试关闭所有资源"""
        # 初始化浏览器和会话
        self.skills.init_browser()
        self.skills.init_session()
        # 关闭所有资源
        self.skills.close_all()
        # 验证资源被关闭
        self.assertIsNone(self.skills.browser)
        self.assertIsNone(self.skills.session)


if __name__ == '__main__':
    unittest.main()
