from pypresence import Presence
# from selenium import webdriver
import time,os,yaml,psutil
##################################################################################
cpu_per = round(psutil.cpu_percent(),1) # Get CPU Usage
mem = psutil.virtual_memory()
mem_per = round(psutil.virtual_memory().percent,1)
##################################################################################
global RPC,config_list,command
command = ""
def reload():
    global RPC,config_list,command
    try:
        with open(r'.\setting\config.yml',encoding="utf-8") as file:
            config_list = yaml.full_load(file)
            print('成功讀取設定檔案，client_id= '+str(config_list['client_id']))
    except:
        print('讀取設定檔案時出錯，正在建立新的')
    if str(str(config_list['debug']).lower()=="true"):print("開啟除錯模式") 
    RPC = Presence(client_id=int(config_list['client_id']))
    try:
        print('與Discord伺服器連線中...')
        RPC.connect()
        print('連線成功')
        print('已就緒，請輸入help或?來取得幫助')
        if str(str(config_list['debug']).lower()=="true"):print("\n"+str(e))
        if config_list['large_image']['Enable'] == True:
            command += str("large_image="+str(config_list['large_image']['text'])+",")
        if config_list['large_text']['Enable'] == True:
            command += str("large_text="+str(config_list['large_text']['text'])+",")
        if config_list['small_text']['Enable'] == True:
            command += str("small_text="+str(config_list['small_text']['text'])+",")
        if config_list['details']['Enable'] == True:
            command += str("details="+str(config_list['details']['text'])+",")
        if config_list['state']['Enable'] == True:
            command += str("state="+str(config_list['state']['text']))
            print(command)
            exit(0)
    except Exception as e:
        print('連線失敗')
        

    
reload()
    
while True:
    try:  
        RPC.update(command)
        time.sleep(0.1)
        # if str(str(config_list['debug']).lower()=="true"):print("更新狀態")
        temp=str(input()).lower()
        if temp =="reload":
            reload()
        elif temp =="stop":
            print('正在回收資源..請稍後')
            quit(0)
        elif temp == "help":
            print("---\n指令幫助:\nreload: 重新讀取設定檔案\nstop:關閉程式\nhelp:取得幫助\nv0.1(Beta)\n---")
        else:
            print('未知的指令.請輸入help來取得幫助')
    except Exception as e:
        print(e)

