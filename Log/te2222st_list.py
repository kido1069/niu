import allure
import pytest
from Common import Assert
from Common import Request
from Common import read_excel

# 新建一个 Assert.Assertions() 的对象 对象名: assertions
assertions = Assert.Assertions()
request = Request.Request()
# 读取 ./document/test.xlsx 这个excel  获得 一个list : excel_list
excel_list = read_excel.read_excel_list('../document/test.xlsx')
# 声明一个空list : idsList
idsList = []
# 获取 excel_list 的长度
len1 = len(excel_list)
# 遍历 excel_list
for i in range(len1):
    #  将excel_list 每个元素的最后一位 删掉 , 并取出来 添加到 idsList 里面
    idsList.append(excel_list[i].pop())


# 数据驱动测试

@allure.feature("演示模块")
class Testdemo(object):

    @allure.story("演示功能")
    @pytest.mark.parametrize("name,pwd,msg",
            excel_list,
            ids=idsList)
    def test_case_demo(self,name,pwd,msg):
        login_data = {"username":name , "password": pwd}
        login_resp = request.post_request(url="http://qa.guoyasoft.com:8099/admin/login", json=login_data)
        # .assert_code 用来断言 状态码 ; 第一个参数 填 响应的状态码, 第二个参数 期望值
        assertions.assert_code(login_resp.status_code, 200)
        # 获取响应正文  字典格式
        login_resp_json = login_resp.json()
        # .assert_in_text 用来断言字符 第一个参数填 比较多的那个字符; 第二参数填 这个字符 是否存在第一个字符里面
        assertions.assert_in_text(login_resp_json['message'], msg)
        print(excel_list)
        print(idsList)