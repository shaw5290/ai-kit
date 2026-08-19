"""自定义异常类"""


class DrissionPageSkillError(Exception):
    """技能模块基础异常"""
    pass


class BrowserError(DrissionPageSkillError):
    """浏览器操作异常"""
    pass


class NetworkError(DrissionPageSkillError):
    """网络请求异常"""
    pass


class ElementNotFoundError(BrowserError):
    """元素未找到异常"""
    pass


class PageLoadError(BrowserError):
    """页面加载异常"""
    pass
