import os, sys
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
import unittest, time
from TBEA.base.HTMLTestRunner import HTMLTestRunner
from TBEA.base.util import Email

class TestRunner:

    def runner(self):
        # 创建测试套件
        suite = unittest.TestSuite()
        # 将测试用例添加到测试套件中
        # 参数1，用例所在的路径
        # 参数2，用例文件名应满足的条件
        suite.addTests(unittest.TestLoader().discover(r'..\case', pattern='*_test.py'))

        # 创建html报告文件
        timestr = time.strftime('%Y-%m-%d_%H-%M-%S')  # 时间戳
        path = r'..\Report\report_%s.html' % timestr
        report = open(path, mode='wb')
        # 创建用例运行器
        test_runner = HTMLTestRunner(stream=report, title='TBEA自动化测试报告', description='报告的详细内容描述....')

        # 运行测试用例，生成报告
        test_runner.run(suite)
        # 发送邮件
        # Email().send('TBEA自动化测试报告',path)


if __name__ == "__main__":
    TestRunner().runner()
