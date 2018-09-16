import cv2
from tkinter import *
from PIL import Image as Img
from PIL import ImageSequence as Ims
from tkinter.filedialog import *
from shutil import rmtree
import os
import imageio
info = {
    'path':[]
}  #用 字典型 info 来存放 所读取所有文件的 path

def analyze(pic,index):
    # 人脸提取— > 预设图片— > 重合— > 合成gif图保存
    cascPath = "haarcascade_frontalface_default.xml"
    hc = cv2.CascadeClassifier(cascPath)
    faces = hc.detectMultiScale(pic)
    i = 1
    if not os.path.exists('./pic'):  # 在pic下 根据人脸数目创建不同文件夹  存放
        os.makedirs('./pic')
    for face in faces:
        c='./pic/face_%d' % i
        if not os.path.exists(c):    #在pic下 根据人脸数目创建不同文件夹  存放
            os.makedirs(c)
        imgROI = pic[face[1]:face[1] + face[3], face[0]:face[0] + face[2]]
        s = c+'/%d.png' %index
        cv2.imwrite(s, imgROI)
        i = i + 1

def make_app():
    app = Tk()
    Label(app,text='compress tool', font=('Arial', 10)).pack()
    Listbox(app, name='lbox', bg='#f2f2f2').pack(fill=BOTH, expand=True)
    Button(app,text='| pick |', command=select).pack()
    Button(app,text='| start |', command=compress).pack()
    app.geometry('300x400')
    return app

def compress():
   for f in info['path']:
        output = f.split('/')[-1]       #在本程序目录下输出图片可以更改
        gif = Img.open(f)
        imgs = [i.copy() for i in Ims.Iterator(gif)]
        index = 0
        file = 'F:/%s' % output
        os.makedirs(file)
        for frame in imgs:
            frame.save(file+"/%d.png" % index)  #当然这里用quality=N 下面就不需要对读出来数据处理
            im = cv2.imread(file+"/%d.png" % index)
            analyze(im,index)
            index += 1
        files=os.listdir('./pic')
        i=1
        back=Img.open('./background.png')
        back_w = back.size[0]
        back_h = back.size[1]
        img2 = back.convert('1')
        for f in files:
            indexx=1
            for p in os.listdir('./pic/'+f):
                face = Img.open('./pic/' + f+'/'+p)
                face = face.convert('1')
                face_w = face.size[0]
                face_h = face.size[1]
                for code_ in range(5):
                    if face_w >= back_w | face_h >= back_h:
                        face_w = face_w//2
                        face_h = face_h//2
                    if face_w < back_w//3 and face_h < back_h//3:
                        face_w = 2*face_w
                        face_h = 2*face_h

                box = ((back_w-face_w)//2,(back_h-face_h)//2)  #计算图片放到中间的坐标
                cop = img2
                cop.paste(face.resize((face_w, face_h), Img.ANTIALIAS),box)
                file_path='C:/Users/dori/Desktop/pic/face__%d.png'%indexx       #png前面的文件夹可以自己定义
                cop.save(file_path)
                indexx += 1
            imglist = []
            for k in os.listdir('C:/Users/dori/Desktop/pic'):
                co=imageio.imread('C:/Users/dori/Desktop/pic/'+k)
                imglist.append(co)

            out = 'C:/Users/dori/Desktop/pic/face_%d_' % i
            out= out+'%s' % output
            i+=1
            imageio.mimsave(out, imglist, 'GIF', duration=0.1)

        rmtree(file)
        rmtree('./pic')

def select():
    f_name=askopenfilenames()
    lbox=app.children['lbox']
    info ['path'] = f_name
    if info['path']:
        for name in f_name:
            lbox.insert(END, name.split('/')[-1])

app=make_app()
app.mainloop()