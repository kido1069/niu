
from Common import Request, Assert
import allure


request = Request.Request()

assertion = Assert.Assertions()

@allure.feature("登录功能")
class Test_login:

    @allure.story("登录")
    def test_login(self):
        # =后面 :  request对象 调用了  post_request  方法,传入了两个参数
        # = 前面:  将方法 返回的 对象/变量  起一个名字
        login_resp = request.post_request(url='http://192.168.1.137:8080/admin/login',
                                            json={"username": "admin", "password": "123456"})

        # 响应 . text  :  就是获取 text属性的内容,这个就是 响应正文 (str 格式)
        resp_text = login_resp.text
        print(type(resp_text))

        # 响应 .json()  :  就是获取 字典格式的内容,这个就是 响应正文 (字典 格式)
        resp_dict = login_resp.json()
        print(type(resp_dict))

        assertion.assert_code(login_resp.status_code,200)
        assertion.assert_in_text(resp_dict['message'],'成功')