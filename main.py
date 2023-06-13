import tkinter
from tkinter import messagebox
import xml.etree.ElementTree as ET
import os
import subprocess
import time
from datetime import datetime
import paramiko


def sftp_connect_dowload(x):
    host = x
    port = 22
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username="root", password="")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get('/mnt/application/backend/22218f48-5850-4864-bd2f-03ef71248244/Config/HardwareManager/HardwareManager.xml', localpath='E:\\HardwareManager.xml')
    except:
        messagebox.showerror("Error", "Error! Nie można nawiązać połączenia.")


def sftp_connect_upload(x):
    host = x
    port = 22
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username="root", password="")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('E:\\HardwareManager.xml', remotepath='/mnt/application/backend/22218f48-5850-4864-bd2f-03ef71248244/Config/HardwareManager/HardwareManager.xml')
    except:
        messagebox.showerror("Error", "Error! Nie można nawiązać połączenia.")

def save_history(ip):
    date = datetime.now()
    date_formated = date.strftime("%d.%m.%Y %H:%M")
    read_mac = "arp -a " +str(ip)
    mac_output = subprocess.getoutput(read_mac)
    mac_list = mac_output.split()
    f=open("history.txt", 'a')
    device_info = str(date_formated +" | "+ mac_list[10] +" | "+ ip)
    f.write(device_info)
    f.write("\n")
    f.close()


def actualIp():
    file_exist = os.path.isfile('E:\\HardwareManager.xml')
    if file_exist == True:
        os.remove('E:\\HardwareManager.xml')
    for y in range(201,221):
        global ip_3
        ip_3 = y
        template = "192.168.0."
        global full_ip
        full_ip = str(template) + str(ip_3)
        full_ip_information = "Aktualne IP: " + str(full_ip)
        command_ping = ("ping -n 1 "+str(template) + str(y))
        ping_output = subprocess.getoutput(command_ping)
        ping_list = ping_output.split()
        if 'TTL=64' in ping_list:
            messagebox.showinfo("Actual IP", full_ip_information)
            break




def rand_ip():
    ping_201_output = subprocess.getoutput("ping 192.168.0.201")
    ping_201_list = ping_201_output.split()
    if 'TTL=64' in ping_201_list:
        file_exist = os.path.isfile('E:\\HardwareManager.xml')
        if file_exist == True:
            os.remove('E:\\HardwareManager.xml')
        standart = "192.168.0.201"
        sftp_connect_dowload(standart)
        file = ET.parse('E:\\HardwareManager.xml')
        ipaddress = file.find('Settings/Setting/IPAddress')

        global count
        count = count + 1
        if count > 220:
            count = 203

        template = "192.168.0."
        full_ip = str(template)+str(count)
        ipaddress.text= full_ip
        file.write('E:\\HardwareManager.xml')

        sftp_connect_upload(standart)
        os.system("plink root@192.168.0.201 -batch -pw 'password' reboot")
        time.sleep(45)
        os.system("plink root@192.168.0.201 -batch -pw 'password' reboot")
        time.sleep(15)
        ping = "ping -n 1 " + str(full_ip)
        os.system(ping)
        ping_full_ip_output = subprocess.getoutput(ping)
        ping_full_ip_list = ping_full_ip_output.split()
        if 'TTL=64' in ping_full_ip_list:
            messagebox.showinfo("New IP assigned", "Przydzielono nowe IP: " + str(full_ip) + " [Skopiowano]")
            save_history(full_ip)
            echo = "echo " + full_ip +" | clip"
            os.system (echo)
        else:
            messagebox.showerror("PING", "Error! Nie można spingować znaku.")
    else:
        messagebox.showerror("The sign can't be pinged", "Nie można spignować znaku! [192.168.0.201]")


def reset():
    actualIp()
    if full_ip == "192.168.0.201":
        actual_ip= ("Aktuane IP: " + full_ip)
        messagebox.showinfo("Actual IP", actual_ip)
    else:
        file_exist = os.path.isfile('E:\\HardwareManager.xml')
        if file_exist == True:
            os.remove('E:\\HardwareManager.xml')
        sftp_connect_dowload(full_ip)
        file = ET.parse('E:\\HardwareManager.xml')
        ipaddress = file.find('Settings/Setting/IPAddress')
        ipaddress.text = "192.168.0.201"
        file.write('E:\\HardwareManager.xml')
        sftp_connect_upload(full_ip)
        reboot = "plink root@192.168.0." +str(ip_3) + str(" -batch -pw 'password' reboot")
        os.system(reboot)
        time.sleep(45)
        os.system(reboot)
        time.sleep(15)
        ping_201_output = subprocess.getoutput("ping -n 1 192.168.0.201")
        ping_201_list = ping_201_output.split()
        if 'TTL=64' in ping_201_list:
            messagebox.showinfo("IP Backup", "Przywrócono IP: 192.168.0.201")
        else:
            messagebox.showerror("IP Backup", "Error! Nie przywrócono IP.")


