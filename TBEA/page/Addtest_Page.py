import os, sys, random, ast
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
import json, ast, random, re

from TBEA.base.util import BasePage, BoxDriver, GetTxt, GetRedis

from TBEA.page.Login_Page import LoginPage


class AddTestPage(LoginPage):
    # 初始化
    def Init(self, transformer="测试变电站", E="测试变压器1", test_list='绝缘油溶解气体试验', test_type="出厂试验"):
        try:
            self.transformer = transformer
            self.E = E
            self.test_list = test_list
            self.test_type = test_type
        finally:
            pass

    # 删除所有出厂试验
    def DeleteLeaveTest(self):
        try:
            driver = self.driver
            driver.refresh()
            driver.click('x,//*[@id="home"]/main/div/div[2]/div[1]/ul/li[2]')
            driver.wait(1)
            driver.click('x,//input[@placeholder="请选择变电站"]')
            # 点击‘测试变电站名称’
            driver.wait(1)
            driver.click(f'x,//span[text()="{self.transformer}"]')
            # 选择设备
            driver.wait(1)
            driver.click('x,//input[@placeholder="请选择设备"]')
            # 点击设备名称
            driver.wait(1)
            driver.click(f'x,//span[text()="{self.E}"]')
            driver.wait(1)
            # 点击查询
            driver.locate_element('x,//button[text()="查询"]')
            self.temp = ""
            try:
                driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/button[1]/span')
                self.temp = "ok"
            except Exception as e:
                self.temp = "err"
            if self.temp == "ok":
                title = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/button[1]/span').text
                if title == "查看详情":
                    driver.click(
                        'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/button[2]')
                    driver.click('x,/html/body/div[4]/div/div[3]/button[2]')
                    driver.wait(2)
                    driver.refresh()
                    return self.DeleteLeaveTest()
            else:
                driver.refresh()
        finally:
            pass

    # 删除所有未完成实验
    def Unfinished(self):
        try:
            driver = self.driver

            driver.click('x,//*[@id="home"]/main/div/div[2]/div[1]/ul/li[4]')
            driver.wait(1)
            driver.click('x,//input[@placeholder="请选择变电站"]')
            # 点击‘测试变电站名称’
            driver.wait(1)
            driver.click(f'x,//span[text()="{self.transformer}"]')
            # 选择设备
            driver.wait(1)
            driver.click('x,//input[@placeholder="请选择设备"]')
            # 点击设备名称
            driver.wait(1)
            driver.click(f'x,//span[text()="{self.E}"]')
            driver.wait(1)
            # 点击查询
            driver.locate_element('x,//button[text()="查询"]')
            self.temp = ""
            try:
                driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div[1]/div[3]/table/tbody/tr/td[3]/div/button/span')
                self.temp = "ok"
            except Exception as e:
                self.temp = "err"
            if self.temp == "ok":
                title = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div[1]/div[3]/table/tbody/tr/td[3]/div/button/span').text
                if title == "查看详情":
                    driver.click('x,//*[@id="home"]/main/div/div[3]/div[1]/div[3]/table/tbody/tr/td[3]/div/button/span')
                    t = driver.locate_element(
                        'x,//*[@id="home"]/main/div/div[1]/div[1]/div[3]/table/tbody/tr/td[5]/div/button[2]/span').text
                    if t == "删除":
                        try:
                            driver.click(
                                'x,//*[@id="home"]/main/div/div[1]/div[1]/div[3]/table/tbody/tr/td[5]/div/button[2]/span')
                            driver.click('x,/html/body/div[2]/div/div[3]/button[2]/span')
                            driver.wait(2)
                            driver.refresh()
                            driver.click('x,//*[@id="home"]/main/div/div[1]/div[2]/div[2]/button[1]/span')
                            return self.Unfinished()
                        except Exception as e:
                            driver.click('x,//*[@id="home"]/main/div/div[1]/div[2]/div[2]/button[2]/span')
                            driver.wait(3)
                            return self.Unfinished()
            else:
                driver.refresh()
        finally:
            pass

    # 查找最近建的试验
    def Find(self):
        try:
            driver = self.driver
            # 点击请选择变电站
            driver.wait(1)
            driver.click('x,//input[@placeholder="请选择变电站"]')
            # 点击‘测试变电站名称’
            driver.wait(1)
            driver.click(f'x,//span[text()="{self.transformer}"]')

            # 选择设备
            driver.wait(1)
            driver.click('x,//input[@placeholder="请选择设备"]')
            # 点击设备名称
            driver.wait(1)
            driver.click(f'x,//span[text()="{self.E}"]')
            driver.wait(1)
            # 点击查询
            driver.locate_element('x,//button[text()="查询"]')
            if self.test_list == "短路阻抗和负载损耗试验":
                testName = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[2]/td[3]/div').text
                transformerName = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[2]/td[4]/div').text
                EQ_Name = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[2]/td[5]/div').text
                testType = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[2]/td[7]/div/span').text
                if testType == "出厂":
                    testType = "出厂试验"
                else:
                    testType = "预防性试验"
                return [testName, transformerName, EQ_Name, testType]
            else:
                testName = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[3]/div').text
                transformerName = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[4]/div').text
                EQ_Name = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[5]/div').text
                testType = driver.locate_element(
                    'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[7]/div/span').text
                if testType == "出厂":
                    testType = "出厂试验"
                else:
                    testType = "预防性试验"
                return [testName, transformerName, EQ_Name, testType]
        finally:
            pass

    # 生成试验日报
    def TestReport(self):
        try:
            driver = self.driver
            # 点击查看详情
            driver.click(
                'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/button[1]/span')
            # 点击生成日报
            driver.click('x,//*[@id="home"]/main/div/div/div[3]/div[1]/button')
            # 点击保存
            driver.click('x,//*[@id="home"]/main/div/div[2]/div[1]/button[1]/span')
            # 输入Name
            RepoetName = str(uuid.uuid4())
            driver.wait(2)
            driver.input('x,/html/body/div[2]/div/div[2]/div[2]/div[1]/input', RepoetName)
            driver.click('x,/html/body/div[2]/div/div[3]/button[2]/span')
            driver.wait(10)
            driver.click('x,//*[@id="home"]/div/div/ul/li[1]/b')
            driver.click('x,//*[@id="home"]/main/div/div[2]/div[1]/ul/li[5]')
            text = driver.locate_element('x,//*[@id="home"]/main/div/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[1]/div').text
            if text == RepoetName:
                driver.click('x,//*[@id="home"]/main/div/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[3]/div/button[2]/span')
                driver.click('x,/html/body/div[2]/div/div[3]/button[2]/span')
                try:
                    driver.wait(2)
                    title = driver.locate_element('x,//p[text()="删除成功！"]').text
                except Exception as e:
                    title = "删除失败！"
                driver.wait(5)
                driver.refresh()
                return ['保存成功', title]
            else:
                driver.refresh()
                return '保存失败'
        finally:
            pass

    # 主页面删除
    def HomeDelete(self):
        try:
            driver = self.driver
            driver.wait(3)
            try:
                if self.driver.locate_element(
                        'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr/td[9]/div/button[1]/span').text == "查看详情":
                    if self.test_list == "空载损耗和空载电流试验" or self.test_list == "短路阻抗和负载损耗试验":
                        if self.test_list == "空载损耗和空载电流试验":
                            driver.click(
                                'x,/html/body/div/div/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/button[2]/span')
                            driver.click('x,/html/body/div[4]/div/div[3]/button[2]/span')
                            inf = driver.locate_element('x,//p[text()="删除成功！"]').text
                            driver.wait(4)
                            driver.click(
                                'x,/html/body/div/div/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/button[2]/span')
                            driver.click('x,/html/body/div[4]/div/div[3]/button[2]/span')
                            driver.wait(4)
                            self.HomeDelete()
                            return inf
                        elif self.test_list == "短路阻抗和负载损耗试验":
                            driver.click(
                                'x,/html/body/div/div/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/button[2]/span')
                            driver.click('x,/html/body/div[4]/div/div[3]/button[2]/span')
                            driver.wait(4)
                            driver.click(
                                'x,/html/body/div/div/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/button[2]/span')
                            driver.click('x,/html/body/div[4]/div/div[3]/button[2]/span')
                            inf = driver.locate_element('x,//p[text()="删除成功！"]').text
                            driver.wait(4)
                            self.HomeDelete()
                            return inf

                    else:
                        driver.click(
                            'x,/html/body/div/div/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/button[2]/span')
                        driver.click('x,/html/body/div[4]/div/div[3]/button[2]/span')
                        driver.wait(1)
                        inf = driver.locate_element('x,//p[text()="删除成功！"]').text
                        self.HomeDelete()
                        return inf
            except Exception as e:
                return 0
        finally:
            pass

    # 添加试验
    def Add(self):
        try:
            driver = self.driver
            driver.refresh()
            driver.wait(3)
            # 点击新建试验
            driver.click('x,/html/body/div[1]/div/main/div/div[2]/div[2]/button[1]/i')
            # 点击请选择变电站
            driver.click('x,//html/body/div/div/div[2]/ul/li[1]/div/div/input')
            # 点击‘测试变电站名称’
            driver.wait(1)
            driver.click(f'x,/html/body/div[4]/div[1]/div[1]/ul/*/span[text()="{self.transformer}"]')
            # 选择设备
            driver.click('x,/html/body/div/div/div[2]/ul/li[2]/div/div[1]/input')
            # 点击设备名称
            driver.wait(1)
            driver.click(f'x,//span[text()="{self.E}"]')
            # 选择试验类型
            driver.wait(1)
            driver.click('x,/html/body/div/div/div[2]/ul/li[3]/div/div/input')
            '''
            1:出厂试验
            2:预防试验
            '''
            driver.wait(1)
            if self.test_type == "出厂试验":
                driver.click('x,//span[text()="出厂试验"]')
            elif self.test_type == "预防性试验":
                driver.click('x,//span[text()="预防性试验"]')

            # 选择试验
            arr = GetTxt().get(r'..\data\TestList.txt')
            i = arr.index(self.test_list) + 1
            driver.wait(1)
            if self.test_list == '空载损耗和空载电流试验':
                driver.click('x,/html/body/div[3]/div/div[2]/div/div[1]/div/div[1]/label[%d]' % i)
                driver.click('x,/html/body/div[3]/div/div[2]/div/div[1]/div/div[1]/label[%d]' % (i + 1))
            elif self.test_list == '短路阻抗和负载损耗试验':
                # 选中试验
                driver.click('x,/html/body/div[3]/div/div[2]/div/div[1]/div/div[1]/label[%d]' % i)
                driver.click('x,/html/body/div[3]/div/div[2]/div/div[1]/div/div[1]/label[%d]' % (i - 1))
            else:
                driver.click('x,/html/body/div/div/div[2]/div/div[1]/div/div[1]/label[%d]' % i)
            # 到右边
            driver.click('x,//span[text()="到右边 "]')
            # 选中右边
            driver.click('x,/html/body/div[3]/div/div[2]/div/div[2]/div/div[1]/label/span[1]')
            # 删除
            # driver.click('x,/html/body/div[3]/div/div[2]/div/div[2]/div/div[2]/button/span')
            # 确认
            driver.click('x,//div[@aria-label="新建试验"]//*/button[2]/span')
        finally:
            pass
    # 共一行
    def Edit(self):
        try:
            driver = self.driver
            driver.wait(5)
            driver.click('x,//*[@id="home"]/main/div/div[1]/div[1]/div[3]/table/tbody/tr/td[5]/div/button[1]')
            driver.wait(5)
        finally:
            pass

    # 共二行编辑第一行
    def EditRow1(self):
        try:
            driver = self.driver
            driver.wait(3)
            driver.click('x,//*[@id="home"]/main/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[5]/div/button[1]')
        finally:
            pass
    # 共二行编辑第二行
    def EditRow2(self):
        try:
            driver = self.driver
            driver.wait(3)

            driver.click('x,//*[@id="home"]/main/div/div[1]/div[1]/div[3]/table/tbody/tr[2]/td[5]/div/button[1]')
        finally:
            pass
    # 删除
    def Delete(self):
        try:
            driver = self.driver
            if self.test_list == '空载损耗和空载电流试验' or self.test_list == '短路阻抗和负载损耗试验':
                for j in range(2):
                    driver.click('x,//*[@id="home"]/main/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[5]/div/button[2]')
                    driver.click('x,/html/body/div[2]/div/div[3]/button[2]')
                    if self.test_list == '空载损耗和空载电流试验':
                        title = driver.locate_element('x,/html/body/div[3]/p').text
                    elif self.test_list == '短路阻抗和负载损耗试验':
                        title = driver.locate_element('x,/html/body/div[3]/p').text
                    driver.wait(5)
                return title
            else:
                driver.click('x,//*[@id="home"]/main/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[5]/div/button[2]')
                driver.click('x,/html/body/div[2]/div/div[3]/button[2]')
                title = driver.locate_element('x,/html/body/div[3]/p').text
                return title
        finally:
            pass
    # 绝缘油溶解气体试验
    def Test1(self, data):
        '''
        :param data:
        :param test: 试验
        :param row: 参数所在的行
        :param result: 导则结果
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            # 第一行
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 第一个表格
            driver.input('x,/html/body/div/div/main/div/div/div[2]/table/tr[2]/td[2]/input', value['p1'])
            # 第二个表格
            driver.input('x,/html/body/div/div/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p2'])
            # 第三个表格
            driver.input('x,/html/body/div/div/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p3'])
            # 第四个表格
            driver.input('x,/html/body/div/div/main/div/div/div[2]/table/tr[2]/td[5]/input', value['p4'])
            # 第五个表格
            driver.input('x,/html/body/div/div/main/div/div/div[2]/table/tr[2]/td[6]/input', value['p5'])
            # 第六个表格
            driver.input('x,/html/body/div/div/main/div/div/div[2]/table/tr[2]/td[7]/input', value['p6'])
            # 第七个表格
            driver.input('x,/html/body/div/div/main/div/div/div[2]/table/tr[2]/td[8]/input', value['p7'])
            # 起始时间
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[10]/div/input', f"{value['p8']} 00:00:00")
            # 取样部位
            driver.click('x,/html/body/div[1]/div/main/div/div/div[2]/table/tr[2]/td[13]/div/div/input')
            # 上中下瓦斯继电器
            x = random.randint(1, 4)
            driver.click(f'x,/html/body/div[3]/div[1]/div[1]/ul/li[{x}]')

            # 第二行
            # 第一个表格
            driver.input('x,/html/body/div[1]/div/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p9'])
            # 第二个表格
            driver.input('x,/html/body/div[1]/div/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p10'])
            # 第三个表格
            driver.input('x,/html/body/div[1]/div/main/div/div/div[2]/table/tr[3]/td[4]/input', value['p11'])
            # 第四个表格
            driver.input('x,/html/body/div[1]/div/main/div/div/div[2]/table/tr[3]/td[5]/input', value['p12'])
            # 第五个表格
            driver.input('x,/html/body/div[1]/div/main/div/div/div[2]/table/tr[3]/td[6]/input', value['p13'])
            # 第六个表格
            driver.input('x,/html/body/div[1]/div/main/div/div/div[2]/table/tr[3]/td[7]/input', value['p14'])
            # 第七个表格
            driver.input('x,/html/body/div[1]/div/main/div/div/div[2]/table/tr[3]/td[8]/input', value['p15'])
            # 终止时间
            driver.input('x,/html/body/div[1]/div/main/div/div/div[2]/table/tr[3]/td[10]/div/input',
                         f"{value['p16']} 00:00:00")
            driver.click('x,//*[@id="home"]/main/div/div/div[1]/div')
            driver.wait(1)
            # Result
            # 第一次取样烃类总和
            rs1 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[9]/span').text
            # 取样间隔d
            rs2 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[11]/span').text
            # 取样间隔m
            rs3 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[12]/span').text
            # 第二次取样烃类总和
            rs4 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[9]/span').text
            # 绝对产气速率H2
            rs5 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[2]/span').text
            # 绝对产气速率CO
            rs6 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/span').text
            # 绝对产气速率CO2
            rs7 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/span').text
            # 绝对产气速率CH4
            rs8 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/span').text
            # 绝对产气速率C2H4
            rs9 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[6]/span').text
            # 绝对产气速率C2H6
            rs10 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[7]/span').text
            # 绝对产气速率C2H2
            rs11 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[8]/span').text
            # 绝对产气速率总烃
            rs12 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[9]/span').text
            # 相对产气速率H2
            rs13 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[2]/span').text
            # 相对产气速率CO
            rs14 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/span').text
            # 相对产气速率CO2
            rs15 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/span').text
            # 相对产气速率CH4
            rs16 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/span').text
            # 相对产气速率C2H4
            rs17 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[6]/span').text
            # 相对产气速率C2H6
            rs18 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[7]/span').text
            # 相对产气速率C2H2
            rs19 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[8]/span').text
            # 相对产气速率总烃
            rs20 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[9]/span').text
            Result = {'rs1': rs1, 'rs2': rs2, 'rs3': rs3, 'rs4': rs4, 'rs5': rs5, 'rs6': rs6, 'rs7': rs7, 'rs8': rs8,
                      'rs9': rs9, 'rs10': rs10, 'rs11': rs11, 'rs12': rs12, 'rs13': rs13, 'rs14': rs14, 'rs15': rs15,
                      'rs16': rs16, 'rs17': rs17, 'rs18': rs18, 'rs19': rs19, 'rs20': rs20}

            for i in Result.keys():

                if re.compile("^-?\d*\\.?\d*$").match(Result[i]):
                    Result[i] = float(Result[i])
            return Result
        finally:
            pass

    # 绕组直流电阻试验
    def Test2(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            global i2
            driver = self.driver
            redis = GetRedis()
            # 第一行
            value = redis.GetDate(data)
            value = ast.literal_eval(value)

            # 参数1
            if self.test_type == "出厂试验":
                if value['p1'] == "相":
                    i = 1
                else:
                    i = 2
                driver.click('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[2]/div/div/input')
                driver.click(f'x,/html/body/div/div[1]/div[1]/ul/li[{i}]/span')
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[4]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[2]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[2]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/input', value['p10'])
            # 参数11
            if self.test_type == "出厂试验":
                if value['p11'] == "相":
                    i1 = 1
                else:
                    i1 = 2
                driver.click('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[2]/div/div/input')
                driver.click(f'x,/html/body/div[3]/div[1]/div[1]/ul/li[{i1}]/span')
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[2]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[3]/input', value['p13'])
            # 参数14
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[4]/input', value['p14'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[2]/input', value['p15'])
            # 参数16
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[3]/input', value['p16'])
            # 参数17
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[4]/input', value['p17'])
            # 参数18
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[2]/input', value['p18'])
            # 参数19
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[3]/input', value['p19'])
            # 参数20
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[4]/input', value['p20'])
            # 参数21
            if self.test_type == "出厂试验":
                if value['p21'] == "相":
                    i2 = 1
                else:
                    i2 = 2
                driver.click('x,//*[@id="home"]/main/div/div/div[2]/table/tr[14]/td[2]/div/div[1]/input')
                driver.click(f'x,/html/body/div[4]/div[1]/div[1]/ul/li[{i2}]/span')
            # 参数22.
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[15]/td[2]/input', value['p22'])
            # 参数23
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[15]/td[3]/input', value['p23'])
            # 参数24
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[15]/td[4]/input', value['p24'])
            # 最负分解
            rs1 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[5]/span').text
            # 主分接
            rs2 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/span').text
            # 最正分接
            rs3 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/span').text
            # 最负分接
            rs4 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[5]/span').text
            # 主分接
            rs5 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[5]/span').text
            # 最正分接
            rs6 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[5]/span').text
            # 低压分接头
            rs7 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[15]/td[5]/span').text
            Result = {'rs1': rs1, 'rs2': rs2, 'rs3': rs3, 'rs4': rs4, 'rs5': rs5, 'rs6': rs6, 'rs7': rs7}

            for i in Result.keys():

                if re.compile("^-?\d*\\.?\d*$").match(Result[i]):
                    Result[i] = float(Result[i])
            return Result
        finally:
            pass
    # 绕组绝缘电阻试验
    def Test3(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[5]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[4]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[5]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/input', value['p11'])
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p13'])
            # 参数14
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[4]/input', value['p14'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[5]/input', value['p15'])
            # 吸收比d(高压)
            rs1 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[6]/span').text
            # 极化指数(高压)
            rs2 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[7]/span').text
            # 吸收比d(中压)
            rs3 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[6]/span').text
            # 极化指数(中压)
            rs4 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[7]/span').text
            # 吸收比d(低压)
            rs5 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[6]/span').text
            # 极化指数(低压)
            rs6 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[7]/span').text
            # 吸收比d(高压和中压)
            rs7 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[6]/span').text
            # 极化指数(高压和中压)
            rs8 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[7]/span').text
            # 吸收比d(高压中亚和低压)
            rs9 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[6]/span').text
            # 极化指数(高压中亚和低压)
            rs10 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[7]/span').text
            Result = {'rs1': rs1, 'rs2': rs2, 'rs3': rs3, 'rs4': rs4, 'rs5': rs5, 'rs6': rs6, 'rs7': rs7, 'rs8': rs8,
                      'rs9': rs9, 'rs10': rs10}
            for i in Result.keys():
                if re.compile("^-?\d*\\.?\d*$").match(Result[i]):
                    Result[i] = float(Result[i])
            return Result
        finally:
            pass

    # 绕组绝缘电阻的介损和电容
    def Test4(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[6]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[5]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[5]/input', value['p11'])
            # 高压
            rs1 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[5]/span').text
            # 中压
            rs2 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[4]/span').text
            # 低压
            rs3 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/span').text
            # 高压和中压
            rs4 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/span').text
            # 高压中压和低压
            rs5 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[4]/span').text

            Result = {'rs1': rs1, 'rs2': rs2, 'rs3': rs3, 'rs4': rs4, 'rs5': rs5}

            for i in Result.keys():

                if re.compile("^-?\d*\\.?\d*$").match(Result[i]):
                    Result[i] = float(Result[i])
            return Result
        finally:
            pass

    # 套管的介损和电容
    def Test5(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[6]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[5]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[5]/input', value['p11'])

            # 高压
            rs1 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[5]/span').text
            # 中压
            rs2 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[4]/span').text
            # 低压
            rs3 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/span').text
            # 高压和中压
            rs4 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/span').text
            # 高压中压和低压
            rs5 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[4]/span').text

            Result = {'rs1': rs1, 'rs2': rs2, 'rs3': rs3, 'rs4': rs4, 'rs5': rs5}

            for i in Result.keys():

                if re.compile("^-?\d*\\.?\d*$").match(Result[i]):
                    Result[i] = float(Result[i])
            return Result
        finally:
            pass
    # 交流外施耐压试验
    def Test6(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p5'])
        finally:
            pass
    # 铁心、夹件绝缘电阻试验
    def Test7(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[4]/input', value['p4'])
        finally:
            pass
    # 绕组泄露电流
    def Test8(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p5'])
        finally:
            pass
    # 电压比和联结组标号检定
    def Test9(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[12]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[2]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[2]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[4]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[2]/input', value['p11'])
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[3]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[4]/input', value['p13'])
            # 参数14
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[12]/input', value['p14'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[2]/input', value['p15'])
            # 参数16
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[3]/input', value['p16'])
            # 参数17
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[4]/input', value['p17'])
            # 参数18
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[2]/input', value['p18'])
            # 参数19
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[3]/input', value['p19'])
            # 参数20
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[4]/input', value['p20'])
            # 参数21
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[2]/input', value['p21'])
            # 参数22
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[3]/input', value['p22'])
            # 参数23
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[4]/input', value['p23'])
            # 参数24
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[12]/input', value['p24'])
            # 参数25
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[2]/input', value['p25'])
            # 参数26
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[3]/input', value['p26'])
            # 参数27
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[4]/input', value['p27'])
            # 参数28
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[2]/input', value['p28'])
            # 参数29
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[3]/input', value['p29'])
            # 参数30
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[4]/input', value['p30'])
            # 最负分接
            rs1 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[6]/span').text
            rs2 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[7]/span').text
            rs3 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[8]/span').text
            rs4 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[9]/span').text
            rs5 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[10]/span').text
            rs6 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[11]/span').text
            # 主分接
            rs7 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/span').text
            rs8 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[6]/span').text
            rs9 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[7]/span').text
            rs10 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[8]/span').text
            rs11 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[9]/span').text
            rs12 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[10]/span').text
            # 最正分接
            rs13 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[5]/span').text
            rs14 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[6]/span').text
            rs15 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[7]/span').text
            rs16 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[8]/span').text
            rs17 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[9]/span').text
            rs18 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[10]/span').text
            # 最负分接
            rs19 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[6]/span').text
            rs20 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[7]/span').text
            rs21 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[8]/span').text
            rs22 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[9]/span').text
            rs23 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[10]/span').text
            rs24 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[11]/span').text
            # 主分接
            rs25 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[5]/span').text
            rs26 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[6]/span').text
            rs27 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[7]/span').text
            rs28 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[8]/span').text
            rs29 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[9]/span').text
            rs30 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[10]/span').text
            # 最正分接
            rs31 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[5]/span').text
            rs32 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[6]/span').text
            rs33 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[7]/span').text
            rs34 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[8]/span').text
            rs35 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[9]/span').text
            rs36 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[10]/span').text
            # 最负分接
            rs37 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[6]/span').text
            rs38 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[7]/span').text
            rs39 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[8]/span').text
            rs40 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[9]/span').text
            rs41 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[10]/span').text
            rs42 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[11]/span').text
            # 主分接
            rs43 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[5]/span').text
            rs44 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[6]/span').text
            rs45 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[7]/span').text
            rs46 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[8]/span').text
            rs47 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[9]/span').text
            rs48 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[10]/span').text
            # 最正分接
            rs49 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[5]/span').text
            rs50 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[6]/span').text
            rs51 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[7]/span').text
            rs52 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[8]/span').text
            rs53 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[9]/span').text
            rs54 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[10]/span').text
            Result = {'rs1': rs1, 'rs2': rs2, 'rs3': rs3, 'rs4': rs4, 'rs5': rs5, 'rs6': rs6, 'rs7': rs7, 'rs8': rs8,
                      'rs9': rs9, 'rs10': rs10, 'rs11': rs11, 'rs12': rs12, 'rs13': rs13, 'rs14': rs14, 'rs15': rs15,
                      'rs16': rs16, 'rs17': rs17, 'rs18': rs18, 'rs19': rs19, 'rs20': rs20, 'rs21': rs21, 'rs22': rs22,
                      'rs23': rs23, 'rs24': rs24, 'rs25': rs25, 'rs26': rs26, 'rs27': rs27, 'rs28': rs28, 'rs29': rs29,
                      'rs30': rs30, 'rs31': rs31, 'rs32': rs32, 'rs33': rs33, 'rs34': rs34, 'rs35': rs35, 'rs36': rs36,
                      'rs37': rs37, 'rs38': rs38, 'rs39': rs39, 'rs40': rs40, 'rs41': rs41, 'rs42': rs42, 'rs43': rs43,
                      'rs44': rs44, 'rs45': rs45, 'rs46': rs46, 'rs47': rs47, 'rs48': rs48, 'rs49': rs49, 'rs50': rs50,
                      'rs51': rs51, 'rs52': rs52, 'rs53': rs53, 'rs54': rs54}
            for i in Result.keys():
                if re.compile("^-?\d*\\.?\d*$").match(Result[i]):
                    Result[i] = float(Result[i])
            return Result
        finally:
            pass

    # 三相变压器/单相变压器极性检定

    def Test10(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            if value['p1'] == "三相":
                i = 1
            elif value['p1'] == "单相":
                i = 2
            driver.click('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[1]/div/div/input')
            driver.click(f'x,/html/body/div/div[1]/div[1]/ul/li[{i}]/span')
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[2]/input', value['p2'])
        finally:
            pass
    # 空载损耗和空载电流试验
    def Test11(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[4]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[5]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[6]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[8]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[2]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[6]/input', value['p11'])
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[8]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[2]/input', value['p13'])
            # 参数14
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p14'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/input', value['p15'])
            # 参数16
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/input', value['p16'])
            # 参数17
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[6]/input', value['p17'])
            # 参数18
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[8]/input', value['p18'])
            # 参数19
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[2]/input', value['p19'])
            # 参数20
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[3]/input', value['p20'])
            # 参数21
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[4]/input', value['p21'])
            # 参数22
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[5]/input', value['p22'])
            # 参数23
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[6]/input', value['p23'])
            # 参数24
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[8]/input', value['p24'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[2]/input', value['p25'])
            # 参数26
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[3]/input', value['p26'])
            # 参数27
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[4]/input', value['p27'])
            # 参数28
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[5]/input', value['p28'])
            # 参数29
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[6]/input', value['p29'])
            # 参数30
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[8]/input', value['p30'])
            # 参数31
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[2]/input', value['p31'])
            # 参数32
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[3]/input', value['p32'])
            # 参数33
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[4]/input', value['p33'])
            # 参数34
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[5]/input', value['p34'])
            # 参数35
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[6]/input', value['p35'])
            # 参数36
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[8]/input', value['p36'])
            # 试验前 90%
            rs1 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[7]/span').text
            rs2 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[9]/span').text
            # 试验前 100%
            rs3 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[7]/span').text
            rs4 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[9]/span').text
            # 试验前 110%
            rs5 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[7]/span').text
            rs6 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[9]/span').text
            # 试验后 90%
            rs7 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[7]/span').text
            rs8 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[9]/span').text
            # 试验后 100%
            rs9 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[7]/span').text
            rs10 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[9]/span').text
            # 试验后110%
            rs11 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[7]/span').text
            rs12 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[9]/span').text

            Result = {'rs1': rs1, 'rs2': rs2, 'rs3': rs3, 'rs4': rs4, 'rs5': rs5, 'rs6': rs6, 'rs7': rs7, 'rs8': rs8,
                      'rs9': rs9, 'rs10': rs10, 'rs11': rs11, 'rs12': rs12}
            for i in Result.keys():
                if re.compile("^-?\d*\\.?\d*$").match(Result[i]):
                    Result[i] = float(Result[i])
            return Result
        finally:
            pass
    # 短路阻抗和负载损耗试验
    def Test12(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[6]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[2]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[6]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[2]/input', value['p11'])
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[4]/input', value['p13'])
            # 参数14
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[5]/input', value['p14'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[6]/input', value['p15'])
            # 参数16
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[2]/input', value['p16'])
            # 参数17
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[3]/input', value['p17'])
            # 参数18
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[4]/input', value['p18'])
            # 参数19
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[5]/input', value['p19'])
            # 参数20
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[6]/input', value['p20'])
            # 参数21
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[2]/input', value['p21'])
            # 参数22
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[3]/input', value['p22'])
            # 参数23
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[4]/input', value['p23'])
            # 参数24
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[5]/input', value['p24'])
            # 参数25
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[6]/input', value['p25'])
            # 参数26
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[2]/input', value['p26'])
            # 参数27
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[3]/input', value['p27'])
            # 参数28
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[4]/input', value['p28'])
            # 参数29
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[5]/input', value['p29'])
            # 参数30
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[6]/input', value['p30'])
            # 参数31
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[2]/input', value['p31'])
            # 参数32
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[3]/input', value['p32'])
            # 参数33
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[4]/input', value['p33'])
            # 参数34
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[5]/input', value['p34'])
            # 参数35
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[6]/input', value['p35'])
            # 参数36
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[2]/input', value['p36'])
            # 参数37
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[3]/input', value['p37'])
            # 参数38
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[4]/input', value['p38'])
            # 参数39
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[5]/input', value['p39'])
            # 参数40
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[6]/input', value['p40'])
            # 参数41
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[2]/input', value['p41'])
            # 参数42
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[3]/input', value['p42'])
            # 参数43
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[4]/input', value['p43'])
            # 参数44
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[5]/input', value['p44'])
            # 参数45
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[20]/td[6]/input', value['p45'])

            # 高对中
            rs1 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[7]/span').text
            rs2 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[7]/span').text
            rs3 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[7]/span').text
            # 高对低
            rs4 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[7]/span').text
            rs5 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[7]/span').text
            rs6 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[7]/span').text
            # 中对低
            rs7 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[7]/span').text
            rs8 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[19]/td[7]/span').text
            rs9 = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr[18]/td[7]/span').text

            Result = {'rs1': rs1, 'rs2': rs2, 'rs3': rs3, 'rs4': rs4, 'rs5': rs5, 'rs6': rs6, 'rs7': rs7, 'rs8': rs8,
                      'rs9': rs9}
            for i in Result.keys():
                if re.compile("^-?\d*\\.?\d*$").match(Result[i]):
                    Result[i] = float(Result[i])
            return Result
        finally:
            pass

    # 短时感应电压试验
    def Test13(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[5]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[6]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[7]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[8]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[9]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[10]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[11]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[12]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[4]/input', value['p11'])
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[5]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[6]/input', value['p13'])
            # 参数14
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[7]/input', value['p14'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[8]/input', value['p15'])
            # 参数16
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[9]/input', value['p16'])
            # 参数17
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[10]/input', value['p17'])
            # 参数18
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[11]/input', value['p18'])
            # 参数19
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p19'])
            # 参数20
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/input', value['p20'])
            # 参数21
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/input', value['p21'])
            # 参数22
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[6]/input', value['p22'])
            # 参数23
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[7]/input', value['p23'])
            # 参数24
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[8]/input', value['p24'])
            # 参数25
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[9]/input', value['p25'])
            # 参数26
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[10]/input', value['p26'])
            # 参数27
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[11]/input', value['p27'])
            # 参数28
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p28'])
            # 参数29
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/input', value['p29'])
            # 参数30
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/input', value['p30'])
            # 参数31
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[6]/input', value['p31'])
            # 参数32
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[7]/input', value['p32'])
            # 参数33
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[8]/input', value['p33'])
            # 参数34
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[9]/input', value['p34'])
            # 参数35
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[10]/input', value['p35'])
            # 参数36
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[11]/input', value['p36'])
            # 参数37
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p37'])
            # 参数38
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[4]/input', value['p38'])
            # 参数39
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[5]/input', value['p39'])
            # 参数40
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[6]/input', value['p40'])
            # 参数41
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[7]/input', value['p41'])
            # 参数42
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[8]/input', value['p42'])
            # 参数43
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[9]/input', value['p43'])
            # 参数44
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[10]/input', value['p44'])
            # 参数45
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[11]/input', value['p45'])
        finally:
            pass
    # 长时感应电压试验
    def Test14(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[5]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[6]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[7]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[8]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[9]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[10]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[11]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[12]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[4]/input', value['p11'])
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[5]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[6]/input', value['p13'])
            # 参数14
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[7]/input', value['p14'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[8]/input', value['p15'])
            # 参数16
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[9]/input', value['p16'])
            # 参数17
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[10]/input', value['p17'])
            # 参数18
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[11]/input', value['p18'])
            # 参数19
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p19'])
            # 参数20
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/input', value['p20'])
            # 参数21
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/input', value['p21'])
            # 参数22
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[6]/input', value['p22'])
            # 参数23
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[7]/input', value['p23'])
            # 参数24
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[8]/input', value['p24'])
            # 参数25
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[9]/input', value['p25'])
            # 参数26
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[10]/input', value['p26'])
            # 参数27
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[11]/input', value['p27'])
            # 参数28
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p28'])
            # 参数29
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/input', value['p29'])
            # 参数30
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/input', value['p30'])
            # 参数31
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[6]/input', value['p31'])
            # 参数32
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[7]/input', value['p32'])
            # 参数33
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[8]/input', value['p33'])
            # 参数34
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[9]/input', value['p34'])
            # 参数35
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[10]/input', value['p35'])
            # 参数36
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[11]/input', value['p36'])
            # 参数37
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p37'])
            # 参数38
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[4]/input', value['p38'])
            # 参数39
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[5]/input', value['p39'])
            # 参数40
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[6]/input', value['p40'])
            # 参数41
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[7]/input', value['p41'])
            # 参数42
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[8]/input', value['p42'])
            # 参数43
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[9]/input', value['p43'])
            # 参数44
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[10]/input', value['p44'])
            # 参数45
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[11]/input', value['p45'])
        finally:
            pass

    # 有载分接开关试验
    def Test15(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[2]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[2]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[2]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[3]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[4]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[5]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[6]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[7]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[2]/input', value['p11'])
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[3]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[4]/input', value['p13'])
            # 参数14
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[5]/input', value['p14'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[6]/input', value['p15'])
            # 参数16
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[7]/input', value['p16'])
            # 参数17
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[2]/input', value['p17'])
        finally:
            pass
    # 气体继电器检测
    def Test16(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p1'])
        finally:
            pass
    # 压力释放器检测
    def Test17(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/p/input[1]', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/p/input[2]', value['p3'])
        finally:
            pass
    # 冷却装置检测试验
    def Test18(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p2'])
        finally:
            pass
    # 套管电流互感器绝缘试验
    def Test19(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[5]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[6]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[7]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[8]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[4]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[5]/input', value['p11'])
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[6]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[7]/input', value['p13'])
            # 参数14
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[8]/input', value['p14'])
            # 参数15
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[2]/input', value['p15'])
            # 参数16
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[3]/input', value['p16'])
            # 参数17
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[4]/input', value['p17'])
            # 参数18
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[5]/input', value['p18'])
            # 参数19
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[6]/input', value['p19'])
            # 参数20
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[7]/input', value['p20'])
            # 参数21
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[8]/input', value['p21'])
            # 参数22
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[2]/input', value['p22'])
            # 参数23
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[3]/input', value['p23'])
            # 参数24
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[4]/input', value['p24'])
            # 参数25
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[5]/input', value['p25'])
            # 参数26
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[6]/input', value['p26'])
            # 参数27
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[7]/input', value['p27'])
            # 参数28
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[8]/input', value['p28'])
            # 参数29
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[2]/input', value['p29'])
            # 参数30
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[3]/input', value['p30'])
            # 参数31
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[4]/input', value['p31'])
            # 参数32
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[5]/input', value['p32'])
            # 参数33
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[6]/input', value['p33'])
            # 参数34
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[7]/input', value['p34'])
            # 参数35
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[8]/input', value['p35'])
            # 参数36
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[7]/td[2]/input', value['p36'])
            # 参数37
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[7]/td[3]/input', value['p37'])
            # 参数38
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[7]/td[4]/input', value['p38'])
            # 参数39
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[7]/td[5]/input', value['p39'])
            # 参数40
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[7]/td[6]/input', value['p40'])
            # 参数41
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[7]/td[7]/input', value['p41'])
            # 参数42
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[7]/td[8]/input', value['p42'])
            # 参数43
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[2]/input', value['p43'])
            # 参数44
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[3]/input', value['p44'])
            # 参数45
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[4]/input', value['p45'])
            # 参数46
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[5]/input', value['p46'])
            # 参数47
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[6]/input', value['p47'])
            # 参数48
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[7]/input', value['p48'])
            # 参数49
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[8]/input', value['p49'])
            # 参数50
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[2]/input', value['p50'])
            # 参数51
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[3]/input', value['p51'])
            # 参数52
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[4]/input', value['p52'])
            # 参数53
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[5]/input', value['p53'])
            # 参数54
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[6]/input', value['p54'])
            # 参数55
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[7]/input', value['p55'])
            # 参数56
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[8]/input', value['p56'])
            # 参数57
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[2]/input', value['p57'])
            # 参数58
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[3]/input', value['p58'])
            # 参数59
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[4]/input', value['p59'])
            # 参数60
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[5]/input', value['p60'])
            # 参数61
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[6]/input', value['p61'])
            # 参数62
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[7]/input', value['p62'])
            # 参数63
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[8]/input', value['p63'])
            # 参数64
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[2]/input', value['p64'])
            # 参数65
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[3]/input', value['p65'])
            # 参数66
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[4]/input', value['p66'])
            # 参数67
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[5]/input', value['p67'])
            # 参数68
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[6]/input', value['p68'])
            # 参数69
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[7]/input', value['p69'])
            # 参数70
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[8]/input', value['p70'])
            # 参数71
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[2]/input', value['p71'])
            # 参数72
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[3]/input', value['p72'])
            # 参数73
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[4]/input', value['p73'])
            # 参数74
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[5]/input', value['p74'])
            # 参数75
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[6]/input', value['p75'])
            # 参数76
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[7]/input', value['p76'])
            # 参数77
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[8]/input', value['p77'])
            # 参数78
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[2]/input', value['p78'])
            # 参数79
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[3]/input', value['p79'])
            # 参数80
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[4]/input', value['p80'])
            # 参数81
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[5]/input', value['p81'])
            # 参数82
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[6]/input', value['p82'])
            # 参数83
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[7]/input', value['p83'])
            # 参数84
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[8]/input', value['p84'])
        finally:
            pass
    # 测温装置检测
    def Test20(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[3]/input', value['p2'])
        finally:
            pass
    # 绝缘油试验
    def Test21(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/div/input', value['p2'])
            driver.click('x,//*[@id="home"]/main/div/div/div[2]/p')
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[3]/td[2]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[4]/td[2]/input', value['p4'])
            # 参数5
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[5]/td[2]/input', value['p5'])
            # 参数6
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[6]/td[2]/input', value['p6'])
            # 参数7
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[7]/td[2]/input', value['p7'])
            # 参数8
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[8]/td[2]/input', value['p8'])
            # 参数9
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[9]/td[2]/input', value['p9'])
            # 参数10
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[10]/td[2]/input', value['p10'])
            # 参数11
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[11]/td[2]/input', value['p11'])
            # 参数12
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[12]/td[2]/input', value['p12'])
            # 参数13
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[13]/td[2]/input', value['p13'])
        finally:
            pass
    # 振动测量
    def Test22(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/div/input', value['p3'])
            driver.click('x,//*[@id="home"]/main/div/div/div[2]/p')
        finally:
            pass
    # 噪声测量
    def Test23(self, data):
        '''
        :param self:
        :param data:
        :return:
        '''
        try:
            driver = self.driver
            redis = GetRedis()
            value = redis.GetDate(data)
            value = ast.literal_eval(value)
            # 参数1

            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[5]/div/input', value['p4'])
            driver.click('x,//*[@id="home"]/main/div/div/div[2]/p')

            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[2]/input', value['p1'])
            # 参数2
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[3]/input', value['p2'])
            # 参数3
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[4]/input', value['p3'])
            # 参数4
            driver.input('x,//*[@id="home"]/main/div/div/div[2]/table/tr[2]/td[5]/div/input', value['p4'])
            driver.click('x,//*[@id="home"]/main/div/div/div[2]/p')
        finally:
            pass
    # 导则判断
    def Judgement(self):
        try:
            driver = self.driver
            driver.click('x,//span[text()="导则判断"]')
            result = driver.locate_element('x,//*[@id="home"]/main/div/div/div[2]/table/tr/td[2]/div/span')
            driver.wait(2)
            return result
        except Exception as e:
            driver.wait(5)
            return "No Restlt"
        finally:
            pass

    # 确认入库
    def Save(self):
        try:
            driver = self.driver
            driver.wait(3)
            driver.click('x,//span[text()="确认(入库)"]')
            driver.wait(2)
            inf = driver.locate_element('x,//p[text()="入库成功！"]').text
            driver.wait(2)
            return inf
        finally:
            pass

    # 录入完成
    def Input(self):
        try:
            driver = self.driver
            driver.wait(3)
            driver.click('x,//span[text()="录入完成"]')
            testName = driver.locate_element(
                'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[3]/div').text
            transformerName = driver.locate_element(
                'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[4]/div').text
            EQ_Name = driver.locate_element(
                'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[5]/div').text
            testType = driver.locate_element(
                'x,//*[@id="home"]/main/div/div[3]/div/div[1]/div/div[3]/table/tbody/tr[1]/td[7]/div/span').text
            # ['绝缘油溶解气体试验', '测试变电站', '测试变压器1', '预防']
            if testType == "出厂":
                testType = "出厂试验"
            else:
                testType = "预防性试验"
            return [testName, transformerName, EQ_Name, testType]
        finally:
            pass

    # 返回
    def Back(self):
        try:
            driver = self.driver
            driver.wait(4)
            driver.click('x,//span[text()="返回试验"]')
        finally:
            pass

    # 返回主界面
    def Home(self):
        try:
            driver = self.driver
            driver.wait(5)
            driver.click('x,//span[text()="试验管理"]')
        finally:
            pass

    # 获取变电站信息
    def GetTransformer(self):

        driver = self.driver
        driver.wait(3)
        # 系统管理
        driver.click('x,//*[@id="home"]/div/div/ul/li[2]/span')
        # 设备管理
        driver.click('x,//*[@id="home"]/main/div/div[2]/div[1]/ul/li[2]')
        # 搜索设备
        driver.input('x,//*[@id="home"]/main/div/div[1]/div[2]/div/div/input',self.transformer)
        # 点击查找
        driver.click('x,//*[@id="home"]/main/div/div[1]/button')
        driver.wait(2)
        temp = driver.locate_elements('x,//*[@id="home"]/main/div/div[3]/div[1]/div[3]/table/tbody/tr/td[2]/div')
        i=0
        for a in temp:
            temp[i]=a.text
            i = i + 1
        index = temp.index(self.E)+1
        # 点击查看详情
        driver.click(f'x,//*[@id="home"]/main/div/div[3]/div[1]/div[3]/table/tbody/tr[{index}]/td[8]/div/button[1]/span')
        # 额定容量
        capacity = driver.locate_element('x,/html/body/div[3]/div/div[2]/div[2]/table/tr[7]/td[3]/input').get_attribute('value')
        # 额定电压
        voltage = driver.locate_element('x,/html/body/div[3]/div/div[2]/div[2]/table/tr[7]/td[6]/input').get_attribute('value')
        # 油重
        weight = driver.locate_element('x,/html/body/div[3]/div/div[2]/div[2]/table/tr[20]/td[2]/input').get_attribute('value')
        # 高压
        height = driver.locate_element('x,/html/body/div[3]/div/div[2]/div[2]/table/tr[7]/td[6]/input').get_attribute('value')
        # 中亚
        center = driver.locate_element('x,/html/body/div[3]/div/div[2]/div[2]/table/tr[8]/td[4]/input').get_attribute('value')
        # 低压
        low = driver.locate_element('x,/html/body/div[3]/div/div[2]/div[2]/table/tr[9]/td[4]/input').get_attribute('value')
        # 取消
        driver.back()
        driver.wait(1)
        # 试验管理
        driver.click('x,//*[@id="home"]/div/div/ul/li[1]/span')
        driver.wait(3)
        return [capacity,voltage,weight,height,center,low]


if __name__ == '__main__':
    driver = BoxDriver()
    add = AddTestPage(driver)
    add.login()

    # Result = add.TestReport()
    # print(Result)
    add.Init(test_list='绝缘油溶解气体试验')
    x = add.GetTransformer()
    print(x)
    # add.Add()
    # add.Edit()
    # result = add.Test1('Test1_A')
    # print(result)
    # add.Judgement()
    # a = add.Save()
    # print(a)
    # inf = add.Input()
    # print(inf)
    # add.Find()
    # title = add.TestReport()
    # add.Find()
    # add.HomeDelete()
    # print(title)
