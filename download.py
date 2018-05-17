import requests, os

certcode = 'http://payment.ucas.ac.cn/NetWorkUI/authImage'
sess = requests.Session()

def download(url, path, times=1):
    for i in range(times):
        print(i, times)
        name = os.path.join(path, '%d.png' % i)
        response = sess.get(url)
        with open(name, 'wb') as f:
            f.write(response.content)

if __name__ == '__main__':
    path = 'raw_data'
    if not os.path.isdir(path):
        os.mkdir(path)

    download(certcode, path, 1000)
