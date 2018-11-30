def get_icon_save(path):
    from win32com.shell.shell import SHGetFileInfo
    from win32ui import CreateDCFromHandle, CreateBitmap
    from win32gui import GetDC,DestroyIcon
    from os.path import basename, splitext, dirname, realpath
    from PIL import Image
    
    ret, info = SHGetFileInfo(path, 0, 0x000001000 | 0x00001 | 0x000000100 | 0x000000010)
    hIcon, iIcon, dwAttr, name, typeName = info
    hdc = CreateDCFromHandle(GetDC(0))
    hbmp = CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 32, 32)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), hIcon)
    DestroyIcon(hIcon)
    pth = dirname(realpath(__file__)) + "/ico/" + splitext(path)[1][1:] + ".bmp"
    bmpinfo = hbmp.GetInfo()
    
    Image.frombuffer(
        "RGBA",
        (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
        hbmp.GetBitmapBits(True), "raw", "BGRA", 0, 1
    ).resize((16, 16)).save(pth)
    print("iconsaved", pth)
    return pth



# get_icon_save("D:/Source/Python/explorer/test3.ahk")