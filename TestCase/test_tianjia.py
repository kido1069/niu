from Common import Request, Assert,read_excel
import allure
import pytest

request = Request.Request()
assertion = Assert.Assertions()
url = 'http://192.168.1.137:8080/'
head = {}
sku_id = 0
idlist = []
excel_list = read_excel.read_excel_list('../document/youhui.xlsx')
length =len(excel_list)
for i in range(length):
    idlist.append(excel_list[i].pop())


@allure.feature("商品模块")
class Test_sku:

    @allure.story("登录")
    def test_login(self):

        login_resp = request.post_request(url=url + 'admin/login',
                                          json={"username": "admin", "password": "123456"})

        resp_text = login_resp.text
        print(type(resp_text))

        resp_dict = login_resp.json()
        print(type(resp_dict))

        assertion.assert_code(login_resp.status_code, 200)
        assertion.assert_in_text(resp_dict['message'], '成功')

        data_dict = resp_dict['data']

        token = data_dict['token']
        tokenhead = data_dict['tokenHead']
        global head
        head = {'Authorization': tokenhead + token}

    @allure.story('获取优惠券')
    def test_niu(self):

        get_sku_rep = request.get_request(url=url+'coupon/list',params={'pageNum': 1, 'pageSize': 10} ,headers= head)
        reat = get_sku_rep.json()
        json_data = reat['data']
        pad = json_data['list']
        item = pad[0]
        global sku_id
        sku_id = item['id']
        assertion.assert_code(get_sku_rep.status_code, 200)
        assertion.assert_in_text(reat['message'], '成功')

    @allure.story('删除优惠券')
    def test_niubi(self):
        nn = request.post_request(url= url+'coupon/delete/'+str(sku_id),headers=head)
        re = nn.json()
        assertion.assert_code(nn.status_code, 200)
        assertion.assert_in_text(re['message'], '成功')

    @allure.story('批量添加优惠券')
    @pytest.mark.parametrize("name,amount,minPoint,publishCount,msg", excel_list, ids=idlist)
    def test_daniu(self,name,amount,minPoint,publishCount,msg):
        json = {"type":0,"name":name,"platform":0,"amount":amount,"perLimit":1,"minPoint":minPoint,
                "startTime":'2019-03-31T16:00:00.000Z',"endTime":"2019-04-16T16:00:00.000Z","useType":0,"note":'',"publishCount":publishCount,
                "productRelationList":[],"productCategoryRelationList":[]}
        add = request.post_request(url= url +'coupon/create',json = json,headers=head )

        read = add.json()
        assertion.assert_code(add.status_code,200)
        assertion.assert_in_text(read['message'],msg)