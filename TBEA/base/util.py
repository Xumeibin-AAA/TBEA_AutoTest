from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import random, yaml, time, openpyxl, logging, sys, smtplib, pymysql, configparser, redis
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class BoxDriver:

    def __init__(self, broswer_type='Chrome'):
        if broswer_type == 'Chrome':
            self.driver = webdriver.Chrome()
        elif broswer_type == 'Firefox':
            self.driver = webdriver.Firefox()
        elif broswer_type == 'Ie':
            self.driver = webdriver.Ie()

    def get(self, url):
        '''
        打开网页
        url: 网页的地址
        '''
        self.driver.get(url)

    def maximize_window(self):
        '''
        窗口最大化
        '''
        self.driver.maximize_window()

    def implicitly_wait(self, time=10):
        '''
        隐式等待
        time: 最大等待时间，单位是秒, 默认等待时间是10秒
        '''
        self.driver.implicitly_wait(time)

    def wait(self, second):
        '''
        休眠
        second: 休眠的时间，单位是秒
        '''
        time.sleep(second)

    def webdriver_wait(self, selector):
        '''
        显示等待元素
        selector: 自定义定位方式
        '''
        locator = self.selector_to_locator(selector)
        WebDriverWait(self.driver, 10, 0.05).until(EC.presence_of_element_located(locator))

    def selector_to_locator(self, selector):
        '''
        把自定义的selector定位方式转换为selenium标准定位方式
        'id, account' -> (By.ID, 'account')
        selector: 自定义定位方式
        '''
        # 定位方式
        by = selector.split(',')[0].strip()
        # 定位方式的值
        value = selector.split(',')[1].strip()
        if by == 'id' or by == 'i':
            locator = (By.ID, value)
        elif by == 'name' or by == 'n':
            locator = (By.NAME, value)
        elif by == 'class_name' or by == 'c':
            locator = (By.CLASS_NAME, value)
        elif by == 'link_text' or by == 'l':
            locator = (By.LINK_TEXT, value)
        elif by == 'partial_link_text' or by == 'p':
            locator = (By.PARTIAL_LINK_TEXT, value)
        elif by == 'tag_name' or by == 't':
            locator = (By.TAG_NAME, value)
        elif by == 'xpath' or by == 'x':
            locator = (By.XPATH, value)
        elif by == 'css_selector' or by == 'css':
            locator = (By.CSS_SELECTOR, value)

        return locator

    def locate_element(self, selector):
        '''
        定位单个元素
        selctor: 自定义定位方式
        '''
        locator = self.selector_to_locator(selector)
        element = self.driver.find_element(*locator)
        return element

    def locate_elements(self, selctor):
        '''
        定位多个元素
        selctor: 自定义定位方式
        '''
        locator = self.selector_to_locator(selctor)
        elements = self.driver.find_elements(*locator)
        return elements

    def click(self, selector):
        '''
        单击元素
        selctor: 自定义定位方式
        '''
        self.locate_element(selector).click()

    def input(self, selector, value):
        '''
        向文本框写入值
        selector: 自定义定位方式
        value: 要写入的值
        '''
        # 先清理一下
        element = self.locate_element(selector)
        element.clear()
        # 然后再写入
        element.send_keys(value)

    def refresh(self):
        self.driver.refresh()

    def quit(self):
        '''
        退出浏览器
        '''
        self.driver.quit()
    def back(self):
        '''
        后退
        '''
        self.driver.back();
    def close(self):
        '''
        关闭当前窗口
        '''
        self.driver.close()

    def switch_to_frame(self, selector):
        '''
        进入frame
        '''
        iframe = self.locate_element(selector)
        self.driver.switch_to.frame(iframe)

    def select_by_index(self, selector, index):
        '''
        根据index选择元素
        selector: 自定义定位方式
        index: 选项的索引
        '''
        dept_element = self.locate_element(selector)
        depts = Select(dept_element)
        # 选择部门
        depts.select_by_index(index)

    def select_by_value(self, selector, value):
        '''
        根据value选择元素
        selector: 自定义定位方式
        value: 选项的value值
        '''
        dept_element = self.locate_element(selector)
        depts = Select(dept_element)
        # 选择部门
        depts.select_by_value(value)

    def select_by_visible_text(self, selector, visible_text):
        '''
        根据visible_text选择元素
        selector: 自定义定位方式
        visible_text: 选项的索引
        '''
        dept_element = self.locate_element(selector)
        depts = Select(dept_element)
        # 选择部门
        depts.select_by_visible_text(visible_text)
        # 悬浮

    def Suspension(self, selector):
        driver = self.driver
        dept_element = self.locate_element(selector)
        ActionChains(driver).move_to_element(dept_element).perform()


