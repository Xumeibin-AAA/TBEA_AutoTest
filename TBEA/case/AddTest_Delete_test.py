import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from TBEA.base.util import BoxDriver, GetLogger, BasePage, GetExcel,GetTxt
import unittest
from parameterized import parameterized

from TBEA.page.Addtest_Page import AddTestPage
from TBEA.page.Login_Page import LoginPage

class AddTestTest(unittest.TestCase):
    logger = GetLogger(r'..\Report')
    @classmethod
    def setUpClass(self):

        self.driver = BoxDriver()
        self.logger.warning('打开了浏览器，输入项目地址')
        self.page = AddTestPage(self.driver)
        self.page.login()


    @classmethod
    def tearDownClass(self):
        self.logger.info('退出浏览器')
        self.driver.quit()
    @parameterized.expand(GetTxt.get(r'..\data\TestList.txt'))
    def test_addtest_success(self, test_name):
        '''试验添加成功工程用例'''
        self.logger.warning(f'试验名称:{test_name}')
        try:
            self.driver.refresh()
            self.page.Init(test_list=test_name,type_test="出厂试验")
            self.page.Unfinished()
            self.page.Add()
            title = self.page.Delete()
            self.assertEqual(title,"删除成功！","断言失败")
            self.logger.warning('删除成功！')
            self.page.Back()
            self.driver.refresh()


        except Exception as e:
            self.logger.warning(f'测试失败{e}')
            raise NameError('测试失败')

if __name__ == '__main__':
    unittest.main()

