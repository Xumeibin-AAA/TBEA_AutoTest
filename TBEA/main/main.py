import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

from TBEA.test_runner.Test_Runner import TestRunner

if __name__ == '__main__':
    runner = TestRunner()
    runner.runner()