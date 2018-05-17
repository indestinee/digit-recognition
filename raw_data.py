import os, cv2
import numpy as np


def split(img):# {{{
    img[img>127] = 255
    img[img!=255]= 0
    img = img[2:-2, 5:-5]
    img = np.minimum(img[:, :, 0], img[:, :, 1], img[:, :, 2])

    shape = img.shape
    
    y = shape[1] // 4
    
    p = [img[:, z: z+y] for z in range(0, img.shape[1], y)]

    def work(pp):
        x = np.where(pp==0)[1]
        mini = min(x)
        maxi = max(x)
        img = np.ones((20, 20), np.uint8) * 255
        pp = pp[:, mini: maxi+1]
        img[:pp.shape[0], :pp.shape[1]] = pp
        return img

    p = [work(pp) for pp in p]
    return p# }}}

def recognition(img, pattern):# {{{
    x = split(img)
    p = np.array(x).reshape(4, -1).astype(int)
    for i in range(10):
        print(sum((p[0] - pattern[:, i])**2))
    loss = np.sum((p**2), axis=1, keepdims=True) - \
            2 * np.matmul(p, pattern) + \
            np.sum((pattern**2), axis=0, keepdims=True)
    result = np.argmin(loss, axis=1)
    return result
# }}}

if __name__ == '__main__':

    raw_path = 'raw_data'
    imgs = os.listdir(raw_path)
    t10 = [np.zeros((20, 20), int) for i in range(10)]
    cnt = [0] * 10
    for img_name in imgs:
        num = img_name.split('.')[0]
        if len(num) != 4:
            continue
        a, b, c, d = num
        a, b, c, d = map(int, [a, b, c, d])
        num = [a, b, c, d]

        img = cv2.imread(os.path.join(raw_path, img_name))
        
        p = split(img)

        # cv2.imshow('img', img)
        
        for index, i in enumerate(num):
            t10[i] += p[index]
            cnt[i] += 1
        
    i10 = []
    for i in range(10):
        if cnt[i] == 0:
            img = np.ones((20, 20), np.uint8)
        else:
            img = (t10[i] / cnt[i]).astype(np.uint8)
        i10.append(img)

    img = np.concatenate(i10, axis=1)
    cv2.imshow('img', img)
    cv2.waitKey(1)

    pattern = np.array(i10).reshape(10, -1).transpose().astype(int)


    t10 = [np.zeros((20, 20), int) for i in range(10)]
    cnt = [0] * 10
    for img_name in imgs:
        num = img_name.split('.')[0]

        img = cv2.imread(os.path.join(raw_path, img_name))
        
        p = split(img)
        result = recognition(img, pattern)
        
        for index, i in enumerate(result):
            t10[i] += p[index]
            cnt[i] += 1

    i10 = []
    for i in range(10):
        if cnt[i] == 0:
            img = np.ones((20, 20), np.uint8)
        else:
            img = (t10[i] / cnt[i]).astype(np.uint8)
        i10.append(img)

    img = np.concatenate(i10, axis=1)
    cv2.imshow('img', img)

    for i, each in enumerate(i10):
        cv2.imwrite('%d.png'%i, each)

    cv2.waitKey(0)
