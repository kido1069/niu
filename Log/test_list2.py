
import allure
import pytest
from Common import Assert
from Common import Request
from Common import read_excel


assertions = Assert.Assertions()
request = Request.Request()

excel_list = read_excel.read_excel_list("./document/test.xlsx")
print(excel_list)
idsList = []

len1 = len(excel_list)
for i in range(len1):
    a = excel_list[i].pop()
    idsList.append(a)
print(excel_list)
print(idsList)


@allure.feature("演示模块")
class Testdemo(object):
    @allure.story("演示功能")
    @pytest.mark.parametrize('name,pwd,msg',excel_list,ids= idsList)
    def test_case_demo(self,name,pwd,msg):
        login_data = {"username": name, "password": pwd}
        login_resp = request.post_request(url="http://qa.guoyasoft.com:8099/admin/login", json=login_data)
        # .assert_code 用来断言 状态码 ; 第一个参数 填 响应的状态码, 第二个参数 期望值
        assertions.assert_code(login_resp.status_code, 200)
        # 获取响应正文  字典格式
        login_resp_json = login_resp.json()
        # .assert_in_text 用来断言字符 第一个参数填 比较多的那个字符; 第二参数填 这个字符 是否存在第一个字符里面
        assertions.assert_in_text(login_resp_json['message'], msg)