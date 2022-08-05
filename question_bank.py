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

# create import frame
import_qa = tk.Frame(root)
import_qa.grid()


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
            x = ""
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
    import_qa.grid_forget()
    test.grid()


# set button
import_q_button = tk.Button(
    import_qa,
    text="導入題目",
    font=("標楷體", 20),
    command=import_questions
).grid(column=0, row=0, padx=10, pady=10, sticky=tk.EW)

import_a_button = tk.Button(
    import_qa,
    text="導入答案",
    font=("標楷體", 20),
    command=import_answers
).grid(column=0, row=1, padx=10, pady=10, sticky=tk.EW)

# set entry
q_filename = tk.Entry(
    import_qa,
    width=50,
    font=("Times New Roman", 20)
)
q_filename.grid(column=1, row=0, padx=10, pady=10, sticky=tk.EW)

a_filename = tk.Entry(
    import_qa,
    width=50,
    font=("Times New Roman", 20)
)
a_filename.grid(column=1, row=1, padx=10, pady=10, sticky=tk.EW)

# set button
start_btn = tk.Button(
    import_qa,
    text="開始測驗",
    font=("標楷體", 20),
    command=start_command
).grid(column=0, row=2, padx=10, pady=10, sticky=tk.EW)

# create menu frame
menu = tk.Frame(root)

# create menu button
restart_btn = tk.Button(
    menu,
    text="重新作答",
    font=("標楷體", 20),
    command=lambda: [menu.grid_forget(), test.grid()]
).grid(column=0, row=0, padx=10, pady=10, sticky=tk.EW)

wrong_btn = tk.Button(
    menu,
    text="錯題練習",
    font=("標楷體", 20),
    command=lambda: [menu.grid_forget(), wrong_review.grid(), command_wrong()]
).grid(column=0, row=1, padx=10, pady=10, sticky=tk.EW)

wrong_review = tk.Frame(root)

# x1 用來記錄錯誤的題目
x1 = []
x2 = []
# 和此 py 檔在同一個資料夾內才可以直接用檔名
df = pd.DataFrame(pd.read_csv('question_bank.csv'))


