
import tkinter as tk
from numpy import rint

import pytz
from googletrans import Translator
import pycountry
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
from PIL import Image
import datetime
import threading

class TranslatePrograme():
    def __init__(self, root_window):
        self.root = root_window
        s_width = self.root.winfo_screenwidth()
        s_height = self.root.winfo_screenheight()
        r_width = 600
        r_height = 500
        self.root.title('Translate Programe')
        self.root.geometry(f'{r_width}x{r_height}+{(s_width-r_width)//2}+{(s_height-r_height-100)//2}')
        self.root.resizable(0,0)

        self.all_selected_images = []
        self.selected_lang = tk.StringVar()
        self.selected_lang.set('Select Language')
        self.rmv_int_var = tk.BooleanVar(False)

        self.all_threads = {}

        self.all_langs = {
            'Afrikaans' : 'af', 'Amharic': 'am', 'Albanian' : 'sq', 'Arabic (Saudi Arabia)' : 'ar', 'Azerbaijani': 'az', 'Basque' : 'eu', 'Belarusian' : 'be', 'Bulgarian' : 'bg', 'Bengali': 'bn', 'Bosnian': 'bs', 'Catalan' : 'ca', 'Chinese' : 'zh-cn', 'Chinese (Taiwan)' : 'zh-tw', 'Corsican': 'co', 'Croatian' : 'hr', 'Czech' : 'cs', 'Danish' : 'da', 'Dutch' : 'nl', 'English' : 'en', 'Estonian' : 'et', 'Farsi' : 'fa', 'Finnish' : 'fi', 'French' : 'fr', 'Gaelic' : 'gd','Galician': 'gl', 'Gujarati': 'gu', 'German' : 'de', 'Greek' : 'el', 'Hebrew' : 'he', 'Hindi' : 'hi', 'Haitian': 'ht', 'Hungarian' : 'hu', 'Icelandic' : 'is', 'Indonesian' : 'id', 'Irish' : 'ga', 'Italian' : 'it', 'Japanese' : 'ja', 'Kannada': 'kn', 'Korean' : 'ko', 'Korean (Johab)' : 'ko', 'Kurdish' : 'ku', 'Latin': 'la', 'Latvian' : 'lv', 'Lithuanian' : 'lt', 'Macedonian (FYROM)' : 'mk', 'Malayalam' : 'ml', 'Malagasy': 'mg', 'Malaysian' : 'ms', 'Maltese' : 'mt', 'Mongolian': 'mn','Marathi': 'mr',  'Norwegian' : 'no', 'Polish' : 'pl', 'Portuguese' : 'pt', 'Punjabi' : 'pa', 'Romanian' : 'ro', 'Russian' : 'ru', 'Serbian' : 'sr', 'Slovak' : 'sk', 'Slovenian' : 'sl', 'Spanish' : 'es', 'Scottish Gaelic': 'gd', 'Swedish' : 'sv', 'Thai' : 'th', 'Turkish' : 'tr', 'Ukrainian' : 'uk', 'Urdu' : 'ur', 'Vietnamese' : 'vi', 'Welsh' : 'cy', 'Xhosa' : 'xh', 'Zulu' : 'zu',  'Nepali': 'ne' , 'Panjabi': 'pa', 'Pushto': 'ps', 'Sindhi': 'sd', 'Sinhala': 'si', 'Samoan': 'sm', 'Shona': 'sn', 'Somali': 'so', 'Southern Sotho': 'st', 'Tajik': 'tg', 'Tagalog': 'tl', 'Uighur': 'ug', 'Uzbek': 'uz', 
        }


    def start(self):
        self.root_header()
        self.language_section()
        self.image_area()
        self.footer()

    def root_header(self):
        self.header = tk.Frame(self.root, background='white')
        self.header.pack(fill=tk.X, ipadx=5, ipady=5)

        self.remove_sign_cbtn = tk.Checkbutton(self.header, text='Remove number & sign', background='white', variable=self.rmv_int_var, onvalue=True, offvalue=False)
        self.remove_sign_cbtn.pack(side=tk.LEFT)

        self.upload_img_btn = tk.Button(self.header, text='Upload Images', font=('sans-serif', 12), background='#009fd8', foreground='white', border=0, command=self.selected_image_pc)
        self.upload_img_btn.pack(side=tk.RIGHT, ipadx=10)

    def language_section(self):
        self.language_frame = tk.Frame(self.root)
        self.language_frame.pack(fill=tk.X)

        options = [i for i in self.all_langs]

        self.drop_down = ttk.Combobox(self.language_frame, textvariable=self.selected_lang, font=('sans-serif' , 12), height=10)
        self.drop_down['values'] = options
        self.drop_down.current(1)
        self.drop_down.pack(fill=tk.X)


    def image_area(self):
        self.image_s = tk.Frame(self.root)
        self.image_s.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.image_s)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.img_list = tk.Listbox(self.image_s, font=('sans-serif' , 11))
        self.img_list.pack(fill=tk.BOTH, expand=True)

        self.img_list.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.img_list.yview)

    def footer(self):
        self.footer_s = tk.Frame(self.root)
        self.footer_s.pack(side=tk.BOTTOM, fill=tk.X)

        self.export_btn = tk.Button(self.footer_s, text='Translate & Save', background='#009fd8', foreground='white', border=0, font=('sans-serif', 12), command=self.export_hander)
        self.export_btn.pack(fill=tk.X, ipady=5)

        self.progress_bar = ttk.Progressbar(self.footer_s, mode='determinate' , orient='horizontal')
        self.progress_bar.pack(fill=tk.X)


    def selected_image_pc(self):
        selected_images = filedialog.askopenfilenames(
            filetypes=[
                ('Image Files' , '.png'),
                ('Image Files' , '.jpg'),
                ('Image Files' , '.jpeg'),
            ]
        )
        self.all_selected_images = list(selected_images)
        self.show_images()

    def show_images(self):
        for img in self.all_selected_images:
            self.img_list.insert(0 , img)

    
    def export_hander(self):
        if len(self.all_selected_images) == 0:
            messagebox.showerror('Error' , 'Please select Images')
        else:
            time_now = str(datetime.datetime.now().strftime('%m%H%S'))
            self.all_threads[time_now] =  threading.Thread(name=time_now, target=self.image_processing)
            all_keys = self.all_threads.keys()
            all_keys = list(all_keys)
            self.all_threads[all_keys[-1]].setDaemon(True)
            self.all_threads[all_keys[-1]].start()

    def image_processing(self):
        self.progress_bar['value'] = 0

        if not os.path.isdir('./outputImages'):
            os.mkdir('outputImages')
        
        self.export_btn['text'] = 'Loading...'
        translator = Translator()
        prog_value = 100 / len(self.all_selected_images) 
        for index , img in enumerate(self.all_selected_images):
            img_splits = img.split('/')[-1].split('.')
            image_name = img_splits[0]
            image_ext = img_splits[1]
            try:
                if ' ' in img and ' ' not in image_name:
                    messagebox.showerror('Error' , 'Spaces are not allowed in Image path \ne.g /path/path with space/ not allowed \n Removing all images, Please select new one') 
                    self.all_selected_images = []
                    self.img_list.delete(0 , tk.END)
                    self.progress_bar['value'] = 0
            except:
                pass

            self.progress_bar['value'] += prog_value

            if self.rmv_int_var.get() :
                replace_w = {
                    '--' : '',
                    '(' : '',
                    ')' : '',
                    '_' : '',
                    '  ' : '',
                    '0' : '',
                    '1' : '',
                    '2' : '',
                    '3' : '',
                    '4' : '',
                    '5' : '',
                    '6' : '',
                    '7' : '',
                    '8' : '',
                    '9' : '',
                }
                for key, value in replace_w.items():
                    image_name = image_name.replace(key , value)

                if image_name[-1] == '-':
                    image_name = image_name.replace('-' , '')
            
            lang = self.selected_lang.get()
            lang = self.all_langs[lang]

            try:
                image_name = translator.translate(image_name, dest=lang)
                image_name = image_name.text
                image = Image.open(img)

                is_img_exist = os.path.exists(f'./outputImages/{image_name}.{image_ext}')
                if is_img_exist:
                    image_name += str(index)

                image.save(f'./outputImages/{image_name}.{image_ext}')
                idx = self.img_list.get(0, tk.END).index(img)
                self.img_list.delete(idx)
            except Exception as err:
                print(err)

        self.progress_bar['value'] = 100
        self.open_folder()
        
    def open_folder(self):
        pwd_path = os.getcwd()
        os.startfile(f'{pwd_path}/outputImages')
            

if __name__ == '__main__':
    # text = 'how are you'
    # translator = Translator()
    # get_text = translator.translate(text, dest='ur')
    # print(get_text.text)

        
    root = tk.Tk()
    translate_program = TranslatePrograme(root)
    translate_program.start()
    root.mainloop()