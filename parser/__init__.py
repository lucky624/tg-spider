#!/usr/bin/python3
import os
import pyautogui
import Xlib.display
from time import sleep
from selenium import webdriver
from pyvirtualdisplay import Display


def download(url):
    v_display = Display(visible=0, size=(1600, 900))
    v_display.start()

    pyautogui._pyautogui_x11._display = Xlib.display.Display(
        os.environ['DISPLAY'])

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1600x900')
    options.add_argument('download.default_directory=~/Downloads, download.prompt_for_download=False')

    driver = webdriver.Chrome("/home/lucky/tools/chromedriver_linux64/chromedriver", chrome_options=options)
    driver.set_window_size(1600, 900)

    driver.get(url)

    sleep(5)

    pyautogui.hotkey('ctrl', 's')
    sleep(1)
    pyautogui.press('enter')
    sleep(1)
    pyautogui.hotkey('enter')

    sleep(5)

    driver.close()
    v_display.stop()

