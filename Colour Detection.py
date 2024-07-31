from tkinter import *
import sqlite3
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import pandas as pd
import imutils

r = g = b = xpos = ypos = 0

window=Tk()
window.geometry("650x400")
window.title("Color Detection")

def image():
	

	def open_file():

		filepath = askopenfilename(initialdir="/", title="Select an image", filetypes=(("jpeg","*.jpeg"),("jpg","*.jpg")))
		img = cv2.imread(filepath)


		#Reading csv file with pandas and giving names to each column
		index=["color","color_name","hex","R","G","B"]
		csv = pd.read_csv('colors.csv', names=index, header=None)

		#function to calculate minimum distance from all colors and get the most matching color
		def getColorName(R,G,B):
			minimum = 10000
			for i in range(len(csv)):
				d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
				if(d<=minimum):
					minimum = d
					cname = csv.loc[i,"color_name"]
			return cname


		#function to get x,y coordinates of mouse double click
		def draw_function(event, x,y,flags,param):
			global b,g,r,xpos,ypos
			xpos = x
			ypos = y
			b,g,r = img[y,x]
			b = int(b)
			g = int(g)
			r = int(r)


		cv2.namedWindow('image')
		root.destroy()
		cv2.setMouseCallback('image',draw_function)

		while(1):


			cv2.imshow("image",img)
			
			#cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
			cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

			#Creating text string to display( Color name and RGB values )
			text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)

			#cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
			cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

			#For very light colours we will display text in black colour
			if(r+g+b>=600):
				cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

			#Break the loop when user hits 'esc' key
			if cv2.waitKey(20) & 0xFF ==27:
				break

		
		cv2.destroyAllWindows()



	window.destroy()
	root = Tk() 
	#root.geometry('200x100') 
 
	root.title("Color Detection")
	root.minsize(640, 400)


	btn = Button(root, text ='Open', command = open_file)
	btn.pack(side = TOP, pady = 10)

	mainloop()




# Real time color detection
def livevideo():

	#if default camera then 0 else try 1,2,3.... if u have placed external device(camera)
	camera = cv2.VideoCapture(0)

	index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
	df = pd.read_csv('colors.csv', names = index, header = None)


	def getColorName(R,G,B):
		minimum = 10000
		for i in range(len(df)):
			d = abs(R - int(df.loc[i,"R"])) + abs(G - int(df.loc[i,"G"])) + abs(B - int(df.loc[i,"B"]))
			if (d <= minimum):
				minimum = d
				cname = df.loc[i, 'color_name'] + '   Hex=' + df.loc[i, 'hex']
		return cname


	def identify_color(event, x, y, flags, param):
		global b, g, r, xpos, ypos
		xpos = x
		ypos = y
		b, g, r = frame[y,x]
		b = int(b)
		g = int(g)
		r = int(r)


	cv2.namedWindow('image')
	window.destroy()
	cv2.setMouseCallback('image', identify_color)

	while True:
		grabbed, frame= camera.read()
		frame = imutils.resize(frame, width=900)
		kernal = np.ones((5, 5), "uint8")
		cv2.rectangle(frame, (20,20), (800, 60),(b,g,r), -1)
		text = getColorName(b,g,r) + '   R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
		cv2.putText(frame,text, (50,50),2, 0.8, (255,255,255),2,cv2.LINE_AA)


		if(r+g+b >= 600):
			cv2.putText(frame,text,(50,50), 2, 0.8, (0,0,0),2,cv2.LINE_AA)

		cv2.imshow('image',frame)

		if cv2.waitKey(20) & 0xFF == 27:
			break

	camera.release()
	cv2.destroyAllWindows()


#Main loop
l1=Label(window,text="Detect colour from",font="times 20")
l1.grid(row=0,column=0,columnspan=10)

b1=Button(window,text="Image",width=20,command=image)
b1.grid(row=10,column=10)

b2=Button(window,text="Live video",width=20,command=livevideo)
b2.grid(row=30,column=10)


window.mainloop()