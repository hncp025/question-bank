from fileinput import filename
import tkinter as tk
from tkinter import filedialog
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from pandas.core.frame import DataFrame
import pandas as pd
import random
import docx
from tkinter import messagebox

# create window
root = tk.Tk()
root.title("question bank")
root.geometry("1000x800")


# def button command
def import_questions():
    files = filedialog.askopenfilename(
        title="open a file",
        filetypes=[("pdf files", "*.pdf")],
        multiple=True
    )
    var = root.tk.splitlist(files)
    q_filename.insert("insert", var)

    # convert pdf to txt
    def convert_pdf_to_txt(path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, "rb")
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text

    s = ""
    for file in var:
        t = convert_pdf_to_txt(file)
        # multiple replacement
        t = t.replace("", "(A)")
        t = t.replace("", "(B)")
        t = t.replace("", "(C)")
        t = t.replace("", "(D)")
        t = t.replace("1(A)", "(A)1")
        t = t.replace("2(B)", "(B)2")
        t = t.replace("3(C)", "(C)3")
        t = t.replace("4(D)", "(D)4")
        t = t.replace("計算器。", "計算器。\n")
        t = t.replace("\t", "")
        s += t + "\n"
        question_file = open("question_bank.txt", "w", encoding="utf-8")
        question_file.write(s)
        question_file.close()
    x = ""

    global questions, option_A, option_B, option_C, option_D
    questions = []
    option_A = []
    option_B = []
    option_C = []
    option_D = []
    for line in s.split():
        if line.startswith("(A)"):
            option_A.append(line.replace("\n", ""))
            questions.append(x)
            x = ""
        elif line.startswith("(B)"):
            option_B.append(line.replace("\n", ""))
        elif line.startswith("(C)"):
            option_C.append(line.replace("\n", ""))
        elif line.startswith("(D)"):
            option_D.append(line.replace("\n", ""))
        else:
            x += line.replace("\n", "")
    # print(len(questions))
    # print(len(option_A))
    # print(len(option_B))
    # print(len(option_C))
    # print(len(option_D))



def import_answers():
    files = filedialog.askopenfilename(
        title="open a file",
        filetypes=[("pdf files", "*.pdf")],
        multiple=True
    )
    var = root.tk.splitlist(files)
    a_filename.insert("insert", var)

    # convert pdf to txt
    def convert_pdf_to_txt(path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, "rb")
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text

    s = ""
    for file in var:
        t = convert_pdf_to_txt(file)
        s += t

    global answers
    answers = []
    answer = ["A", "B", "C", "D"]
    for line in s.split():
        for i in answer:
            if line.replace("\n", "") == i:
                answers.append(line.replace("\n", ""))
    # print(len(answers))


def start_command():
    df = DataFrame({
        "question": questions,
        "option_A": option_A,
        "option_B": option_B,
        "option_C": option_C,
        "option_D": option_D,
        "answer": answers
    })
    df.to_csv("question_bank.csv", encoding="utf-8")







# set button
import_q_button = tk.Button(
    root,
    text="導入題目",
    font=("標楷體", 20),
    command=import_questions
).grid(column=0, row=0, padx=10, pady=10, sticky=tk.EW)

import_a_button = tk.Button(
    root,
    text="導入答案",
    font=("標楷體", 20),
    command=import_answers
).grid(column=0, row=1, padx=10, pady=10, sticky=tk.EW)

# set entry
q_filename = tk.Entry(
    root,
    width=50,
    font=("Times New Roman", 20)
)
q_filename.grid(column=1, row=0, padx=10, pady=10, sticky=tk.EW)

a_filename = tk.Entry(
    root,
    width=50,
    font=("Times New Roman", 20)
)
a_filename.grid(column=1, row=1, padx=10, pady=10, sticky=tk.EW)

# set button
start_btn = tk.Button(
    root,
    text="開始測驗",
    font=("標楷體", 20),
    command=start_command
).grid(column=0, row=2, padx=10, pady=10, sticky=tk.EW)



root.mainloop()
