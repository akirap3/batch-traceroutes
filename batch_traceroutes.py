#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pprint, os, time
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from netmiko import ConnectHandler
import pandas as pd


# In[2]:


def get_Type_PortNumber_CommandList(host_ip, vrf, source_ip):
    commandList = []
    if host_ip == 'your_device_ip_X.X.X.X' or host_ip == 'your_device_ip_X.X.X.X':
        connect_type = 'cisco_ios_telnet'
        portNumber = 23
        for dstIP in content:
            command = 'traceroute ' + vrf + ' ' + dstIP + ' source ' + source_ip + ' timeout 1 ttl 1 25'
            commandList.append(command)
    else:
        connect_type = 'cisco_ios'
        portNumber = 22
        for dstIP in content:
            command = 'traceroute ' + vrf + ' ' + dstIP + ' source ' + source_ip + ' maxttl 25 timeout 1'
            commandList.append(command)      
    return [connect_type, portNumber, commandList]


# In[3]:


# create a window instance
window = Tk()
window.title("Choose the router you'd like to log in")
# window.geometry('350x200')

# this variable is for getting radius button value
selected = StringVar()

# design radius widgets
rt001_rad = Radiobutton(window,text='your_device_name', value="your_device_ip_X.X.X.X", variable=selected)
rt002_rad = Radiobutton(window,text='your_device_name', value="your_device_ip_X.X.X.X", variable=selected)
# rt003_rad = Radiobutton(window,text='your_device_name', value="your_device_ip_X.X.X.X", variable=selected)
# rt004_rad = Radiobutton(window,text='your_device_name', value="your_device_ip_X.X.X.X", variable=selected)
brt01_rad = Radiobutton(window,text='your_device_name', value="your_device_ip_X.X.X.X", variable=selected)
brt02_rad = Radiobutton(window,text='your_device_name', value="your_device_ip_X.X.X.X", variable=selected)

# design texts widgets
vrf_txt = Entry(window,width=15)
source_ip_txt = Entry(window, width=15)

# design lable widgets
vrf_lbl = Label(window)
source_ip_lbl = Label(window)
vrf_title_lbl = Label(window, text="Please enter vrf name: ")
source_ip_title_lbl = Label(window, text="Please enter source IP: ")
dest_ips_lbl = Label(window,text="Please select txt file contains Destination IPs")

# define the function for buttons
def rt_clicked():
    print('The ROUTER IP IS: ' + selected.get())
    
def vrf_clicked():
    print('THE VRF IS: ' + vrf_txt.get())
    vrf_lbl.configure(text = 'VRF IS: ' + vrf_txt.get())
       
def srIP_clicked():
    print('THE SOURCE IP IS: ' + source_ip_txt.get())
    source_ip_lbl.configure(text = 'Source IP is ' + source_ip_txt.get())
    
def dstIP_clicked():
    global file 
    file = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*")))
    print('FILE PATH IS: ' + file)
    dest_ips_lbl.configure(text = 'FILE PATH IS: ' + file)
    
def close_window(): 
    global vrf, source_ip, file_path
    vrf = vrf_txt.get()
    if vrf != '':
        vrf = "vrf " + vrf
    source_ip = source_ip_txt.get()
    file_path = file
    window.destroy()
    
# design buttons    
rt_btn = Button(window, text="Confirm RT", command=rt_clicked)
vrf_btn = Button(window, text="Confirm VRF", command=vrf_clicked)
source_ip_btn = Button(window, text="Confirm SrIP", command=srIP_clicked)
dest_ips_btn = Button(window, text="Confirm DstIP", command=dstIP_clicked)
close_btn = Button(window, text="All Confirmed", command=close_window)
    
# to place the widgets
# row 0
rt001_rad.grid(column=0, row=0, padx=5, pady=10)
rt002_rad.grid(column=1, row=0, padx=5, pady=10)
# rt003_rad.grid(column=2, row=0, padx=5, pady=10)
# rt004_rad.grid(column=3, row=0, padx=5, pady=10)
rt_btn.grid(column=4, row=0, padx=5, pady=10)
# row 1
brt01_rad.grid(column=0, row=1, padx=5, pady=10)
brt02_rad.grid(column=1, row=1, padx=5, pady=10)
# row 2
vrf_title_lbl.grid(column=0, row=2, padx=5, pady=10)
vrf_txt.grid(column=1, row=2, padx=5, pady=10)
vrf_lbl.grid(column=2, row=2, padx=5, pady=10)
vrf_btn.grid(column=4, row=2, padx=5, pady=10)
# row 3
source_ip_title_lbl.grid(column=0, row=3, padx=5, pady=10)
source_ip_txt.grid(column=1, row=3, padx=5, pady=10)
source_ip_lbl.grid(column=2, row=3, padx=5, pady=10)
source_ip_btn.grid(column=4, row=3 ,padx=5, pady=10)
# row 4
dest_ips_lbl.grid(column=0, row=4, padx=5, pady=10)
dest_ips_btn.grid(column=4, row=4, padx=5, pady=10)
# row 5
close_btn.grid(column=4, row=5, padx=5, pady=10)

# to run the window
window.mainloop()


# In[ ]:


# to get IPs for each line
with open(file_path,'r+') as f:
 content = f.readlines()
 content = [x.strip() for x in content]
    
# hint the number of destination IPs
print("THERE ARE " + str(len(content)) + " DESTINATION IPs.")

# get type, portNumber and create command lists
type_PortNumber_commandlist = get_Type_PortNumber_CommandList(selected.get(), vrf, source_ip)

# define router login parameters
router = {
    'device_type': type_PortNumber_commandlist[0],
    'host':   selected.get(),
    'username': 'your_username',
    'password': 'your_password',
    'port' : type_PortNumber_commandlist[1],        
    'secret': ''
}


# create connection with router
try:
    net_connect = ConnectHandler(**router)
    print("CONNECTION SUCCESS")
except Exception as e:
    print("THERE IS SOMETHING WRONG WITH THE CONNECTION !!!")
    print("CONNECTION CLOSED")
    net_connect.disconnect()
    print(e)



# Traceroute for each destination IPs
try:
    print("Processing............")
    outputList = []
    for command in type_PortNumber_commandlist[2]:
        output = net_connect.send_command(command)
        outputList.append(output)
        time.sleep(0.2)
    
    # Close the connection
    net_connect.disconnect()
    
    # Create a zipped list of tuples from above lists
    zippedList = list(zip(content, outputList))
    # Create dataframe and transform the data to csv file
    dfObj = pd.DataFrame(zippedList, columns = ['Dest IP' , 'Traceroute']) 
    dfObj.to_csv(os.getcwd()+"\\traceroutes_results.csv", escapechar='\\',index = False)
    print("Traceroutes have been completed, good job !!!")
    
except Exception as e:
    print("THERE IS SOMETHING WRONG WITH THE COMMANDS OR THE DATA YOU INPUT !!!")
    print("CONNECTION CLOSED")
    net_connect.disconnect()
    print(e)

