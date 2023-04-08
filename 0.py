import tkinter as tk
import win32api
import win32con
import win32gui
import keyboard
import time


#请安装
#pip install pywin32
#pip install keyboard
#带有蓄能的，使用祭礼的不能使用，除非你保证每次都连续释放。
#夜兰及类似情况的E无法使用，因为无法辨别哪一次E进入冷却。
#当然你也可以通过将预留“时间”加到冷却时间上的办法使用，但准确性无法保证。

#原始参数
cha_skill_cooldown = [20,18,6,8]#输入E技能冷却时间
cha_skillq_cooldown = [20,18,13.5,20]#输入Q技能冷却时间

time.sleep(0.5)
countdown = [0,0,0,0] # 创建一个全局变量来存储倒计时的秒数
create_all = [] #创建所有字符串/图片结合
character_flag = 0 #当前登场人物

# 创建一个窗口
window = tk.Tk()
window.title("genshinSkillCooldown")
window.geometry("400x960")

# 创建一个画布
canvas = tk.Canvas(window, width=640, height=960)
canvas.pack()
textE = canvas.create_text(100, 50, text="E", fill="red", font=("SimHei", 32), tags="texte")
textQ = canvas.create_text(300, 50, text="Q", fill="red", font=("SimHei", 32), tags="textq")
# 加载图片
image1 = tk.PhotoImage(file="image1.png")
image2 = tk.PhotoImage(file="image2.png")
image3 = tk.PhotoImage(file="image3.png")
image4 = tk.PhotoImage(file="image4.png")
image = [image1,image2,image3,image4]


class Pic:
    def __init__(self, name, image,  cha_skill_cooldown, lockkeyb = True):
        self.name = name
        self.image = image
        self.text_id = canvas.create_text(100, 100 + 200 * int(self.name) - 100, text="准备就绪", fill="red", font=("SimHei", 32), tags="text" + self.name)
        self.pic = None
        self.lockkeyb = lockkeyb
        self.lockkeyq = True
        self.cha_skill_cooldown = cha_skill_cooldown
        self.countdown = cha_skill_cooldown

    def create_etext(self, canvas):
        
        if self.lockkeyb:
            self.lockkeyb = False
            canvas.delete(self.text_id)
            self.text_id = None
            
            self.text_id = canvas.create_text(100, 100 + 200 * int(self.name) - 100, text=str(self.countdown) + "s", fill="red", font=("Arial", 36), tags="text" + self.name)
            self.update_countdown(canvas)
            
    def create_qpic(self, time, canvas):
        if self.lockkeyq:
            self.lockkeyq = False
            self.pic = canvas.create_image(200, 200 * int(self.name) - 100, anchor="nw", image=self.image)
            print(int(time*1000))
            canvas.after(int(time*1000), lambda: self.unlockq())
    
    def unlockq(self):
        canvas.delete(self.pic)
        self.lockkeyq = True
              
    def update_countdown(self, canvas):
        if self.countdown > 0:
            self.countdown -= 1
            canvas.itemconfig(self.text_id, text=str(self.countdown) + "s")
            canvas.after(1000, lambda: self.update_countdown(canvas))
        else:
            canvas.itemconfig(self.text_id, text="准备就绪", fill="red", font=("SimHei", 32)) # 修改文本内容和属性
            self.countdown = self.cha_skill_cooldown
            self.lockkeyb = True
            #canvas.delete(self.text_id)
            #self.text_id = None

def set_chara(e, chara):
    print(e)
    global character_flag
    chara -= 1
    character_flag = chara
    keyboard.press(str(chara+1))
    #create_all[chara].create_picandtext(chara, canvas)

def input_e(e, character_flag):

    print(e)
    keyboard.press("e") 
    create_all[character_flag].create_etext(canvas)


def input_q(e, character_flag):
    print(e)
    keyboard.press("q")
    create_all[character_flag].create_qpic(cha_skillq_cooldown[character_flag], canvas)
 
for i in range(4):
    create_all.append(Pic(str(i+1), image[i], cha_skill_cooldown[i]))

keyboard.on_press_key("1", lambda e: set_chara(e, 1))
keyboard.on_press_key("2", lambda e: set_chara(e, 2))
keyboard.on_press_key("3", lambda e: set_chara(e, 3))
keyboard.on_press_key("4", lambda e: set_chara(e, 4))

keyboard.on_press_key("e", lambda e: input_e(e, character_flag))
keyboard.on_press_key("q", lambda e: input_q(e, character_flag))

# 获取窗口句柄
hwnd = window.winfo_id()

# 设置窗口为置顶
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# 设置窗口为透明
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)

# 进入主循环
window.mainloop()