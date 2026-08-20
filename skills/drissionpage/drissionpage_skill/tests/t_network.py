"""网络请求模块测试"""

import unittest
from drissionpage_skill import DrissionPageSkill
from drissionpage_skill.exceptions import NetworkError


class TestNetwork(unittest.TestCase):
    """网络请求模块测试类"""
    
    def setUp(self):
        """测试前设置"""
        self.skill = DrissionPageSkill()
    
    def tearDown(self):
        """测试后清理"""
        self.skill.close()
    
    def test_get_request(self):
        """测试GET请求"""
        # 测试一个简单的GET请求
        url = "https://httpbin.org/get"
        response = self.skill.get(url, params={"test": "value"})
        
        # 验证响应状态码
        self.assertEqual(response["status_code"], 200)
        # 验证响应数据包含请求参数
        self.assertEqual(response["data"]["args"]["test"], "value")
    
    def test_post_request(self):
        """测试POST请求"""
        # 测试表单数据POST请求
        url = "https://httpbin.org/post"
        data = {"key": "value"}
        response = self.skill.post(url, data=data)
        
        # 验证响应状态码
        self.assertEqual(response["status_code"], 200)
        # 验证响应数据包含提交的表单数据
        self.assertEqual(response["data"]["form"]["key"], "value")
    
    def test_post_json_request(self):
        """测试JSON数据POST请求"""
        # 测试JSON数据POST请求
        url = "https://httpbin.org/post"
        json_data = {"key": "value", "number": 123}
        response = self.skill.post(url, json=json_data)
        
        # 验证响应状态码
        self.assertEqual(response["status_code"], 200)
        # 验证响应数据包含提交的JSON数据
        self.assertEqual(response["data"]["json"]["key"], "value")
        self.assertEqual(response["data"]["json"]["number"], 123)
    
    def test_put_request(self):
        """测试PUT请求"""
        # 测试PUT请求
        url = "https://httpbin.org/put"
        data = {"key": "value"}
        response = self.skill.put(url, data=data)
        
        # 验证响应状态码
        self.assertEqual(response["status_code"], 200)
        # 验证响应数据包含提交的数据
        self.assertEqual(response["data"]["form"]["key"], "value")
    
    def test_delete_request(self):
        """测试DELETE请求"""
        # 测试DELETE请求
        url = "https://httpbin.org/delete"
        response = self.skill.delete(url)
        
        # 验证响应状态码
        self.assertEqual(response["status_code"], 200)
    
    def test_invalid_url(self):
        """测试无效URL"""
        # 测试无效URL
        url = "invalid_url"
        with self.assertRaises(NetworkError):
            self.skill.get(url)
    
    def test_custom_headers(self):
        """测试自定义请求头"""
        # 测试自定义请求头
        url = "https://httpbin.org/get"
        headers = {"X-Custom-Header": "custom_value"}
        response = self.skill.get(url, headers=headers)
        
        # 验证响应状态码
        self.assertEqual(response["status_code"], 200)
        # 验证响应数据包含自定义请求头
        self.assertEqual(response["data"]["headers"]["X-Custom-Header"], "custom_value")


if __name__ == "__main__":
    unittest.main()
