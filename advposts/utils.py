# from advposts.models import AdvDetails, BidDetails
from accounts.models import AccountUser
from advposts.models import BidDetails
from org.models import OrgUser
import random
import datetime
import string
import cv2
import os
import numpy as np
from advposts.signals import post_creation
from django.dispatch import receiver

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

m = 256
A = 71
B = random.randint(31,255)
def encryption(original_img):
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

def startGen(absolute_path,ctx):
    image = cv2.imread(absolute_path,1) #"/home/hackhard/django-upload-example/"+
    image=cv2.resize(image,(240,240))
    a=encryption(image)
    n=4
    b=createShare(image,n,ctx)

def createShare(original_img,n,ctx):
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
    
    post_creation.send(sender=createShare,ctext=ctx)

'''
    Receiver for Signal
    This add share to the Organisation Member account
'''
@receiver(post_creation)
def post_share_creation(**kwargs):
    print("Starting to assign shares")
    ctxData = kwargs['ctext']
    members = OrgUser.objects.filter(organization=ctxData['adv_detail'].organisation).filter(is_admin = False)
    bidder = AccountUser.objects.get(pk = ctxData['bidder'])
    b = str(ctxData['adv_detail'].tenderID) # 36 character
    i = str(ctxData['adv_detail'].organisation.pk) 
    d = str(ctxData['bidder'])
    
    for member,share in zip(members,range(1,5)):
        s = BidDetails.objects.create(
            bidID = b+'-'+i+'-'+d,
            tenderID = ctxData['adv_detail'],
            bidderID = bidder,
            orgID = ctxData['adv_detail'].organisation,
            partHolderID = member,
            bidFilePath = "media/share{}.png".format(share)
        )
    
    print(kwargs['ctext'])
    print("Assign Complete")

############################################################################
########                                                            ######## 
########                 SHARE COMBINATION                          ########    
########                                                            ########
############################################################################
def combine_share(path_list):
    HERE = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(HERE, path_list[0])
    img1 = cv2.imread(image_path,1)
    if img1 is None:
        print("failed to load 1")
    
    image_path = os.path.join(HERE, path_list[1])
    img2 = cv2.imread(image_path,1)
    if img2 is None:
        print("failed to load 2")
    
    image_path = os.path.join(HERE, path_list[2])
    img3 = cv2.imread(image_path,1)
    if img3 is None:
        print("failed to load 3")
    
    image_path = os.path.join(HERE, path_list[3])
    img4 = cv2.imread(image_path,1)
    if img4 is None:
        print("failed to load 4")

    height = img1.shape[0]
    width = img1.shape[1]
    pr =0
    for i in range(0,height):
        for j in range(0, width):
            img1_px = img1[i][j]
            img2_px = img2[i][j]
            img3_px = img3[i][j]
            img4_px = img4[i][j]

            px1 = [(img1_px[0]^img2_px[0]), (img1_px[1]^img2_px[1]), (img1_px[2]^img2_px[2])]    
            px2 = [(px1[0]^img3_px[0]), (px1[1]^img3_px[1]), (px1[2]^img3_px[2])]
            px = [(px2[0]^img4_px[0]), (px2[1]^img4_px[1]), (px2[2]^img4_px[2])]
        
            if(pr ==  0):
                pr=1 
            img1[i][j] = px
            
    cv2.imwrite('result.png',img1)