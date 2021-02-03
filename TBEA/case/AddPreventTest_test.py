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
    def test_edittest_success(self, test_name):
        '''试验输入数据成功工程用例'''
        self.logger.warning(f'试验名称:{test_name}')
        try:
            self.driver.refresh()
            self.page.Init(transformer="测试变电站", E="测试变压器1", test_list=test_name, test_type="出厂试验")
            self.page.DeleteLeaveTest()
            self.page.Unfinished()
            self.page.Add()
            if test_name == "空载损耗和空载电流试验" or test_name == "短路阻抗和负载损耗试验":
                if test_name == "空载损耗和空载电流试验":
                    self.page.EditRow1()
                    self.page.Test11('Test11_A')
                    self.page.Save()
                    self.page.EditRow2()
                    self.page.Test12('Test12_A')
                    self.page.Save()
                    self.page.Input()
                else:
                    self.page.EditRow1()
                    self.page.Test11('Test11_A')
                    self.page.Save()
                    self.page.EditRow2()
                    self.page.Test12('Test12_A')
                    self.page.Save()
                    self.page.Input()

            else:
                self.page.Edit()
                if test_name == "绝缘油溶解气体试验":
                    self.page.Test1('Test1_A')
                elif test_name == "绕组直流电阻试验":
                    self.page.Test2('Test2_A')
                elif test_name == "绕组绝缘电阻试验":
                    self.page.Test3('Test3_A')
                elif test_name == "绕组绝缘电阻的介损和电容":
                    self.page.Test4('Test4_A')
                elif test_name == "套管的介损和电容":
                    self.page.Test5('Test5_A')
                elif test_name == "交流外施耐压试验":
                    self.page.Test6('Test6_A')
                elif test_name == "铁心、夹件绝缘电阻试验":
                    self.page.Test7('Test7_A')
                elif test_name == "绕组泄露电流":
                    self.page.Test8('Test8_A')
                elif test_name == "电压比和联结组标号检定":
                    self.page.Test9('Test9_A')
                elif test_name == "三相变压器/单相变压器极性检定":
                    self.page.Test10('Test10_A')
                elif test_name == "短时感应电压试验":
                    self.page.Test13('Test13_A')
                elif test_name == "长时感应电压试验":
                    self.page.Test14('Test14_A')
                elif test_name == "有载分接开关试验":
                    self.page.Test15('Test15_A')
                elif test_name == "气体继电器检测":
                    self.page.Test16('Test16_A')
                elif test_name == "压力释放器检测":
                    self.page.Test17('Test17_A')
                elif test_name == "冷却装置检测试验":
                    self.page.Test18('Test18_A')
                elif test_name == "套管电流互感器绝缘试验":
                    self.page.Test19('Test19_A')
                elif test_name == "测温装置检测":
                    self.page.Test20('Test20_A')
                elif test_name == "绝缘油试验":
                    self.page.Test21('Test21_A')
                elif test_name == "振动测量":
                    self.page.Test22('Test22_A')
                elif test_name == "噪声测量":
                    self.page.Test23('Test23_A')
                self.page.Save()
                self.page.Input()
            self.page.Init(transformer="测试变电站", E="测试变压器1", test_list=test_name,test_type="预防性试验")
            self.page.Unfinished()
            self.page.Add()
            self.logger.warning(f'{test_name}出厂试验已完成')
            if test_name == "空载损耗和空载电流试验" or test_name == "短路阻抗和负载损耗试验":
                if test_name == "空载损耗和空载电流试验":
                    self.page.EditRow1()
                    self.page.Test11('Test11_A')
                    Result = self.page.Judgement()
                    inf = self.page.Save()
                    self.page.EditRow2()
                    self.page.Test12('Test12_A')
                    self.page.Judgement()
                    self.page.Save()
                    self.page.Input()
                    arr = self.page.Find()
                else:
                    self.page.EditRow1()
                    self.page.Test11('Test11_A')
                    self.page.Judgement()
                    self.page.Save()
                    self.page.EditRow2()
                    self.page.Test12('Test12_A')
                    Result = self.page.Judgement()
                    inf = self.page.Save()
                    self.page.Input()
                    arr = self.page.Find()

            else:
                self.page.Edit()
                if test_name == "绝缘油溶解气体试验":
                    self.page.Test1('Test1_A')
                elif test_name == "绕组直流电阻试验":
                    self.page.Test2('Test2_A')
                elif test_name == "绕组绝缘电阻试验":
                    self.page.Test3('Test3_A')
                elif test_name == "绕组绝缘电阻的介损和电容":
                    self.page.Test4('Test4_A')
                elif test_name == "套管的介损和电容":
                    self.page.Test5('Test5_A')
                elif test_name == "交流外施耐压试验":
                    self.page.Test6('Test6_A')
                elif test_name == "铁心、夹件绝缘电阻试验":
                    self.page.Test7('Test7_A')
                elif test_name == "绕组泄露电流":
                    self.page.Test8('Test8_A')
                elif test_name == "电压比和联结组标号检定":
                    self.page.Test9('Test9_A')
                elif test_name == "三相变压器/单相变压器极性检定":
                    self.page.Test10('Test10_A')
                elif test_name == "短时感应电压试验":
                    self.page.Test13('Test13_A')
                elif test_name == "长时感应电压试验":
                    self.page.Test14('Test14_A')
                elif test_name == "有载分接开关试验":
                    self.page.Test15('Test15_A')
                elif test_name == "气体继电器检测":
                    self.page.Test16('Test16_A')
                elif test_name == "压力释放器检测":
                    self.page.Test17('Test17_A')
                elif test_name == "冷却装置检测试验":
                    self.page.Test18('Test18_A')
                elif test_name == "套管电流互感器绝缘试验":
                    self.page.Test19('Test19_A')
                elif test_name == "测温装置检测":
                    self.page.Test20('Test20_A')
                elif test_name == "绝缘油试验":
                    self.page.Test21('Test21_A')
                elif test_name == "振动测量":
                    self.page.Test22('Test22_A')
                elif test_name == "噪声测量":
                    self.page.Test23('Test23_A')
                try:
                    self.page.Judgement()
                finally:
                    pass
                self.page.Save()
                self.page.Input()
                arr = self.page.Find()
                self.logger.warning(f'---------{[self.page.test_list,self.page.transformer,self.page.E,self.page.test_type]}')
                self.logger.warning('------分割符------')
                self.logger.warning(f'---------{arr}')

            self.assertEqual(1,1,"断言失败")
            self.logger.warning(f"查询成功！查询结果未:{arr}")
        except Exception as e:
            self.logger.warning('准备Back1')
            self.page.Back()
            self.logger.warning('Back1成功')
            self.logger.warning('准备Back2')
            self.page.Back()
            self.logger.warning('Back成功2')
            self.logger.warning(f'测试失败{e}')
            raise NameError('测试失败')
        finally:
            self.page.Find()
            self.page.HomeDelete()

if __name__ == '__main__':
    unittest.main()

