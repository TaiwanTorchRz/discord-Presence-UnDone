from pypresence import Presence
# from selenium import webdriver
import time,os,yaml,threading,warnings,sys
# import psutil
import speedtest
# from selenium import webdriver
##################################################################################
# cpu_per = round(psutil.cpu_percent(),1) # Get CPU Usage
# mem = psutil.virtual_memory()
# mem_per = round(psutil.virtual_memory().percent,1)
##################################################################################
defauld_config = {'debug': True, 'client_id': '\'<client_id>\'', 'update_timer': 5, 'large_image': {'text': '\'test\'', 'Enable': True}, 'large_text': {'text': '\'test\'', 'Enable': True}, 'small_image': {'text': '\'test\'', 'Enable': True}, 'small_text': {'text': '\'test\'', 'Enable': False}, 'state': {'text': '\'test\'', 'Enable': True}, 'details': {'text': '\'test\'', 'Enable': True}, 'name': '<大標題是DC應用程式名稱>'}
global RPC,config_list,command,large_image,large_text,small_text,details,state,update_timer,config_list
global PING,DOWNLOAD,UPLOAD
DOWNLOAD=None
UPDATE = True
SPEED=False
def speedtestfun():

    global PING,DOWNLOAD,UPLOAD,SPEED
    while SPEED!=-1:
        time.sleep(1)
        if SPEED:
            print('[系統消息] 正在測試網路速度...')
            s = speedtest.Speedtest()
            print('[系統消息] 正在尋找最佳測速伺服器...')
            s.get_best_server()
            print('[系統消息] 正在測試下載速度...')
            s.download()
            print('[系統消息] 正在測試上傳速度...')
            s.upload()
            results_dict = s.results.dict()
            PING=int(results_dict['ping'])
            DOWNLOAD=int(results_dict['download']/1000000)
            UPLOAD=int(results_dict['upload']/1000000)
            if config_list['debug']==True:
                print("[偵錯訊息]\n "+str(results_dict))    
            print('PING: '+str(results_dict['ping'])+"ms\n下載速度: "+str(int(results_dict['download']/1000000))+" Mbps\n上傳速度: "+str(int(results_dict['upload']/1000000))+" Mbps")
            print('[系統消息] 測試完畢')
            if SPEED>=0:
                SPEED=False
            if config_list['debug']==True:print(SPEED)
    SPEED=-2

_speedtest = threading.Thread(target=speedtestfun)
_speedtest.setName('Thread-speedtest')
_speedtest.start()
def reload():
    global RPC,config_list,command,large_image,large_text,small_text,details,state,UPDATE,update_timer,SPEED,defauld_config
    UPDATE = True
    print('[系統消息] 讀取設定檔案')
    try:
        with open('.\setting\config.yml',encoding="utf-8",mode="r") as file:
            config_list = yaml.full_load(file)
            print('[系統消息] 成功讀取設定檔案，client_id= '+str(config_list['client_id']))
            if config_list['debug']==True: print('[偵錯訊息] \r'+str(config_list))
    except:
        pass
        print('[系統警告] 找不到設定檔案，正在建立')
        with open('.\setting\config.yml', 'w',) as f:
            yaml.dump(defauld_config, f, default_flow_style=False)
        reload()
        return
    try:
        if config_list['debug']==True:
            print("[偵錯訊息] 開啟除錯模式") 
        update_timer = int(config_list['update_timer'])
        if config_list['debug']==True:print("[偵錯訊息] large_image="+str(config_list['large_image']['text'])+" 字串長度為"+str(len(str(config_list['large_image']['text']))))
        if len(str(config_list['large_image']['text']))<2 and config_list['large_image']['Enable']==True: 
            print('[系統警告] large_image 至少要2字元，少於2字元故不顯示')
            config_list['large_image']['text']="  "
        
        if config_list['debug']==True:print("[偵錯訊息] small_image="+str(config_list['small_image']['text'])+" 字串長度為"+str(len(str(config_list['small_image']['text']))))    
        if len(str(config_list['small_image']['text']))<2 and config_list['small_image']['Enable']==True:
            print('[系統警告] small_image 至少要2字元，少於2字元故不顯示')
            config_list['small_image']['text']="  "
        
        if config_list['debug']==True:print("[偵錯訊息] large_text="+str(config_list['large_text']['text'])+" 字串長度為"+str(len(str(config_list['large_text']['text']))))    
        if len(str(config_list['large_text']['text']))<2 and config_list['large_text']['Enable'] == True:
            print('[系統警告] large_text 至少要2字元，少於2字元故不顯示')
            config_list['large_text']['text']="  "
        
        if config_list['debug']==True:print("[偵錯訊息] small_text="+str(config_list['small_text']['text'])+" 字串長度為"+str(len(str(config_list['small_text']['text']))))    
        if len(str(config_list['small_text']['text']))<2 and config_list['small_text']['Enable']==True:
            print('[系統警告] small_text 至少要2字元，少於2字元故不顯示')
            config_list['small_text']['text']="  "
    except:
        print('[系統警告] 讀取檔案錯誤，正在重新建立檔案')
        with open('.\setting\config.yml', 'w',) as f:
            yaml.dump(defauld_config, f, default_flow_style=False)
        reload()
        return
    
    try: 
        RPC = Presence(client_id=int(config_list['client_id']))
    except:
        RPC_dect = True
        while RPC_dect:
            print('[系統警告] client id 設定錯誤，輸入reload重新讀取')
            temp = str(input()).lower()
            if temp == 'reload':
                RPC_dect = False
                reload()
            time.sleep(1)
    try:
        print('[系統消息] 與Discord伺服器連線中...')
        RPC.connect()
        print('[系統消息] 連線成功')
        # if config_list['AutoChangeNameSetting']['Enable']:
        #     if DOWNLOAD == None:
        #         print('[系統消息] 啟用自動更改(DC應用程式)名稱，先進行網路測速')
        #         SPEED = True
        # print('已就緒，請輸入help或?來取得幫助')
        print('\n[系統消息] 初始化完畢')
    except Exception as e:
        print('[系統消息] 連線失敗')
