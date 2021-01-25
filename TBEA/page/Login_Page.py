import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from TBEA.base.util import BasePage,BoxDriver

class LoginPage(BasePage):
    def login(self,username='tbea_guest1',password='123456'):
        driver = self.driver
        driver.input('x,//*[@id="app"]/div/div/div[2]/div[1]/input',username)
        driver.input('x,//*[@id="app"]/div/div/div[2]/div[2]/input', password)
        driver.click('x,//*[@id="app"]/div/div/div[2]/p/button')
        driver.wait(2)
    def logout(self):
        driver = self.driver
        driver.click('x,//html/body/div[1]/div/div/div/div[2]/div/span')
        driver.wait(2)
        driver.click('x,//html/body/ul/li[2]')
        driver.wait(2)
        driver.click('x,//html/body/div[2]/div/div[3]/button[2]/span')
        driver.wait(2)

    def get_login_name(self):
        driver = self.driver
        name = driver.locate_element('x,//html/body/div[1]/div/div/div/div[2]/div/span')
        return name.text
    def eq(self):
        driver = self.driver
        driver.click('x,//*[@id="home"]/div/div/ul/li[2]/span')




if __name__ == '__main__':
    driver = BoxDriver()
    login = LoginPage(driver)
    login.login()
    login.eq()
    login.get_login_name()
    login.logout()


