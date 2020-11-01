import requests
import base64
import sys
import json
import time
import os 
from os import path

headers = {'Content-Type': 'application/json'}

class ConvertioAPI():

    _API_URL = "https://api.convertio.co/convert";

    # 下载文件的URL, 最后的参数始终是 base64
    _API_DOWNLOAD_URL = "https://api.convertio.co/convert/{id}/dl/base64";

    _API_KEY = "bc85bd7ff546ec4ea7ed789e59390011"

    def fileToBase64(cls, filePath):
        """
        把文件专程base64
        filePath: 文件路径
        """
        with open(filePath, "rb") as file:
            encode = base64.b64encode(file.read())
            s = encode.decode()
            file.close()
        return s

    def base64ToFile(cls, b64_data, savePath, saveName):
        """
        把base64转成文件
        """
        
        with open(savePath[0] + ".pdf", 'wb') as file:
            b64_decode = base64.b64decode(b64_data)
            file.write(b64_decode)
            file.close()


    def putFile(self, filePath, ext):
        base64 = self.fileToBase64(filePath)
        
        # 用base64方法进行上传
        # 如果使用base64上传, 必须指定filename
        _dic = { 
            "apikey": self._API_KEY,
            "input": "base64",
            "file": base64,
            "filename": "",
            "outputformat": "pdf"
        }

        response = requests.post(self._API_URL, headers=headers, data=json.dumps(_dic).encode("utf-8"))

        return response.json();


    def downloadFile(self, id, minutes, savePath, saveName):
        """
        下载文件
        id: 服务器返回的数据
        minutes: 服务器转换文件的分钟数
        savePath: 保存文件的路径
        saveName: 保存文件的名称
        """
        print("等待{}分钟".format(minutes))
        time.sleep(minutes * 60)

        response = requests.get(self._API_DOWNLOAD_URL.format(id=id), headers=headers)
        _dic = response.json();
        self.base64ToFile(_dic['data']['content'], savePath, saveName)

if __name__ == "__main__":
    print("解析文件: ", sys.argv[1])

    # python 行第一行 "python main.py filePath"
    file = sys.argv[1]
    # python 获取文件完整路径(硬路径)
    path = path.abspath(file)
    print(path)
    # 只获取文件的路径, 不包含文件名
    filePath = os.path.splitext(path)
    # # 只获取文件的文件名
    (filename, ext) = os.path.splitext(path)

    convertioAPI = ConvertioAPI()
    response_data = convertioAPI.putFile(path, ext)

    if (response_data['code'] == 200):
        # 获取请求回来的data数据, 包含"id"与"minutes"
        data = response_data['data']
        convertioAPI.downloadFile(
            id=data['id'], 
            minutes=data['minutes'],
            savePath=filePath,
            saveName=filename,
            )

