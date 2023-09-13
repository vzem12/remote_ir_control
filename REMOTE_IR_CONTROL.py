import PySimpleGUI as sg
import os, sys
import time
import serial
import serial.tools.list_ports

CURRENT_MODE = 0x01
coms = []
comlist = serial.tools.list_ports.comports()
for com in comlist:
    coms.append(com.device)

SEND = b"\xf1"
MODE_CHANGE = b"\xf2"
MODE= ""

KEYS = {
    "ON": 0xBF48B7,
    "BACK": 0xBF40BF,
    "MENU": 0xBFE01F,
    "FILM": 0xBF1AE5,
    "UP": 0xBFD02F,
    "LEFT": 0xBF926D,
    "RIGHT": 0xBF52AD,
    "DOWN": 0xBFF00F,
    "OK": 0xBFB04F,
    "BACKWARD": 0xBF5AA5,
    "FORWARD": 0xBF708F,
    "PLAY": 0xBF20DF,
    "VOL+": 0xBF04FB,
    "VOL-": 0xBF847B,
    "MUTE": 0xBF44BB,
    "CH+": 0xBF18E7,
    "CH-": 0xBF38C7,
    "PREV": 0xBF06F9,
    "1": 0xBFA857,
    "2": 0xBF6897,
    "3": 0xBFE817,
    "4": 0xBF9867,
    "5": 0xBF58A7,
    "6": 0xBFD827,
    "7": 0xBFB847,
    "8": 0xBF7887,
    "9": 0xBFF807,
    "0": 0xBF827D,
}

layout = [
    [
    sg.Text("COM порт: ", size=(10, 1)),
    sg.Combo(values=coms,size=(10, 1), key="COMSET"),
    sg.Button("ОТКРЫТЬ", size=(10, 1), key="OPENCOM"),
    ],
    [
    sg.Text('_'*40, size=(35, 1))
    ],
    [
    sg.Button("ON/OFF", size=(10, 1), key="ON"),
    ],
    [
    sg.Button("НАЗАД", size=(10, 1), key="BACK"),
    sg.Button("МЕНЮ", size=(10, 1), key="MENU"),
    sg.Button("КИНО", size=(10, 1), key="FILM")
    ],
    [
    sg.Text(' ', size=(11, 1))
    ],
    [
    sg.Text(' ', size=(11, 1)),
    sg.Button("^", size=(10, 1), key="UP")
    ],
    [
    sg.Button("<", size=(10, 1), key="LEFT"),
    sg.Button("OK", size=(10, 1), key="OK"),
    sg.Button(">", size=(10, 1), key="RIGHT")
    ],
    [
    sg.Text(' ', size=(11, 1)),
    sg.Button("v", size=(10, 1), key="DOWN")
    ],
    [
    sg.Text(' ', size=(11, 1))
    ],
    [
    sg.Button("<<", size=(10, 1), key="BACKWARD"),
    sg.Button("PLAY", size=(10, 1), key="PLAY"),
    sg.Button(">>", size=(10, 1), key="FORWARD")
    ],
    [
    sg.Button("VOL+", size=(10, 1), key="VOL+"),
    sg.Button("MUTE", size=(10, 1), key="MUTE"),
    sg.Button("CH+", size=(10, 1), key="CH+")
    ],
    [
    sg.Button("VOL-", size=(10, 1), key="VOL-"),
    sg.Button("---", size=(10, 1), key="PREV"),
    sg.Button("CH-", size=(10, 1), key="CH-")
    ],
    [
    sg.Text(' ', size=(11, 1))
    ],
    [
    sg.Button("1", size=(10, 1), key="1"),
    sg.Button("2", size=(10, 1), key="2"),
    sg.Button("3", size=(10, 1), key="3")
    ],
    [
    sg.Button("4", size=(10, 1), key="4"),
    sg.Button("5", size=(10, 1), key="5"),
    sg.Button("6", size=(10, 1), key="6")
    ],
    [
    sg.Button("7", size=(10, 1), key="7"),
    sg.Button("8", size=(10, 1), key="8"),
    sg.Button("9", size=(10, 1), key="9")
    ],
    [
    sg.Text(' ', size=(11, 1)),
    sg.Button("0", size=(10, 1), key="0"),
    sg.Text(' ', size=(11, 1)),
    ],
    [
    sg.Text('_'*40, size=(35, 1))
    ],
    [
    sg.Button("Считать", size=(10, 1), key="READ"),
    sg.InputText(size=(15, 1), key="INCODE"),
    ],
    [
    sg.Button("Отправить", size=(10, 1), key="SEND"),
    sg.InputText(size=(15, 1), key="OUTCODE"),
    ],
]

# sg.ChangeLookAndFeel('Dark')
if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation') # Arbitrary string
window = sg.Window('IR_REMOTE', layout, icon='icon.ico')

while True:  # The Event Loop
        event, values = window.read()
        print(event)
        if event in (None, 'Exit', 'Cancel'):
            break
        elif event == "OPENCOM":
            COM = values["COMSET"]
            CONTROL = serial.Serial(COM, 9600, bytesize=8, parity="N", stopbits=1, timeout=1)
        elif event == "SEND":
            try:
                CODE = bytes.fromhex(values["OUTCODE"])
                LEN = bytes([len(CODE)])
                CONTROL.write(SEND+LEN+CODE)
            except NameError:
                pass
        elif event == "READ":
            try:
                CONTROL.write(MODE_CHANGE)
                time.sleep(0.2)
                CODE = CONTROL.readline().decode('utf-8').strip()
                window["INCODE"].update(CODE)
                CONTROL.write(MODE_CHANGE)
            except NameError:
                pass
        else:
            try:
                CODE = bytes.fromhex(hex(KEYS[event])[2:])
                LEN = bytes([len(CODE)])
                CONTROL.write(SEND+LEN+CODE)
            except NameError:
                pass