def command_wrong():
    if len(x1) == 0:
        lbl_q2 = tk.Label(
            wrong_review,
            text="目前無題目!!",
            bg="white",
            fg="black",
            font=("標楷體", 20),
            width=60,
            height=10,
            wraplength=600,
            justify="left",
        )
        lbl_q2.grid(column=1, row=0, padx=5, pady=5, sticky=tk.EW)
        b8 = tk.Button(
            wrong_review,
            text="返回選單",
            font=("標楷體", 15),
            wraplength=600,
            justify="left",
            width=60,
            height=2,
            command=lambda: [wrong_review.grid_forget(), menu.grid()]
        )
        b8.grid(column=1, row=1, padx=20, pady=20)
    else:
        wrong_index = random.choice(x1)
        x1.remove(wrong_index)
        lbl_q2 = tk.Label(
            wrong_review,
            text="Q:"+df.loc[wrong_index, "question"],
            bg="white",
            fg="black",
            font=("標楷體", 20),
            width=60,
            height=10,
            wraplength=600,
            justify="left",
        )
        lbl_q2.grid(column=1, row=0, padx=5, pady=5, sticky=tk.EW)

        lbl_a2 = tk.Label(
            wrong_review,
            text="",
            fg="black",
            font=("標楷體", 20),
            width=60,
            height=1
        )
        lbl_a2.grid(column=1, row=5, padx=5, pady=5, sticky=tk.EW)

        b5 = tk.Button(
            wrong_review,
            text=df.loc[wrong_index, "option_A"],
            font=("標楷體", 15),
            wraplength=600,
            justify="left",
            width=60,
            height=2,
            command=lambda: button_command3(b5, "A")
        )
        b5.grid(column=1, row=1, padx=5, pady=5)

        b6 = tk.Button(
            wrong_review,
            text=df.loc[wrong_index, "option_B"],
            font=("標楷體", 15),
            wraplength=600,
            justify="left",
            width=60,
            height=2,
            command=lambda: button_command3(b6, "B")
        )
        b6.grid(column=1, row=2, padx=5, pady=5)

        b7 = tk.Button(
            wrong_review,
            text=df.loc[wrong_index, "option_C"],
            font=("標楷體", 15),
            wraplength=600,
            justify="left",
            width=60,
            height=2,
            command=lambda: button_command3(b7, "C")
        )
        b7.grid(column=1, row=3, padx=5, pady=5)

        b8 = tk.Button(
            wrong_review,
            text=df.loc[wrong_index, "option_D"],
            font=("標楷體", 15),
            wraplength=600,
            justify="left",
            width=60,
            height=2,
            command=lambda: button_command3(b8, "D")
        )
        b8.grid(column=1, row=4, padx=5, pady=5)

        list_2 = [b5, b6, b7, b8]

        def button_command3(button, option):
            if df.loc[wrong_index, "answer"] == option:
                for b in list_2:
                    b.configure(state=tk.DISABLED, disabledforeground="gray")
                button.configure(state=tk.DISABLED,
                                 disabledforeground="black", bg="green")
            else:
                for b in list_2:
                    b.configure(state=tk.DISABLED, disabledforeground="gray")
                button.configure(state=tk.DISABLED,
                                 disabledforeground="black", bg="red")
                if x2.count(wrong_index) == 0:
                    x2.append(wrong_index)
                lbl_a2.configure(text=f"正確答案:" + df.loc[wrong_index, "answer"])

        def next_command2():
            if len(x1) == 0:
                messagebox.showinfo("info", "試題結束")
            wrong_index1 = random.choice(x1)
            x1.remove(wrong_index1)
            lbl_q2["text"] = "Q:"+df.loc[wrong_index1, "question"]
            lbl_a2.configure(text="")
            b5["text"] = df.loc[wrong_index1, "option_A"]
            b6["text"] = df.loc[wrong_index1, "option_B"]
            b7["text"] = df.loc[wrong_index1, "option_C"]
            b8["text"] = df.loc[wrong_index1, "option_D"]
            for b in list_2:
                b.configure(state=tk.NORMAL, bg=orig_color)

            def button_command4(button2, option2):
                if df.loc[wrong_index1, "answer"] == option2:
                    for b in list_2:
                        b.configure(state=tk.DISABLED,
                                    disabledforeground="gray")
                    button2.configure(state=tk.DISABLED,
                                      disabledforeground="black", bg="green")
                else:
                    for b in list_2:
                        b.configure(state=tk.DISABLED,
                                    disabledforeground="gray")
                    button2.configure(state=tk.DISABLED,
                                      disabledforeground="black", bg="red")
                    x2.append(wrong_index1)
                    lbl_a2.configure(
                        text="正確答案:" + df.loc[wrong_index1, "answer"])
            b5["command"] = lambda: button_command4(b5, "A")
            b6["command"] = lambda: button_command4(b6, "B")
            b7["command"] = lambda: button_command4(b7, "C")
            b8["command"] = lambda: button_command4(b8, "D")

        next_btn2 = tk.Button(
            wrong_review,
            text="下一題",
            fg="black",
            font=("標楷體", 20),
            command=next_command2
        )
        next_btn2.grid(column=1, row=10, padx=20, pady=30)

        back_btn2 = tk.Button(
            wrong_review,
            text="結束測驗",
            bg="white",
            fg="black",
            font=("標楷體", 12),
            width=10,
            height=2,
            command=lambda: [wrong_review.grid_forget(), menu.grid()]
        )
        back_btn2.grid(column=0, row=12, padx=5, pady=5, sticky=tk.EW)


def download():
    df2 = pd.DataFrame(columns=df.columns)
    for i in x2:
        df2 = pd.concat([df2, df.iloc[i:i+1]])
    doc = docx.Document()
    for i in range(df2.shape[0]):
        for j in range(df2.shape[1]):
            doc.add_paragraph(str(df2.values[i, j]))
    doc.save("frequently_wrong.docx")


btn_save = tk.Button(
    menu,
    text="下載常錯題目.docx",
    fg="black",
    font=("標楷體", 20),
    command=lambda: download()
).grid(column=0, row=2, padx=10, pady=10, sticky=tk.EW)

test = tk.Frame(root)
test.columnconfigure(0, weight=10)
test.columnconfigure(1, weight=870)

back_btn1 = tk.Button(
    test,
    text="結束測驗",
    bg="white",
    fg="black",
    font=("標楷體", 12),
    width=10,
    height=2,
    command=lambda: [test.grid_forget(), menu.grid()]
)
back_btn1.grid(column=0, row=12, padx=5, pady=5, sticky=tk.EW)


x = []
for i in range(len(df)):
    x.append(i)
# 隨機選取題號索引（整數）
question_index = random.choice(x)
x.remove(question_index)
# 特定欄、列的值： data.loc[列的索引, 欄位標題]

