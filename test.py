from __future__ import division

import numpy as np
import re
import sys
import threading
import time
import pyautogui

from google_trans_new import google_translator

translator = google_translator()
translate_client = google_translator()

#global t_text

def text_translation(input_text):

    # Translates text input to Chinese
    #print(input_text) ------test------
    #translation_zh = translate_client.translate(input_text, 'zh-cn') #call translate_client.translate() funcion to translate
    translation_zh = translator.translate(input_text,lang_tgt='zh-cn')
    # Translates text input to English
    #translation_en = translate_client.translate(input_text, 'en')
    translation_en = translator.translate(input_text,lang_tgt='en')
    return (translation_zh, translation_en)

def gen_dic(orig_text,trans_text):
    dic = {}
    dic[orig_text] = trans_text
    return dic

'''def test_update_dict(dic,t_text):
    if t_text == "" or " "
        return False
    if t_text == dic.keys():
        return False
    return True'''

def main():
    while(True):
        pre_text = input("voice in: ")
        #pyautogui.press('enter', presses=1, interval=0.0)
        #t_test = pre_text
        a,b = text_translation(pre_text)
        if len(a)==0 or len(b)==0:
            continue
        dic = gen_dic(a,b)
        for key in dic.keys():
            print(key)
            print(dic[key])
    return ;

if __name__ == "__main__":
    main()
