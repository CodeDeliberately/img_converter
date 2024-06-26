import PIL.Image
import pyperclip

# import tkinter as tk
import os

# from tkinter.filedialog import askopenfilename
import streamlit as st

# tk.Tk().withdraw()  # part of the import if you are not using other tkinter functions

suppress_blk = "Q"

st.sidebar.header(":rainbow[Options]")

while suppress_blk.lower() not in ["yes", "no"]:
    # suppress_blk = input("Do you want to suppress black pixels? (y/n)").lower()
    suppress_blk = st.sidebar.radio("Suppress black pixels?", ["Yes", "No"]).lower()

allow_relative_position = st.sidebar.radio(
    "Allow relative positioning?", ["Yes", "No"]
).lower()
if allow_relative_position == "yes":
    allow_relative_position = True
else:
    allow_relative_position = False

data = st.sidebar.file_uploader(
    "Upload you image", accept_multiple_files=False, type=["png", "jpg"]
)


# fn = askopenfilename(title="Which image to convert?")
# img_name = data.name


if suppress_blk == "yes":
    suppress_blk = 1
else:
    suppress_blk = 0

if data:
    try:
        img = PIL.Image.open(data).convert("RGB")
        # img = PIL.Image.open(img_name).convert("RGB")
    except Exception as e:
        print("Well, that didn't work.")
        print("With the following error: {}".format(e))
        img_name = "none.png"
        img = PIL.Image.new("RGB", (0, 0))

    func_name = os.path.basename(data.name).split(".")[0]

    pixels = list(img.getdata())
    for k in pixels:
        pass
        # print(k)
    (height, width) = img.size
    st.write(f"Height: {height}, Width: {width}")

    x = 0
    y = 0
    if allow_relative_position:
        output = "void draw_{0}(int x, int y) {1}\n".format(func_name, "{")
    else:
        output = "void draw_{0}() {1}\n".format(func_name, "{")
    for k in range(width):
        for j in range(height):
            if suppress_blk:
                if (
                    not pixels[x * width + y][0]
                    and not pixels[x * width + y][1]
                    and not pixels[x * width + y][2]
                ):
                    x += 1
                    if x >= width:
                        x = 0
                        y += 1
                    continue
            if allow_relative_position:
                output += "\tmatrix.drawPixel({0} + x, {1} + y, matrix.color565({2}, {3}, {4}));\n".format(
                    x,
                    y,
                    pixels[x * width + y][0],
                    pixels[x * width + y][1],
                    pixels[x * width + y][2],
                )
            else:
                output += "\tmatrix.drawPixel({0}, {1}, matrix.color565({2}, {3}, {4}));\n".format(
                    x,
                    y,
                    pixels[x * width + y][0],
                    pixels[x * width + y][1],
                    pixels[x * width + y][2],
                )
            x += 1
            if x >= width:
                x = 0
                y += 1
    output += "}\n"
    # code = st.text_area("Copy This Code", value=ouput, key="code")
    st.code(output, language="C++")
    # print(ouput)
