import json
import tkinter as tk
from tkinter import messagebox



def load_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        while True:
            try:
                object_json = json.loads(f.readline())
                data.append(object_json)
            except json.JSONDecodeError:
                break
            except StopIteration:
                break
    return data



def answer_picked(index):
    global current_question, human_vs_chatgpt
    if index < len(date[current_question]["human_answers"]):
        human_vs_chatgpt["human"] += 1
    else:
        human_vs_chatgpt["chatgpt"] += 1
    current_question += 1
    if current_question < len(date):
        display_qa()
    else:
        messagebox.showinfo("Final counting", f"Human answers: {human_vs_chatgpt['human']}\n"
                                              f"ChatGPT answers: {human_vs_chatgpt['chatgpt']}")
        root.destroy()



def display_qa():
    question_info.config(text=date[current_question]["question"])


    for widget in answer_frame.winfo_children():
        widget.destroy()

    answer_human = date[current_question]["human_answers"]
    answer_chatgpt = date[current_question]["chatgpt_answers"]
    total_answers = answer_human + answer_chatgpt


    for idx, answer in enumerate(total_answers):
        answer_type = "Human" if idx < len(answer_human) else "ChatGPT"
        btn = tk.Button(answer_frame, text=f"Answer {answer_type} {idx + 1}", command=lambda i=idx: answer_picked(i))
        btn.pack()
        text_widget = tk.Text(answer_frame, height=4, width=80)
        text_widget.pack()
        text_widget.insert(tk.END, answer)
        text_widget.config(state=tk.DISABLED)



root = tk.Tk()
root.title("GUI Reinforcement Learning")

current_question = 0
human_vs_chatgpt = {"human": 0, "chatgpt": 0}
date = load_data('chatgpt.json')


question_frame = tk.Frame(root)
question_frame.pack(pady=20)
question_info = tk.Label(question_frame, text="", wraplength=600, justify="left")
question_info.pack()


answer_frame = tk.Frame(root)
answer_frame.pack(padx=20)

display_qa()

root.mainloop()
