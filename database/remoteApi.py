import requests
import config
import json

headers =  {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer '+ '6519354306:AAHPRTzd4K367CwDQhVkFqjpdqwk274MpI8'
        }
class RemoteApi():
    _api_ = 'http://54.199.118.210/api'
  
    # 注册用户
    def add_user(self,user_id,username):
        url = self._api_ + '/user/telegram'
        data = {'tg_id':str(user_id),'username':username}
        payload = json.dumps(data)
        res = requests.post(url,data=payload,headers=headers).json()
        return res
    # 绑定钱包
    def bind_wallet(self,user_id,username,address):
        url = self._api_ + '/user/bundle_address'
        data = {'tg_id':str(user_id),'username':username,'address':address}
        res = requests.post(url,data=json.dumps(data),headers=headers).json()
        if(res.get('status_code') == 200):
          return res.get('data')
        else:
            return None
    # 获取当前账户信息
    def get_balance(self,user_id):
        url = self._api_ + '/user/tg/{user_id}'.format(user_id=str(user_id))
        res = requests.get(url,headers=headers).json()
        if(res.get('status_code') == 200):
          return res.get('data')
        else:
            return None
    # 游戏每一轮更新
    def update_game(self,user_id,amount,wins,loses):
        url = self._api_ + '/user/updategame'
        data = {'tg_id':str(user_id),'amount':amount,'wins':wins,'loses':loses}
        res = requests.post(url,data=json.dumps(data),headers=headers).json()
        return res
    # 提交充值
    def recharge(self,user_id,username,network,address,coin):
        url = self._api_ + '/order/create'
        data = {'tg_id':str(user_id),'network':network,'username':username,'address':address,'coin':coin}
        res = requests.post(url,data=json.dumps(data),headers=headers).json()
        print(res)
        if(res.get('status_code') == 200):
          print(res)
        else:
            return None
    # 提现
    def withdraw(self,user_id,username,network,address,coin,amount):
        url = self._api_ + '/withdraw/create'
        data = {'tg_id':str(user_id),'network':network,'username':username,'address':address,'coin':coin,'amount':amount}
        res = requests.post(url,data=json.dumps(data),headers=headers).json()
        return res