reload()

def update():
    global RPC,config_list,UPDATE,update_timer
    warnings.simplefilter('ignore', RuntimeWarning)
    while UPDATE:
        # print('狀態更stop新')
        time.sleep(update_timer)
        try:
            RPC.update(large_image=str(config_list['large_image']['text']) if config_list['large_image']['Enable'] else '  ', large_text=str(config_list['large_text']['text']) if config_list['large_text']['Enable'] else '  ',small_image=str(config_list['small_image']['text'] if config_list['small_image']['Enable'] else '  '), small_text=str(config_list['small_text']['text'] if config_list['small_text']['Enable'] else '  '),details=str(config_list['details']['text'] if config_list['details']['Enable'] else '  '), state=str(config_list['state']['text'] if config_list['state']['Enable'] else '  '))
            if config_list['debug']==True:
                print("[偵錯訊息] 更新狀態，接受指令輸入") 
                print("[偵錯訊息] UPDATE="+str(UPDATE)+" update_timer="+str(update_timer))
        except:
            # print('更新資料時出現錯誤，10秒後嘗試reload')
            # time.sleep(10)
            # reload()
            if config_list['debug']==True:
                if UPDATE == True :print("[偵錯訊息] 更新遇到錯誤") 
                print("[偵錯訊息] UPDATE="+str(UPDATE)+" update_timer="+str(update_timer))
            
    UPDATE=-1
    return None
        
_update = threading.Thread(target = update)
_update.setName('Thread-Update')

_update.start()
if config_list['debug']==True:
        print("[偵錯訊息] 開始更新") 

# def changename(name):
#     _path = '.\setting\msedgedriver.exe' # webdriver的位置
#     driver = webdriver.Edge(_path)
#     driver.get("https://discord.com/login?redirect_to=%2Fdevelopers") #前往這個網址
# if config_list['AutoChangeNameSetting']['Enable'] == False:
    # _speedtest.start()

while 1:
    try: 
        temp=str(input()).lower()
        if temp == "reload":
            RPC.clear()
            RPC.close()
            reload()
            print('[系統消息] 更新完畢，Discord需要幾秒鐘來更新')
        # temp=str(input()).lower()
        elif temp =="stop":
            UPDATE=False
            SPEED=-1
            print('[系統消息] 正在等待所有線程結束..請稍後')
            RPC.clear()
            RPC.close()
            _update.join()     
            # print('正在回收資源..請稍後')
            # quit(0) 
            while UPDATE!=-1:
                print('[系統消息] 等待結束更新線程')
                time.sleep(1)
            while SPEED!=-2:
                print('[系統消息] 等待結束測速線程')
                time.sleep(1)
            sys.exit()
            # raise SystemExit
        elif temp=="speed":
            if SPEED:
                print("[系統警告] 已經在測速了")
                break
            SPEED = True
            speedtestfun()
        # temp=str(input()).lower()
        elif temp.split(' ')[0]=="rename":
            if config_list['AutoChangeNameSetting']['Enable']==False:print("[系統消息] 由於您關閉自動更新，需要手動到Discord Develop網站更新")
            else:print(temp.split(' ')[1])
        elif temp == "help" or temp == "?":
            print("---\n指令幫助:\nreload: 重新讀取設定檔案\nstop:關閉程式\nspeed:顯示網速\nhelp:取得幫助\nv0.2(Beta)\n---")
        else:
            print('[系統消息] 未知的指令.請輸入help或?來取得幫助')
    except SystemExit:
        break
    except Exception as e:
       if config_list['debug']==True:print(e)
    