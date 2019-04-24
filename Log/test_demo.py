import allure
from Common import Assert
from Common import Request
import requests

# 新建一个 Assert.Assertions() 的对象 对象名: assertions
assertions = Assert.Assertions()

# 新建一个 Request.Request() 的对象 对象名: request
request = Request.Request()

myToken = ''
head = {'Authorization': myToken}
order_id=0
orderSn = ''
ym_url = 'http://192.168.60.132:8080/'

@allure.feature("登录模块")
class TestLogin(object):

    @allure.story("登录系统")
    def test_case_login(self):
        login_data = {"password": "123456", "username": "admin"}
        login_resp = request.post_request(url=ym_url+'admin/login', json=login_data)
        # .assert_code 用来断言 状态码 ; 第一个参数 填 响应的状态码, 第二个参数 期望值
        assertions.assert_code(login_resp.status_code, 200)
        # 获取响应正文  字典格式
        login_resp_json = login_resp.json()
        # .assert_in_text 用来断言字符 第一个参数填 比较多的那个字符; 第二参数填 这个字符 是否存在第一个字符里面
        assertions.assert_in_text(login_resp_json['message'],'成功')

        data_token = login_resp_json['data']
        token = data_token['token']
        token_head = data_token['tokenHead']

        # global : 引入 全局变量 然后才可以对全局变量重新赋值
        global myToken
        global head
        myToken = token_head + token
        head = {'Authorization': myToken}

    @allure.story("获取用户信息")
    def test_case(self):
        get_info_resp = request.get_request(url=ym_url+'admin/info', headers=head)

        assertions.assert_code(get_info_resp.status_code, 200)

    @allure.story("获取待发货列表")
    def test_case1(self):
        #url?k=v&k=v pageNum=1&pageSize=10&status=1
        param = {'pageNum': 1, 'pageSize': 10,'status':1}
        get_info_resp = request.get_request(url=ym_url+'order/list',params=param, headers=head)

        assertions.assert_code(get_info_resp.status_code, 200)
        json = get_info_resp.json()
        data_ = json['data']
        list_ = data_['list']
        list__ = list_[0]
        global order_id
        global orderSn
        order_id = list__['id']
        orderSn = list__['orderSn']

    @allure.story("发货")
    def test_case2(self):
        # url?k=v&k=v pageNum=1&pageSize=10&status=1
        json_data = [{"orderId":order_id,"orderSn":orderSn,"receiverName":"string","receiverPhone":"string","receiverPostCode":"string","address":"stringstringstringstring","deliveryCompany":"中通快递","deliverySn":"5464213231"}]
        get_info_resp = request.post_request(url=ym_url + 'order/update/delivery', json=json_data, headers=head)

        assertions.assert_code(get_info_resp.status_code, 200)

    @allure.story("关闭")
    def test_case3(self):
        # url?k=v&k=v pageNum=1&pageSize=10&status=1
        json_data = {'ids':order_id,'note':'哈哈'}
        get_info_resp = request.post_request(url=ym_url + 'order/update/close', params=json_data, headers=head)

        assertions.assert_code(get_info_resp.status_code, 200)

