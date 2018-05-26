import numpy as np
from .raw_data import recognition
from commom import cfg as ucasbus_cfg


try:
    import cv2
    pattern = np.array(\
            [cv2.imread('certcode/%d.png'%i, 0) for i in range(10)])
    pattern = pattern.reshape(10, -1).transpose()
    recognition_status = True
except:
    recognition_status = False


def auto_recognition_attemps(eric, attemps=ucasbus_cfg.attemps):
    msg = []
    if attemps == 0:
        return 9, msg, None
    msg += ['[LOG] using auto-recognition now, if error, please report to admin']
    for i in range(attemps):
        path = eric.get_certcode(prefix=True)
        img = cv2.imread(path, 1)
        certcode = recognition(img, pattern)
        s = '%d%d%d%d'%(certcode[0], certcode[1], certcode[2], certcode[3])
        res, log, data = eric.login(s)
        msg += log
        if res == 0:
            return 0, msg, data
    return 9, msg, None

