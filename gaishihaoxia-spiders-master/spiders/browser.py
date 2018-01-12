import sys, time
import webbrowser
import win32gui, win32ui, win32con, win32api


chromePath = 'C:\\my_system_tools\\Google\\Chrome\\Application\\chrome.exe'
sanliulingPath = 'C:\\Users\\49451\\AppData\\Roaming\\360se6\\Application\\360se.exe'
qqbrowser = "C:\\Program Files\\Tencent\\QQBrowser\\QQBrowser.exe"


webbrowser.register('360browser', None,  webbrowser.BackgroundBrowser(sanliulingPath))
webbrowser.register('chrome', None,  webbrowser.BackgroundBrowser(chromePath))
webbrowser.register('qqbrowser', None,  webbrowser.BackgroundBrowser(qqbrowser))



def window_capture(filename):
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)






if __name__ == "__main__":

	webbrowser.get('chrome').open('https://www.baidu.com')
	time.sleep(3)
	window_capture('C:\\Users\\49451\\Desktop\\chrome.jpg')
	print('chrome ok')

	webbrowser.get('360browser').open('https://www.baidu.com')
	time.sleep(6)
	print('360browser ok')
	window_capture('C:\\Users\\49451\\Desktop\\360browser.jpg')

	webbrowser.get('qqbrowser').open('https://www.baidu.com')
	print('qq ok')
	window_capture('C:\\Users\\49451\\Desktop\\qqbrowser.jpg')

	webbrowser.open('https://www.baidu.com')
	window_capture('C:\\Users\\49451\\Desktop\\ie.jpg')
	print('IE ok')
