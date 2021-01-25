import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from TBEA.base.util import BoxDriver, GetLogger, BasePage, GetExcel
import unittest
from parameterized import parameterized
from TBEA.page.Login_Page import LoginPage


class LoginTest(unittest.TestCase):
    logger = GetLogger(r'..\Report')

    @classmethod
    def setUpClass(self):

        self.driver = BoxDriver()
        self.logger.info('打开了浏览器，输入项目地址')
        self.page = LoginPage(self.driver)

    @classmethod
    def tearDownClass(self):
        self.logger.info('退出浏览器')
        self.driver.quit()

    @parameterized.expand(GetExcel().load(r'..\data\data.xlsx', 'login_success'))
    def test_login_success(self, username, password):
        '''登陆成功功能测试用例'''
        try:
            self.logger.info('登陆项目')
            self.page.login(username, password)
            # 断言
            real_name = self.page.get_login_name()
            self.logger.info('获取到的真名是：%s' % real_name)
            # assert element.text=='admin'
            self.assertEqual(real_name[0], '游', '登陆失败！')
            self.logger.info('断言成功！')
            self.page.logout()
            self.logger.info('签退完毕')
        except:
            raise NameError('测试失败！')


if __name__ == "__main__":
    unittest.main()