class BasePage:

    def __init__(self, driver: BoxDriver):
        self.driver = driver
        self.driver.implicitly_wait()
        self.driver.maximize_window()
        self.driver.get('http://trial.tbeayun.com/')


class GetYaml:

    def load(self, file):
        '''
        加载yaml文件
        file: 文件路径
        '''
        with open(file, 'r', encoding='utf-8') as yaml_file:
            config = yaml.load(yaml_file.read(), Loader=yaml.BaseLoader)
        return config


class GetExcel:

    def load(self, workbook, worksheet):
        '''
        加载Excel文件
        workbook: 工作簿路径
        worksheet: 工作表名
        '''
        # 打开工作簿
        book = openpyxl.load_workbook(workbook)
        # 获取指定的工作表
        sheet = book[worksheet]

        data = [tuple(cell.value for cell in row) for row in sheet]
        return data[1:]


class GetLogger:

    def __init__(self, path):
        '''
        path: 日志文件的路径
        '''
        self.path = '%s\%s.log' % (path, time.strftime('%Y-%m-%d %H：%M'))
        # 创建日志
        self.logger = logging.getLogger()
        # 设置日志级别
        self.logger.setLevel(logging.WARNING)
        # 指定日志输出的内容与格式
        self.formatter = logging.Formatter('[%(asctime)s]-[%(filename)s]-[%(levelname)s]:%(message)s')

    def console(self, level, message):
        '''
        level: 日志等级
        message: 日志信息
        '''
        # 将日志写入到文件中，选取追加写模式
        fh = logging.FileHandler(self.path, mode='a', encoding='utf-8')
        # 设置文件日志等级
        fh.setLevel(logging.WARNING)
        # 设置日志的格式与内容
        fh.setFormatter(self.formatter)
        # 将内容添加到日志文件
        if not self.logger.handlers:
            self.logger.addHandler(fh)

        # 将日志输出到控制台
        sh = logging.StreamHandler(sys.stdout)
        # 设置控制台日志等级
        sh.setLevel(logging.DEBUG)
        # 设置日志的格式与内容
        sh.setFormatter(self.formatter)
        # 将内容添加到控制台
        self.logger.addHandler(sh)

        # 判断日志等级，进行相应的输出
        if level == 'debug':
            self.logger.debug(message)
            # 避免日志重复输出
            self.logger.removeHandler(sh)
            # 关闭日志文件
            fh.close()
        elif level == 'info':
            self.logger.info(message)
            # 避免日志重复输出
            self.logger.removeHandler(sh)
            # 关闭日志文件
            fh.close()
        elif level == 'warning':
            self.logger.warning(message)
            # 避免日志重复输出
            self.logger.removeHandler(sh)
            # 关闭日志文件
            fh.close()
        elif level == 'error':
            self.logger.error(message)
            # 避免日志重复输出
            self.logger.removeHandler(sh)
            # 关闭日志文件
            fh.close()
        elif level == 'critical':
            self.logger.critical(message)
            # 避免日志重复输出
            self.logger.removeHandler(sh)
            # 关闭日志文件
            fh.close()

        # 避免日志重复输出
        # self.logger.removeHandler(sh)
        # self.logger.removeFilter(fh)
        # # 关闭日志文件
        # fh.close()

    '''
    console('debug',message) -> debug(message)
    '''

    def debug(self, message):
        self.console('debug', message)

    def info(self, message):
        self.console('info', message)

    def warning(self, message):
        self.console('warning', message)

    def error(self, message):
        self.console('error', message)

    def critical(self, message):
        self.console('critical', message)


