import random
import datetime
import string
import cv2
import numpy as np
def random_string_generator(size=7, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_tender_id_generator(instance):
    date = datetime.datetime.now()
    x = str(date.year)+(str(date.month) if len(str(date.month))==2 else'0'+str(date.month))+str(date.day)
    order_new_id = random_string_generator()
    order_new_id = "T" + x + order_new_id
    Klass= instance.__class__

    qs_exists= Klass.objects.filter(bidID= order_new_id).exists()
    if qs_exists:
        return unique_tender_id_generator(instance)
    return order_new_id

def unique_bidpart_id_generator(instance):
    date = datetime.datetime.now()
    x = str(date.year)+(str(date.month) if len(str(date.month))==2 else'0'+str(date.month))+str(date.day)
    order_new_id = random_string_generator(size=10)
    order_new_id = "BP" + x + order_new_id
    Klass= instance.__class__

    qs_exists= Klass.objects.filter(bidPartID= order_new_id).exists()
    if qs_exists:
        return unique_bidpart_id_generator(instance)
    return order_new_id

class generate_share(object):
    m = 256
    A = 71
    B = random.randint(31,255)
    @classmethod
    def encryption(cls,original_img):
        """
        Encryption of image 
        """
        height = original_img.shape[0]
        width = original_img.shape[1]
        for i in range(0,height):
            for j in range(0,width):
                a = original_img[i][j]      # rgb list
                r = (A*a[0] + B)%m
                g = (A*a[1] + B)%m
                b = (A*a[2] + B)%m
                original_img[i][j] = [r,g,b]
            
        return cv2.imwrite('media/encrypted_img.png', original_img)

    def createShare(self,original_img,n):
        height = original_img.shape[0]
        width = original_img.shape[1]
        blank_image = np.zeros((height,width,3), np.uint8)
        for share in range(0,n):
            if share < n-1 :
                for i in range(0,height):
                    for j in range(0,width):
                        # a = temp_img[i][j]
                        r = random.randint(0,255)
                        g = random.randint(0,255)
                        b = random.randint(0,255)
                        blank_image[i][j] = [r,g,b]
                cv2.imwrite('media/random{}.png'.format(share+1),blank_image)
            if share == 0:
                cv2.imwrite('media/share{}.png'.format(share+1),blank_image)

            elif share > 0 and share <= n-2 :
                temp_img = cv2.imread('media/random{}.png'.format(share))
                for i in range(0,height):
                    for j in range(0,width):
                        a = blank_image[i][j]
                        b = temp_img[i][j]
                        temp_img[i][j] = [(a[0]^b[0]), (a[1]^b[1]), (a[2]^b[2])]
                cv2.imwrite('media/share{}.png'.format(share+1),temp_img)

            else:
                temp_img = cv2.imread('media/random{}.png'.format(share))
                for i in range(0,height):
                    for j in range(0,width):
                        a = temp_img[i][j]
                        b = original_img[i][j]
                        temp_img[i][j] = [(a[0]^b[0]), (a[1]^b[1]), (a[2]^b[2])]

                cv2.imwrite('media/share{}.png'.format(share+1), temp_img)