lbl_q1 = tk.Label(
    test,
    text="Q:"+df.loc[question_index, "question"],
    bg="white",
    fg="black",
    font=("標楷體", 20),
    width=60,
    height=10,
    wraplength=600,
    justify="left",
)  # wraplength:指定多少單位後開始換行；justify:指定多行的對齊方式；anchor:指定文字或影像在Label中的顯示位置
lbl_q1.grid(column=1, row=0, padx=5, pady=5, sticky=tk.EW)

lbl_a1 = tk.Label(
    test,
    text="",
    fg="black",
    font=("標楷體", 20),
    width=60,
    height=1
)
lbl_a1.grid(column=1, row=5, padx=5, pady=5, sticky=tk.EW)

b1 = tk.Button(
    test,
    text=df.loc[question_index, "option_A"],
    font=("標楷體", 15),
    wraplength=600,
    justify="left",
    width=60,
    height=2,
    command=lambda: button_command1(b1, "A")
)
# 按下按鈕後的背景顏色、文字顏色（前景）
# btn["activebackground"] = "white"
# btn["activeforeground"] = "black"
b1.grid(column=1, row=1, padx=5, pady=5)

# 取得背景色（即按鈕背景色）
orig_color = b1.cget("background")

b2 = tk.Button(
    test,
    text=df.loc[question_index, "option_B"],
    font=("標楷體", 15),
    wraplength=600,
    justify="left",
    width=60,
    height=2,
    command=lambda: button_command1(b2, "B")
)
b2.grid(column=1, row=2, padx=5, pady=5)

b3 = tk.Button(
    test,
    text=df.loc[question_index, "option_C"],
    font=("標楷體", 15),
    wraplength=600,
    justify="left",
    width=60,
    height=2,
    command=lambda: button_command1(b3, "C")
)
b3.grid(column=1, row=3, padx=5, pady=5)

b4 = tk.Button(
    test,
    text=df.loc[question_index, "option_D"],
    font=("標楷體", 15),
    wraplength=600,
    justify="left",
    width=60,
    height=2,
    command=lambda: button_command1(b4, "D")
)
b4.grid(column=1, row=4, padx=5, pady=5)

list_1 = [b1, b2, b3, b4]


def button_command1(button, option):
    if df.loc[question_index, "answer"] == option:
        for b in list_1:
            b.configure(state=tk.DISABLED, disabledforeground="gray")
        button.configure(state=tk.DISABLED,
                         disabledforeground="black", bg="green")
    else:
        for b in list_1:
            b.configure(state=tk.DISABLED, disabledforeground="gray")
        button.configure(state=tk.DISABLED,
                         disabledforeground="black", bg="red")
        lbl_a1.configure(text=f"正確答案:" + df.loc[question_index, "answer"])
        x1.append(question_index)


def next_command1():
    if len(x) == 0:
        messagebox.showinfo("info", "試題結束")
        for i in range(len(df)):
            x.append(i)
        question_index1 = random.choice(x)
        x.remove(question_index1)
        test.grid_forget()
        menu.grid()
    question_index1 = random.choice(x)
    x.remove(question_index1)
    lbl_q1["text"] = "Q:"+df.loc[question_index1, "question"]
    lbl_a1.configure(text="")
    b1["text"] = df.loc[question_index1, "option_A"]
    b2["text"] = df.loc[question_index1, "option_B"]
    b3["text"] = df.loc[question_index1, "option_C"]
    b4["text"] = df.loc[question_index1, "option_D"]
    for b in list_1:
        b.configure(state=tk.NORMAL, bg=orig_color)

    def button_command2(button1, option1):
        if df.loc[question_index1, "answer"] == option1:
            for b in list_1:
                b.configure(state=tk.DISABLED, disabledforeground="gray")
            button1.configure(state=tk.DISABLED,
                              disabledforeground="black", bg="green")
        else:
            for b in list_1:
                b.configure(state=tk.DISABLED, disabledforeground="gray")
            button1.configure(state=tk.DISABLED,
                              disabledforeground="black", bg="red")
            x1.append(question_index1)
            lbl_a1.configure(text="正確答案:" + df.loc[question_index1, "answer"])
    b1["command"] = lambda: button_command2(b1, "A")
    b2["command"] = lambda: button_command2(b2, "B")
    b3["command"] = lambda: button_command2(b3, "C")
    b4["command"] = lambda: button_command2(b4, "D")


next_btn1 = tk.Button(
    test,
    text="下一題",
    fg="black",
    font=("標楷體", 20),
    command=next_command1
)
next_btn1.grid(column=1, row=10, padx=20, pady=30)


tk.Frame.tkraise(menu)


root.mainloop()