class Email:

    def send(self, subject, path):
        try:
            # 邮件服务器地址
            smtpserver = 'smtp.163.com'
            # 邮件服务器端口号
            port = 25

            # 发件人账号
            sender = 'yr10158094@163.com'
            # 邮箱密码
            pwd = 'ENKXDXFUDWVFAXRT'
            # 收件人
            receiver = 'moderator@163.com;zxx147298870@163.com;bxk3154143826@163.com;lethe_2020@163.com;fk2013302552@163.com'

            # 创建邮件对象
            mail = MIMEMultipart()
            # 初始化发件人
            mail['from'] = sender
            # 添加收件人
            mail['to'] = receiver
            # 添加主题
            mail['subject'] = subject

            # 读取报告内容
            with open(path, 'rb') as file:
                mail_body = file.read()

            '''邮件正文'''
            # 创建html格式的消息对象
            body = MIMEText(mail_body, 'html', 'utf-8')
            # 将报告内容添加到邮件正文当中
            mail.attach(body)

            '''邮件附件'''
            # 创建base64格式的对象
            att = MIMEText(mail_body, 'base64', 'utf-8')
            # 指定附件的类型
            att['Content-Type'] = 'application/octet-stream'
            # 指定浏览器的处理方式
            att['Content-Disposition'] = 'attachment;filename=%s' % path.split('\\')[-1]
            # 添加附件
            mail.attach(att)

            '''发送邮件'''
            # 创建SMTP对象
            smtp = smtplib.SMTP()
            # 连接服务器
            smtp.connect(smtpserver, port)
            # 登陆
            smtp.login(sender, pwd)
            # 发送
            smtp.sendmail(sender, receiver.split(';'), mail.as_string())
            # 关闭邮件服务
            smtp.close()
            print('邮件%s发送完毕!' % subject)
        except:
            raise NameError('邮件发送失败！')


class GetTxt:
    @staticmethod
    def get(path):
        with open(path, mode='r', encoding='utf-8') as file:
            arr = file.read().split('\n')
            file.close()
            return arr


# 读取ini文件
class Getini:
    def get(self, key):
        con = configparser.ConfigParser()
        con.read(r'.\data\DB.ini')
        return con.get('DB', key)


# 连接数据库
def connect():
    try:
        conn = pymysql.connect(host=Getini().get('host'), port=int(Getini().get('port')), user=Getini().get('user'),
                               password=Getini().get('password'), database=Getini().get('name'), charset='utf8')
        print('数据库连接成功')
    except Exception as e:
        print(f"连接数据库异常，异常信息为{e}")
    return conn


# 断开数据库
def disconnect(conn):
    try:
        conn.close()
        print("断开数据库成功")
    except Exception as e:
        print(f"断开数据库失败,异常信息为{e}")


# 执行sql语句
def execute(conn, sql):  # 连接相当于一条到数据库的路
    try:
        cursor = conn.cursor()  # 获取游标 相当于路上的一辆车
        a = cursor.execute(sql)
        temp = cursor.fetchall()

        conn.commit()  # 提交
        cursor.close()  # 关闭游标

        print(f"执行Sql语句{sql}成功")
        return temp
    except Exception as e:
        print(f"执行Sql语句{sql}失败,异常信息为{e}")


class GetRedis:
    def GetDate(self, key):
        '''
        :param Key:
        :return:
        '''
        r = redis.Redis(host='127.0.0.1', port=6379, encoding='utf-8')  # 只要设置了redis的密码，在连接时需要输入密码
        val = r.get(key).decode()
        return val

    def GetDate_H(self, Test_name, Key):
        '''
        :param Test_name:
        :param Key:
        :return:
        '''
        r = redis.Redis(host='127.0.0.1', port=6379, encoding='utf-8')  # 只要设置了redis的密码，在连接时需要输入密码
        val = r.hget(Test_name, Key).decode()
        return val


if __name__ == "__main__":
    # Email().send('报告',r'D:\workspace\selenium\ranzhi\report\report_2020-10-20_16-37-39.html')
    b = connect()
    x = 1
    f = execute(b, 'select * from user limit %d' % x)
    disconnect(b)
    i = 0

    for j in f:
        i = i + 1
        print(i)
        print(j)
