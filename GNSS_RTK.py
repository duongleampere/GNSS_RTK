import serial
from math import cos, sin, sqrt, pi
from tkinter import *
import statistics 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import numpy as np
import time

from datetime import date

def initial():

	global R,a,b,x_base,y_base,z_base,latitude_base,longitude_base,dis_list,x_values,y_values,mean,stdev,theta_list

    R = 6371000
    a = 6378137.0
    b = 6356752.3142
    index = 0
    order = 0

    x_base = -1796509.3072
    y_base = 6003425.8748
    z_base = 1184322.8353

    latitude_base = 10.85239217
    longitude_base = 106.65675883

    dis_list = []
    x_values = []
    y_values = []
    mean = []
    stdev = []
    theta_list = []

# port = 'COM8'
# baud = 115200

def serial_program():

	global ser

    port = 'COM8'
    baud = 115200
	ser = serial.Serial(port, baud, timeout=1)

	if ser.isOpen():
		print(ser.name + ' is_open...')

def mode_program():

    global f, ax, fig, path, txt, name

    today = date.today()
    d1 = today.strftime("%d_%m_%Y")
    parent_dir = ""

    os.system('cls')
    print("Please make sure you change the position of base already")
    mode = input("Graph?(y/n): ")
    txt = input("file.txt?(y/n): ")

    if txt == 'y':
	    name = input("enter file's name: ")

    path = os.path.join(parent_dir, str(d1))
    print(os.path.isdir(path))
    if not os.path.isdir(path):
	    os.mkdir(path)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if mode == 'y':
	    fig.show()
    else:
	    pass

    if txt == 'y':
	    path = os.path.join(path, name)
	    if not os.path.isdir(path):
		    os.mkdir(path)

    if txt == 'y':
	    f = open(path + '\\' + name + '.txt', "w")


def main():
	
   initial()
   serial_program()
   mode_program()

   order = 0
   while True:
    order += 1
    try:
    	out = ser.readlines(3)[0].decode('UTF-8')
    except:
    	print("Error frame has stopped the programme and there are %s samples saved."%order)
	# if out[1:6] == 'GNGGA' and out[3] in 'NS' and out[5] in 'EW':
    if out[1:6] == 'GNGGA':

	    out = out.split(',')

	    lat_str = out[2]
	    log_str = out[4]
	    alt = out[9]
	    altUnit = out[11]

	    latitude = round(float(lat_str[0:2]) + float(lat_str[2:])/60, 8)
	    longitude = round(float(log_str[0:3]) + float(log_str[3:])/60, 8)	
	    altitude = float(alt) + float(altUnit)

	    N = a**2/sqrt(a**2*cos(latitude*pi/180)**2 + b**2*sin(latitude*pi/180)**2)

	    x = (N + altitude) * cos(latitude*pi/180) * cos(longitude*pi/180)
	    y = (N + altitude) * cos(latitude*pi/180) * sin(longitude*pi/180)
	    z = ((b**2 /a**2)*N + altitude)*float(sin(latitude*pi/180))

	    x_values.append(x - x_base)
	    y_values.append(y -  y_base)
 	 
	    dis = sqrt((x-x_base)**2 + (y-y_base)**2 + (z-z_base)**2)
	    dis_list.append(dis)

	    os.system('cls')

	    if txt == 'y':
		    f.write("\nSample %s"%order)
		    f.write('\nLatitude: %s'%latitude)
		    f.write('\nLongitude: %s'%longitude)
		    f.write('\nAtitude: %s'%altitude)

		    f.write('\nECEF-x: %s'%x)
		    f.write('\nECEF-y: %s'%y)
		    f.write('\nECEF-z: %s'%z)

	    print('Latitude: ', latitude)
	    print('Longitude: ', longitude)
	    print('Atitude: ', altitude)
		
	    print('\nECEF-x: ', x)
	    print('ECEF-y: ', y)
	    print('ECEF-z: ', z)

	    if len(dis_list) > 1:
		    print('\nDistance: ', dis)
		    print('Mean (%d samples): %f'%(len(dis_list), statistics.mean(dis_list)))
		    print('Standard Deviation (%d samples): %f'%(len(dis_list),statistics.stdev(dis_list)))

		    if txt == 'y':
			    f.write('\nDistance: %s'%dis)
			    f.write('\nMean (%d samples): %f'%(len(dis_list), statistics.mean(dis_list)))
			    f.write('\nStandard Deviation (%d samples): %f'%(len(dis_list),statistics.stdev(dis_list)))

		    mean.append(statistics.mean(dis_list))
		    stdev.append(statistics.stdev(dis_list))

	    ax.plot(list(range(len(dis_list))), dis_list, color='b', label='Distance', picker=True)
	    ax.plot(list(range(len(mean))), mean, color='r', label='Mean', picker=True)
	    ax.plot(list(range(len(stdev))), stdev, color='c', label='Standard Deviation', picker=True)

	    if len(dis_list) == 1:
			# plt.xlabel('Samples')
		    ax.set_xlabel("Samples")
		    ax.set_ylabel("m")
		    ax.legend()
		    ax.grid()
	
	    fig.canvas.draw()
	    fig.canvas.flush_events()

	    if txt == 'y':
		    fig.savefig(path + '\\' + name +'.png')
		    fig.savefig(path + '\\' + name + '.pdf')

if __name__ == '__main__':
    # try:
    main()
    # except rospy.ROSInterruptException:
        # pass