def manually_ip():
    psw_window = tkinter.Toplevel(root)
    psw_window.geometry("290x80")
    root.eval(f'tk::PlaceWindow {str(psw_window)} center')
    pswd = tkinter.Label(psw_window, text = "Wprowadź hasło.")
    pswd.pack()
    input_psw = tkinter.Entry(psw_window, font=("Cagliari", 12))
    input_psw.config(show="*")
    input_psw.pack(padx = 10, side="left")

    def cps():
        password = input_psw.get()
        if password == "example": #ppassword for admin function
            psw_window.destroy()
            ip = input_ip.get()
            if len(ip) == 13:
                file_exist = os.path.isfile('E:\\HardwareManager.xml')
                if file_exist == True:
                    os.remove('E:\\HardwareManager.xml')
                standart = "192.168.0.201"
                sftp_connect_dowload(standart)
                file = ET.parse('E:\\HardwareManager.xml')
                ipaddress = file.find('Settings/Setting/IPAddress')
                ipaddress.text = ip
                file.write('E:\\HardwareManager.xml')
                sftp_connect_upload(standart)
                os.system("plink root@192.168.0.201 -batch -pw 'password' reboot")
                time.sleep(45)
                os.system("plink root@192.168.0.201 -batch -pw 'password' reboot")
                time.sleep(15)
                command_ping = ("ping -n 1 " + str(ip))
                ping_read_ip_output = subprocess.getoutput(command_ping)
                ping_read_ip_list = ping_read_ip_output.split()
                if 'TTL=64' in ping_read_ip_list:
                    messagebox.showinfo("New IP assigned", "Przydzielono nowe IP: " + str(ip) + " [Skopiowano]")
                else:
                    messagebox.showerror("PING", "Error! Nie można spingować znaku.")
            else:
                messagebox.showwarning("Incorrect IP format", "Nieprawidłowy format IP")
        else:
            messagebox.showerror("Password incorrect", "Hasło niepoprawne.")
    check_psw = tkinter.Button(psw_window, height=2, width=10, text="Zaloguj.", command=cps).pack(padx=10, side="right")


def instruction():
     instruction_window = tkinter.Toplevel(root)
     instruction_window.geometry("1000x400")
     instruction_window.configure(bg="white")


     def labels(text_of_label):
         name_of_label = tkinter.Label(instruction_window, text=text_of_label)
         name_of_label.config(font=("Cagliari", 12))
         name_of_label.configure(bg="white")
         name_of_label.pack()


     instructionText =  "INSTRUKCJA"
     instructionText2 = "1. Podłącz zasilanie oraz kabel ethernet i poczekaj, aż znak się uruchomi."
     instructionText3 = "2. Kliknij 'Przydziel losowe IP' i poczekaj do momentu wyświetlenia na ekranie komunikatu, który poinformuje o pozytywnej zmianie adresu IP."
     instructionText4 = "3. Połącz się z iCenter za pomocą nowegu adresu IP znaku."
     instructionText5 = "4. Podłącz kolejny znak, powtórz podpunkty 1 oraz 2 i połącz się z iCenter za pomocą nowego adresu IP."
     instructionText6 = "INFO - Staraj się nie wyłączać oprogramowania do momentu zakończenia zlecenia. " +"\n" + "Jeśli zapomnisz, bądź nie zapiszesz nowo ustawionego adresu IP, można je odczytać z pliku history.txt."
     instructionText7 = " "
     instructionText8 = "W przypadku problemów wezwij lidera."

     labels(instructionText)
     labels(instructionText7)
     labels(instructionText2)
     labels(instructionText3)
     labels(instructionText4)
     labels(instructionText5)
     labels(instructionText7)
     labels(instructionText6)
     labels(instructionText7)
     labels(instructionText8)

count = 203
count2 = 201
root = tkinter.Tk()
root.title("Ethernet signs - IP Changer")
root.geometry("520x300")
frame = tkinter.Frame(root)
inst = tkinter.Button(root, height=2, width=20, text="INSTRUKCJA", command=instruction).pack(pady=10)
read_ip_button = tkinter.Button(root, height=2, width=20, text="Odczytaj aktualne IP", command=actualIp).pack(pady=10)
change_ip_button = tkinter.Button(root, height=2, width=20, text="Przydziel losowe IP", command=rand_ip).pack(pady=10)
reset_ip_button = tkinter.Button(root, height=2, width=20, text="Przywróć 192.168.0.201", command=reset).pack(pady=10)
frame.pack()
input_ip=tkinter.Entry(frame,font=("Cagliari", 12))
input_ip.pack(padx = 10, side="left")
change_ip_urself = tkinter.Button(frame, height=2, width=20, padx = 10, text="Przydziel IP", command=manually_ip).pack(padx = 10, pady= 10, side="left")
root.mainloop()



