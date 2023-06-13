# ip_changer
IP changer for electronics signs

## General info
It is used to speed up the production line. When devices have same IP address, it isn't possible to upgrade them, so using that script user can easily change IP address by one click. 
Script connects with devices by SFTP, dowloading configuration file, updating him and uploding updated one, while saving the history to txt file. Additionally there is several options for admin such as read IP or assign IP out of range, which is impossible for the user. 

![image](https://github.com/mbiedrzycki/ip_changer/assets/106558286/3a11031a-5ebe-405d-b604-9dde88046b41)

## Technologies
Python 3.9+ with external libraries paramiko, elementpath and tkinter

## Launch
Download project folder and run with python 3.9+ interpreter. 

