import os
import logging
import traceback
from datetime import datetime
import sys
print(f"Python 路径: {sys.executable}")
print(f"Python 版本: {sys.version}")

class MyClass:
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        
        # 日志记录
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler('error.log')
        self.handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    # 主函数
    def main(self):
        print("This is May!")

    def method1(self):
        try:
            # 在这里编写方法1的代码
            print("This is method 1")
            
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            self.logger.error(traceback.format_exc())
            screenshot_name = f"error_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            # self.driver.save_screenshot(screenshot_name)

    def method2(self):
        try:
            # 在这里编写方法1的代码
            print("This is method 2")
            
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            self.logger.error(traceback.format_exc())
            # 如果是selenium才能打开截图
            # screenshot_name = f"error_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            # screenshot_path = os.path.join("报错截图", screenshot_name)
            # self.driver.save_screenshot(screenshot_path)

if __name__ == "__main__":
    # 在这里编写当模块作为主程序执行时的代码
    obj = MyClass(1, 2)
    obj.main()
    obj.method1()
    obj.method2()