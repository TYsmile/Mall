import pickle
import base64
from django.test import TestCase

# Create your tests here.
if __name__ == "__main__":
    # =============================== 设置购物车cookie数据 ===============================
    # cart_dict = {
    #     1: {
    #         'count': 2,
    #         'selected': True
    #     },
    #     3: {
    #         'count': 1,
    #         'selected': False
    #     }
    # }
    #
    # # 将obj转换成bytes字节流
    # # res = pickle.dumps(cart_dict)
    # # print(res)
    # # # base64编码
    # # res = base64.b64encode(res)
    # # print(res)
    # # # bytes转成str
    # # res = res.decode()
    # # print(res)
    #
    # # 以上代码的综合
    # res = base64.b64encode(pickle.dumps(cart_dict)).decode()
    # print(res)


    # =============================== 设解析cookie中购物车数据 ===============================
    # cart_data = 'gAN9cQAoSwF9cQEoWAUAAABjb3VudHECSwJYCAAAAHNlbGVjdGVkcQOIdUsDfXEEKGgCSwFoA4l1dS4='
    #
    # # res = base64.b64decode(cart_data)
    # # print(res)
    # # res = pickle.loads(res)
    # # print(res)
    #
    # # 以上代码的综合
    # res = pickle.loads(base64.b64decode(cart_data))
    # print(res)
    pass


if __name__ == "__main__":
    # ========================= pickle.dumps =============================
    # cart_dict = {
    #     1: {
    #         'count': 2,
    #         'selected': True
    #     },
    #     3: {
    #         'count': 1,
    #         'selected': False
    #     }
    # }
    #
    # # 将obj转换成bytes字节流
    # res = pickle.dumps(cart_dict)
    # print(res)


    # ========================= pickle.loads =============================
    # data = b'\x80\x03}q\x00(K\x01}q\x01(X\x05\x00\x00\x00countq\x02K\x02X\x08\x00\x00\x00selectedq\x03\x88uK\x03}q\x04(h\x02K\x01h\x03\x89uu.'
    # # 将bytes字节流转换成obj
    # res = pickle.loads(data)
    # print(res)
    pass




