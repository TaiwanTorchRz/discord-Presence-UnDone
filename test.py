from pypresence import Presence
# from selenium import webdriver
import time,os,yaml,threading
# import psutil
import speedtest
##################################################################################
# cpu_per = round(psutil.cpu_percent(),1) # Get CPU Usage
# mem = psutil.virtual_memory()
# mem_per = round(psutil.virtual_memory().percent,1)
##################################################################################
global RPC,config_list,command,large_image,large_text,small_text,details,state
command = ""
def reload():
    global RPC,config_list,command,large_image,large_text,small_text,details,state

    with open('.\setting\config.yml',encoding="utf-8",mode="r") as file:
        config_list = yaml.full_load(file)
        print('成功讀取設定檔案，client_id= '+str(config_list['client_id']))
    
        # print('讀取設定檔案時出錯，正在建立新的')
    if config_list['debug']==True:
        print("開啟除錯模式") 
    RPC = Presence(client_id=int(config_list['client_id']))
    try:
        print('與Discord伺服器連線中...')
        RPC.connect()
        print('連線成功')
        # print('已就緒，請輸入help或?來取得幫助')
        print('讀取設定檔案中的文字')
        # if str(str(config_list['debug']).lower()=="true"):print("偵錯模式開啟\n"+str(e))
        print('正在測試網路速度...')
        s = speedtest.Speedtest()
        print('正在尋找最佳測速伺服器...')
        s.get_best_server()
        print('正在測試下載速度...')
        s.download()
        print('正在測試上傳速度...')
        s.upload()
        print('測試完畢')
        results_dict = s.results.dict()
        if config_list['debug']==True:
            print("[偵錯訊息]\n "+str(results_dict))    
        print('PING: '+str(results_dict['ping'])+"ms\n下載速度: "+str(int(results_dict['download']/1000000))+" Mbps\n上傳速度: "+str(int(results_dict['upload']/1000000))+" Mbps")
        print('初始化完畢')
    except Exception as e:
        print('連線失敗')
reload()
def update():
    global RPC,config_list
    while 1:
        time.sleep(0.5)
        RPC.update(large_image=str(config_list['large_image']['text']) if config_list['large_image']['Enable'] else None, large_text=str(config_list['large_text']['text']) if config_list['large_text']['Enable'] else None,small_image=str(config_list['small_image']['text'] if config_list['small_image']['Enable'] else None), small_text=str(config_list['small_text']['text'] if config_list['small_text']['Enable'] else None),details=str(config_list['details']['text'] if config_list['details']['Enable'] else None), state=str(config_list['state']['text'] if config_list['state']['Enable'] else None))
while 1:
    try: 
        # RPC.update(command)
        print('TEST')
        # RPC.update(large_image=str(config_list['large_image']['text']) if config_list['large_image']['Enable'] else None, large_text=str(config_list['large_text']['text']) if config_list['large_text']['Enable'] else None,small_image=str(config_list['small_image']['text'] if config_list['small_image']['Enable'] else None), small_text=str(config_list['small_text']['text'] if config_list['small_text']['Enable'] else None),details=str(config_list['details']['text'] if config_list['details']['Enable'] else None), state=str(config_list['state']['text'] if config_list['state']['Enable'] else None))
        # time.sleep(0.1)
        # if str(str(config_list['debug']).lower()=="true"):print("更新狀態")
        print('TEST2')
        temp=str(input()).lower()
        if temp == "reload":
            RPC.close()
            RPC.clear()
            reload()
        # temp=str(input()).lower()
        if temp =="stop":
            print('正在回收資源..請稍後')
            RPC.close()
            RPC.clear()
            # print('正在回收資源..請稍後')
            quit(0)
        # temp=str(input()).lower()
        if temp == "help":
            print("---\n指令幫助:\nreload: 重新讀取設定檔案\nstop:關閉程式\nhelp:取得幫助\nv0.1(Beta)\n---")
        else:
            print('未知的指令.請輸入help來取得幫助')
    except Exception as e:
       print(e)
       print('ERR')



