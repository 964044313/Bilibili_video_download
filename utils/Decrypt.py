# -*- coding:utf-8 -*-
import requests  # 引入 requests 模块
import json  # 引入 json 模块

class Decrypt(object):
    _Str = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'  # 准备的一串指定字符串
    _Dict = {}  # 建立一个空字典

    # 将字符串的每一个字符放入字典一一对应 ， 如 f对应0 Z对应1 一次类推。
    for i in range(58):
        _Dict[_Str[i]] = i
    # print(tr) #如果你实在不理解请将前面的注释去掉，查看字典的构成

    s = [11, 10, 3, 8, 4, 6, 2, 9, 5, 7]  # 必要的解密列表
    xor = 177451812  # 必要的解密数字 通过知乎大佬的观察计算得出 网址：https://www.zhihu.com/question/381784377
    add = 100618342136696320  # 这串数字最后要被减去或加上

    # 1.在线转化 2.算法转化
    def __init__(self, n=2):
        self.n = n

    # 解密BV号
    def _algorithm_dec(self, bv):
        if bv.find('BV') == -1:
            bv = 'BV' + bv

        r = 0
        # 下面的代码是将BV号的编码对照字典转化并进行相乘相加操作 **为乘方
        for i in range(10):
            r += self._Dict[bv[self.s[i]]] * 58 ** i
        # 将结果与add相减并进行异或计算

        # print('计算成功！请求返回的视频av号为：av' + str((r - self.add) ^ self.xor))
        # print('输入网址访问视频： https://www.bilibili.com/video/av' + str((r - self.add) ^ self.xor))
        # print('输入网址访问视频： https://www.bilibili.com/video/' + bv)
        return str((r - self.add) ^ self.xor)

    def algorithm_dec(self, bv):
        if self.n == 1:  # 在线功能转化
            # video = input('输入AV号或BV号（可以加AV或BV，也可以是网址）：')
            return self._Online_dec(self._video_trbv(bv)).get("av")
        elif self.n == 2:
            # video = input('输入AV号或BV号（可以加AV或BV，也可以是网址）：')
            return self._algorithm_dec(self._video_trbv(bv))
        else:
            print("抱歉您输入的代码不正确！请输入1或者2。")

    # 加密AV号
    def _algorithm_enc(self, av):
        ret = av
        av = int(av)
        # 将AV号传入结果进行异或计算并加上 100618342136696320
        av = (av ^ self.xor) + self.add
        # 将BV号的格式（BV + 10个字符） 转化成列表方便后面的操作
        r = list('BV          ')
        # 将传入的数字对照字典进行转化
        for i in range(10):
            r[self.s[i]] = self._Str[av // 58 ** i % 58]
        # 将转化好的列表数据重新整合成字符串

        # print('计算成功！请求返回的视频BV号为：' + ''.join(r))
        # print('输入网址访问视频： https://www.bilibili.com/video/av' + str(ret))
        # print('输入网址访问视频： https://www.bilibili.com/video/' + ''.join(r))
        return ''.join(r)

        # 加密AV号

    def algorithm_enc(self, av):
        # User = input("----------\n输入 1.在线转化 2.算法转化\n请输入功能代码：")  # 引导用户输入
        if self.n == 1:  # 在线功能转化
            # video = input('输入AV号或BV号（可以加AV或BV，也可以是网址）：')
            return self._Online_enc(self._video_trav(av)).get("BV")
        elif self.n == 2:
            # video = input('输入AV号或BV号（可以加AV或BV，也可以是网址）：')
            return self._algorithm_enc(self._video_trav(av)).get("BV")
        else:
            print("抱歉您输入的代码不正确！请输入1或者2。")

    def _Online_enc(selkf, av):
        av = av.strip()
        try:
            headers = {
                'Host': "api.bilibili.com",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            }
            data = requests.get('http://api.bilibili.com/x/web-interface/archive/stat?aid=%s' % (av),
                                headers=headers)  # 获取视频源数据
            if data.content.decode('utf-8').find('由于触发哔哩哔哩安全风控策略，该次访问请求被拒绝。') != -1:
                raise BaseException('接口访问次数更多，触发了BiliBili安全机制！')
            information = json.loads(data.content.decode('utf-8'))  # 解析数据为字典
            if information['code'] != -400:  # 请求错误
                print('在线请求成功！请求返回的视频BV号为：' + str(information["data"]["bvid"]))
                print('输入网址访问视频： https://www.bilibili.com/video/' + str(information["data"]["bvid"]))
                print('输入网址访问视频： https://www.bilibili.com/video/av' + str(information["data"]["aid"]))
                return {
                    "av": str(information["data"]["aid"]),
                    "BV":  str(information["data"]["bvid"])
                }
            else:
                print(
                    '访问接口拒绝了我们的请求，可能是您的输入错误！返回代码：%d 返回消息：%s' % (information['code'], information['message']))  # 输出错误文本
        except BaseException as Error:
            print('访问在线接口时出现错误，原因：' + str(Error))

    def _video_trbv(self, video: str):
        try:
            up = video.find('/BV')
            down = video.find('?', up + 3)
            if up != -1:  # 输入网址
                if down != -1:  # 结尾有东西
                    return video[up + 3:down]
                else:
                    return video[up + 3:]
            elif video.find('BV') != -1:  # 找到bv
                return video[video.find('BV') + 2:]
            else:
                return video
        except:
            print('BV（网址）输入错误！无法转化！')

    def _video_trav(self, video: str):
        try:
            video = video.lower()
            up = video.find('/av')
            down = video.find('?', up + 3)
            if up != -1:  # 输入网址
                if down != -1:  # 结尾有东西
                    return video[up + 3:down]
                else:
                    return video[up + 3:]
            elif video.find('av') != -1:  # 找到bv
                return video[video.find('av') + 2:]
            else:
                return video
        except:
            print('av（网址）输入错误！无法转化！')

    def _Online_dec(self, bv):
        bv = bv.strip()
        try:
            headers = {
                'Host': "api.bilibili.com",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            }
            data = requests.get('http://api.bilibili.com/x/web-interface/archive/stat?bvid=%s' % (bv),
                                headers=headers)  # 获取视频源数据
            if data.content.decode('utf-8').find('由于触发哔哩哔哩安全风控策略，该次访问请求被拒绝。') != -1:
                raise BaseException('接口访问次数更多，触发了BiliBili安全机制！')
            information = json.loads(data.content.decode('utf-8'))  # 解析数据为字典
            if information['code'] != -400:  # 请求错误
                print('在线请求成功！请求返回的视频av号为：av' + str(information["data"]["aid"]))
                print('输入网址访问视频： https://www.bilibili.com/video/av' + str(information["data"]["aid"]))
                print('输入网址访问视频： https://www.bilibili.com/video/' + str(information["data"]["bvid"]))
                return {
                    "av": str(information["data"]["aid"]),
                    "BV": str(information["data"]["bvid"])
                }
            else:
                print(
                    '访问接口拒绝了我们的请求，可能是您的输入错误！返回代码：%d 返回消息：%s' % (information['code'], information['message']))  # 输出错误文本
        except BaseException as Error:
            print('访问在线接口时出现错误，原因：' + str(Error))


if __name__ == '__main__':
    decrypt = Decrypt()
    print(decrypt.algorithm_dec("https://www.bilibili.com/video/BV1i54y1h75W?p=5"))
    # User = input("----------\n输入 1.在线转化 2.算法转化\n请输入功能代码：")  # 引导用户输入
    # if User == '1':  # 在线功能转化
    #     video = input('输入AV号或BV号（可以加AV或BV，也可以是网址）：')
    #     try:
    #         int(video)
    #     except:
    #         decrypt._Online_dec(decrypt._video_trbv(video))
    #     else:
    #         decrypt._Online_enc(decrypt._video_trav(video))
    # elif User == "2":
    #     video = input('输入AV号或BV号（可以加AV或BV，也可以是网址）：')
    #     try:
    #         int(video)
    #     except:
    #         if video.find('av') != -1:  # av号
    #             print(decrypt.algorithm_enc(decrypt._video_trav(video)))
    #         else:
    #             print(decrypt.algorithm_dec(decrypt._video_trbv(video)))
    #     else:
    #         decrypt.algorithm_enc(decrypt._video_trav(video))
    #     pass
    # else:
    #     print("抱歉您输入的代码不正确！请输入1或者2。")
