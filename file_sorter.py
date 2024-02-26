#=============PROGRAM PARAMETERS=============
# ^ -- Param for naming the dropdown menu -- 
custom_naming = False

# ^ -- Param for resizing the tkinter window --
resize_prp = False

# ~ -- Param for the default font -- 
font = "Roboto"

# ~ -- Param for the default window size --
size_prp = "700x450"

#=======LOGGER=======
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler()
    ],
    format='[%(asctime)s] - [%(levelname)s] - %(message)s'
)
#=========PREPING THE STORED DATA=========
import json
import platform
import os
import sys

#PREPAIRING THE STORED VALUES
def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        logger.info("JSON file read.")
        return data
    except FileNotFoundError:
        logger.error(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON data from '{file_path}'.")
        return None

def write_json(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        logger.info(f"JSON data written to '{file_path}' successfully.")
        return True
    except TypeError:
        logger.error("Invalid data format. Expected a dictionary.")
        return False
    except IOError:
        logger.error(f"Error writing to file '{file_path}'.")
        return False

fl_names_defaults = [
    'sorted_files',
    'raw',
    'videos',
    'photos',
    'apps',
    'plain_text',
    'zipped_files',
    'install_files',
    'pdf_documents',
    'python_code',
    'ms_excel_spreadsheets',
    'ms_powerpoint_presentations',
    'android_applications',
    'web_files',
    'ms_word_docs',
    'torrents',
    'Minecraft_mods',
    'books',
    'audio_files',
    'local',
    'other'
]

extensions = [
    ("nef",    1), 
    ("exe",    4),
    ("app",    4),
    ("mpeg-4", 2),
    ("webm",   2),
    ("txt",    5),
    ("png",    3),
    ("jpg",    3),
    ("jpeg",   3),
    ("heic",   3),
    ("heif",   3),
    ("zip",    6),
    ("gz",     6),
    ("7z",     6),
    ("webp",   3),
    ("dmg",    7), 
    ("htm",    5), 
    ("pdf",    8),
    ("py",     9),
    ("xls",    10), 
    ("rar",    6), 
    ("jar",    16), 
    ("ipa",    4),
    ("bibtex", 17),
    ("docx",   14),
    ("wav",    18),
    ("mp3",    18),
    ("torrent",15),
    ("html",   13),
    ("mp4",    2),
    ("pkg",    7),
    ("iso",    7), 
    ("msi",    7),
    ("acsm",   17),
    ("pyc",    9),
    ("epub",   17),
    ("ris",    17),
    ("enw",    17),
    ("com",    13),
    ("mov",    2),
    ("pptx",   11),
    ("apk",    12),
    ("xz",     6),
    ("mpg",    2),
    ("mkv",    2),
    ("aifc",   18),
    ("icns",   3)
]

package_nn = {
    "version":"2.3.1",
    "author":"JL Studios",
    "copyright":True
}

json_file = 'stored_data.json'

if read_json('package.json') != package_nn:
    logger.error("This is a cracked version. Program auto closed.")
    sys.exit()
else:
    logger.info("License correct!")

if os.path.exists(json_file):
    logger.info('Json exists, skipping step')

    data_js = read_json(json_file)

else:
    logger.info('Json does not exist, writing file')

    write_json({
        "folder_names":fl_names_defaults,
        "pkg installed":False,
        "packages":['tkmacosx'],
        "last_dir":None
    } ,json_file)

    logger.info('Sucessfully written file')

    data_js = read_json(json_file)

#=========IMPORTING PACKAGES=========
if platform.system() == "Darwin":
    logging.info(f"The computer is running MacOS based on '{platform.system()}'")

    if data_js["pkg installed"] == False:
        logger.info("tkmacosx package not installed. Installing...")

        version = ''
        f = 0

        for i in sys.version:
            if i == '.' and f == 0:
                f = 1
            elif i == '.' and f == 1:
                break
            version += i

        for j in data_js['packages']:
            os.system(f'pip{version} install {j}')
            logger.info(f'Package {j} installed')
        
        data_js['pkg installed'] = True

        write_json(data_js, json_file)

        logger.info("All packages installed")

    elif data_js["pkg installed"] == True:
        logger.info("packages installed, skipping a step")

    try:
        logger.info("Importing required MacOS packages...")
        from tkmacosx import *
        from tkmacosx import Button

        logger.info("Imported")

    except Exception as e:
        logger.error(f"Failed to load MacOS package: {e}")

elif platform.system() == "Windows":
    logger.info(f"The computer is running Windows based on '{platform.system()}'")

    from tkinter import Button

#=====IMPORTS=====
import shutil
from tkinter import Tk, Label, Entry, Checkbutton
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import time
from PIL import Image, ImageTk

#==========CODE===========
#-----MAIN CODE-----
fl_names = data_js['folder_names']
sorted_fl = '/'

def make_sort_fldr():
    global sorted_fl
    
    if check_sort.get():
        sorted_fl = "/"+fl_names[0]+"/"
        logger.info("Set the extra sorting folder to True")

    else:
        sorted_fl = "/"
        logger.info("Set the extra sorting folder to False")

def sort_d_ds():
    if check_sort_deep.get():
        logger.info("Set the dirs to sort seperately in this directory to True")

    else:
        logger.info("Set the dirs to sort seperately in this directory to False")

def get_immediate_subdirectories(directory):
    subdirectories = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path):
            subdirectories.append(path)
    return subdirectories

def select_directory():
    global selected_directory

    dir_in = data_js["last_dir"]

    selected_directory = filedialog.askdirectory(initialdir=dir_in)

    if selected_directory:
        dirlabel.configure(text=f"Selected directory")
        entry.delete(0, tk.END)
        data_js["last_dir"] = os.path.dirname(selected_directory)

        logger.info(f"Set dir initial location to {data_js['last_dir']}")

        entry.insert(0, selected_directory)

        write_json(data_js ,json_file)
    else:
        dirlabel.configure(text="No directory selected")

def move_directories(source_folder, destination_folder, exclude=[]):
    """
    Move all directories from source_folder to destination_folder while excluding the specified directories.
    
    Args:
        source_folder (str): Path to the source folder containing directories to move.
        destination_folder (str): Path to the destination folder where directories will be moved.
        exclude (list): List of directory names to exclude from the moving process.
    """
    items = os.listdir(source_folder)
    
    for item in items:
        item_path = os.path.join(source_folder, item)
        
        if os.path.isdir(item_path):
            if item not in exclude:
                if os.path.exists(destination_folder) == False:
                    os.mkdir(destination_folder)
                    logger.info(f"Made root sorting file at {destination_folder}")

                else:
                    logger.info(f"Root folder already exists at: '{destination_folder}'. Skipping a step")

                logger.info(f"Moving item: {item_path}")
                shutil.move(item_path, destination_folder)

            else:
                logger.info(f"item: '{item_path}' is skipped")

def sorting_alg(maindir):
    try:
        maindir += '/'

        alldir=os.listdir(maindir)
        dirs={}

        for i in alldir: #getting the extension of each file seperatly
            a=""
            for j in i[::-1]:
                if j == ".":
                    dirs[i]=a[::-1] # adding them into a dict
                    break
                else:
                    a+=j

        logger.info("All extensions succsefully got")
        logger.info(f"Sorting starting on: {maindir}")

        #making all the folders
        dirlabel.configure(text="Creating folders...")
        logger.info("Creating folders...")

        if os.path.exists(maindir+sorted_fl) == False:
            os.mkdir(maindir+sorted_fl)
            logger.info(f"Made root sorting file at {maindir+sorted_fl}")
        
        else:
            logger.info(f"Root folder already exists at: '{maindir+sorted_fl}'. Skipping a step")
        
        #getting all the difirent extensions in a list
        new_list=[]
        for one_student_choice in dirs.values():
            if one_student_choice not in new_list:
                new_list.append(one_student_choice)

        for num, j in enumerate(new_list):
            logger.info(f"{num+1}. possible extensions: {j.lower()}")

        for k,v in dirs.items():
            v = str(v).lower()

            for ext, indx in extensions:
                if v == ext:
                    if os.path.isfile(maindir+k) or v == 'app':
                        if os.path.exists(maindir+sorted_fl+"/"+fl_names[indx]) == False:
                            os.mkdir(maindir+sorted_fl+"/"+fl_names[indx])
                            logger.info(f"Folder for file: '{ext}' doesn't exist")
                            logger.info(f"Making Folder '{fl_names[indx]}'...")

                        try:
                            shutil.move(maindir+k, maindir+sorted_fl+f"/{fl_names[indx]}/"+k)
                            logger.info(f"Moving file: '{k}'")
                            break
                        
                        except Exception as e:
                            logger.error(f"Failed to move file: {e}")


        try:   
            move_directories(maindir, maindir+sorted_fl+fl_names[-2], fl_names)
            logger.info("Moved directories")

        except Exception as e:
            logger.error(f"Failed to sort directories: {e}")
        
        try:
            logger.info('Moiving remaining files...')

            for dir in os.listdir(maindir):
                if not dir in fl_names:
                    if os.path.exists(maindir+sorted_fl+"/"+fl_names[-1]) == False:
                        os.mkdir(maindir+sorted_fl+"/"+fl_names[-1])
                        logger.info(f"Folder for file: '{fl_names[-1]}' doesn't exist")
                        logger.info(f"Making Folder '{fl_names[-1]}'...")

                    try:
                        shutil.move(maindir+dir, maindir+sorted_fl+f"/{fl_names[-1]}/"+dir)
                        logger.info(f"Moving file: '{dir}'")
                    
                    except Exception as e:
                        logger.error(f"Failed to move file: {e}")

        except Exception as e:
            logger.error(f"Could not sort remaining files: {e}")

        dirlabel.configure(text="Sorting...")

        dirlabel.configure(text="Sorted!")
        logger.info("Sorted!")
        return True

    except Exception as e:
        dirlabel.configure(text="Sorting failed. Please try again")
        logger.error(f"Sorting failed: {e}")
        return False

def sort_files():
    logger.info("Changing input directory...")

    maindir = entry.get()

    if maindir == None:
        dirlabel.configure(text="Please enter a directory!")

    elif maindir == "":
        dirlabel.configure(text="Please enter a directory!")
    
    elif maindir != selected_directory:
        dirlabel.configure(text="Please enter a valid directory")

    else:
        start_time = time.time()

        num_items = 0

        logger.info("Valid directory, copy started")

        if check_sort_deep.get():
            for indx, i in enumerate(get_immediate_subdirectories(maindir)):
                num_items += len(os.listdir(i))

                if sorting_alg(i):
                    logger.info(f"Sorting {indx+1} done")
                else:
                    logger.error(f"Sorting {indx+1} failed")
        else:
            num_items = len(os.listdir(maindir))

            sorting_alg(maindir)
        
        end_time = time.time()
        sorting_time = end_time - start_time

        speed(sorting_time, num_items)

def speed(t, itms):
    speed_res = round((t / itms) *10_000, 3)

    speed_lbl.configure(text=f"Speed: {speed_res}s per 10.000 files")

    canvas.delete("image")

    if 4 > int(speed_res):
        image = resize_image('images/speed_6.png', 260, 260)

    elif 5 > int(speed_res) >= 4:
        image = resize_image('images/speed_5.png', 260, 260)

    elif 7 > int(speed_res) >= 5:
        image = resize_image('images/speed_4.png', 260, 260)

    elif 9 > int(speed_res) >= 7:
        image = resize_image('images/speed_3.png', 260, 260)
    
    elif 11 > int(speed_res) >= 9:
        image = resize_image('images/speed_2.png', 260, 260)
    
    elif int(speed_res) >= 11:
        image = resize_image('images/speed_1.png', 260, 260)

    canvas.create_image(130, 110, anchor=tk.CENTER, image=image)
    canvas.image = image

def handle_dropdown_selection(event):
    pass

def change_fl_names():
    global fl_names

    try:
        sel_val = dropdown.current()
        req_name = entry_drp.get()

        if req_name != 'Enter folder name here...':
            old_name = fl_names[sel_val]
            fl_names[sel_val] = req_name
            data_js['folder_names'] = fl_names

            write_json(data_js, json_file)

            dp_valuess = []

            for indx, i in enumerate(fl_names):
                if custom_naming == True:
                    if indx == 0:
                        a = 'Folder with sorted files'
                    elif indx == len(fl_names) - 1:
                        a = f'Folder with {i} files'
                    elif indx == len(fl_names) - 2:
                        a = 'Folder with folders in dir'
                    elif indx in [1, 5, 9]:
                        a = f'Folder with {i} files'
                    elif indx in [6, 7, 13, 18]:
                        a = f'Folder with {i}'
                    else:
                        a = f'Folder with {i[:-1]} files'
                        
                else:
                    a = f"Folder named -> '{i}'"
                    
                dp_valuess.append(a)

            dropdown['values'] = dp_valuess

            logger.info(f"Succsesfully renaimed {old_name} to {fl_names[sel_val]}")
            dirlabel.configure(text=f"Renaimed to {fl_names[sel_val]}")
        else:
            dirlabel.configure(text=f"Enter text for renaiming!")
    
    except Exception as e:
        logger.error(f"failed to rename folders: {e}")

def on_entry_click(event):
    if entry_drp.get() == 'Enter folder name here...':
       entry_drp.delete(0, tk.END) 
       entry_drp.insert(0, '') 
       entry_drp.configure(fg = 'black')

def on_focusout(event):
    if entry_drp.get() == '':
        entry_drp.insert(0, 'Enter folder name here...')
        entry_drp.configure(fg = 'grey')

def resize_image(input_image_path, width, height):
    input_image = Image.open(input_image_path)
    resized_image = input_image.resize((width, height))
    tk_image = ImageTk.PhotoImage(resized_image)

    return tk_image

#-----GUI-----
root = Tk()
root.geometry(size_prp)
root.title("Sorting files")
root.resizable(resize_prp, resize_prp)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.grid_rowconfigure(1, weight=1)

frame_t_l = tk.Frame(root)
frame_t_r = tk.Frame(root)
frame_btm = tk.Frame(root)
frame_tp = tk.Frame(root)

frame_tp.grid(row=0, column=0, columnspan=2, sticky="ew")
frame_btm.grid(row=2, column=0, columnspan=2, sticky="ew")
frame_t_l.grid(row=1, column=0, sticky="nsew")
frame_t_r.grid(row=1, column=1, sticky="nsew")

frame_t_r.grid_columnconfigure(0, weight=1)

frame_btm.grid_columnconfigure(0, weight=1)

Label(
    frame_tp, 
    text="File Sorter", 
    font=(font, 30), 
    highlightthickness=0
).pack()

entry = Entry(
    frame_btm, 
    font=(font, 14)
)

slc_btn = Button(
    frame_btm, 
    text="Select directory", 
    font=(font, 14), 
    command=select_directory,
    highlightthickness=0
)

sort = Button(
    frame_btm, 
    command=sort_files, 
    text="Sort", 
    font=(font, 20),
    highlightthickness=0
)

dirlabel = Label(
    frame_t_l, 
    text="Click select dirctory to begin", 
    font=(font, 15), 
    highlightthickness=0
)

entry.grid(row=1, column=0, sticky='nswe', padx=5, pady=10)
slc_btn.grid(row=1, column=1, sticky='nse', padx=5, pady=10)

check_sort     = tk.BooleanVar(value=False)
check_sort_deep= tk.BooleanVar(value=False)
selected_value = tk.StringVar()

sort_t_fldr = Checkbutton(
    frame_t_l, 
    text="Make seperate folder in dir", 
    command=make_sort_fldr, 
    variable=check_sort, 
    highlightthickness=0
)

sort_d_dss = Checkbutton(
    frame_t_l, 
    text="Sort all dirs in this directory seperately", 
    command=sort_d_ds, 
    variable=check_sort_deep, 
    highlightthickness=0
)

s = ttk.Style()
s.configure('.', highlightthickness=0)

dropdown = ttk.Combobox(
    frame_t_l, 
    textvariable=selected_value, 
    state="readonly",
    width=30
)
dp_values = []

for indx, i in enumerate(fl_names):
    if custom_naming == True:
        if indx == 0:
            a = 'Folder with sorted files'
        elif indx == len(fl_names) - 1:
            a = f'Folder with {i} files'
        elif indx == len(fl_names) - 2:
            a = 'Folder with folders in dir'
        elif indx in [1, 5, 9]:
            a = f'Folder with {i} files'
        elif indx in [6, 7, 13, 18]:
            a = f'Folder with {i}'
        else:
            a = f'Folder with {i[:-1]} files'
            
    else:
        a = f"Folder named -> '{i}'"
        
    dp_values.append(a)

dropdown['values'] = dp_values
dropdown.current(0)

# Bind an event to handle selection changes
dropdown.bind("<<ComboboxSelected>>", handle_dropdown_selection)

entry_drp = Entry(
    frame_t_l,
    font=(font, 14),
    fg = 'grey'
)

entry_drp.insert(0, 'Enter folder name here...')
entry_drp.bind('<FocusIn>', on_entry_click)
entry_drp.bind('<FocusOut>', on_focusout)

btn_drp = Button(
    frame_t_l,
    text="Change",
    font=(font, 14),
    command=change_fl_names,
    highlightthickness=0
)

chk_test1 = Checkbutton(
    frame_t_r, 
    text="Test 1", 
    command=None, 
    highlightthickness=0
)

chk_test2 = Checkbutton(
    frame_t_r, 
    text="Test 2", 
    command=None, 
    highlightthickness=0
)

chk_test3 = Checkbutton(
    frame_t_r, 
    text="Test 3", 
    command=None, 
    highlightthickness=0
)

chk_test4 = Checkbutton(
    frame_t_r, 
    text="Test 4", 
    command=None, 
    highlightthickness=0
)


dropdown.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', columnspan=2)
entry_drp.grid(row=1, column=0, padx=10, pady=10, sticky='nswe')
btn_drp.grid(row=1, column=1, padx=10, pady=10, sticky='nw')
sort_t_fldr.grid(row=2, column=0, padx=10, pady=10, sticky='nw')
sort_d_dss.grid(row=3, column=0, padx=10, pady=10, sticky='nw')

sort.grid(row=0, column=0, columnspan=2, sticky="nswe", padx=5)
dirlabel.grid(row=4, column=0, padx=10, pady=10, columnspan=2, sticky="nw")

canvas = tk.Canvas(frame_t_r, width=260, height=200)

speed_lbl = Label(
    frame_t_r,
    font=(font, 14),
    text="Speed: ?s per 10.000 files"
)
canvas.pack()
speed_lbl.pack(padx=10, pady=10)

image = resize_image('images/speed_1.png', 260, 260)

canvas.create_image(130, 110, anchor=tk.CENTER, image=image)
canvas.image = image

root.mainloop()