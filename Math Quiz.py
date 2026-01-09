import customtkinter as ctk
import random



# ===================== BASE SCENE =====================
class BaseScene:
    def __init__(self, container, app):
        self.container = container
        self.app = app


        self.frame = ctk.CTkFrame(self.container, fg_color="#2c1a47")  # CTkFrame

    def build(self):
        pass

    def show(self):
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

    def hide(self):
        self.frame.place_forget()


# ===================== SCENE MANAGER =====================
class SceneManager:
  def __init__(self, container, app):
    self.container = container
    self.app = app
    self.scenes = {}
    self.current_scene = None

  def register(self, name, scene_class):
    self.scenes[name] = scene_class

  def switch(self, name):
    if name in self.scenes:
      if self.current_scene:
        self.current_scene.hide()
      scene_class = self.scenes[name]
      self.current_scene = scene_class(self.container, self.app)
      self.current_scene.build()
      self.current_scene.show()
    else:
      print(f"Scene '{name}' is not registered.")


# ===================== SCENE ONE =====================
class SceneOne(BaseScene):
  def build(self):
    self.frame.configure(width=270, height=470, fg_color="#212022")
    self.frame.grid_columnconfigure(0, weight=1)
    self.frame.grid_columnconfigure(1, weight=1)
    self.frame.grid_columnconfigure(2, weight=1)

    self.frame.grid_rowconfigure(0, weight=1)
    self.frame.grid_rowconfigure(1, weight=1)
    self.frame.grid_rowconfigure(2, weight=1)
    self.frame.grid_rowconfigure(3, weight=1)
    self.frame.grid_rowconfigure(4, weight=1)
    self.frame.grid_rowconfigure(5, weight=1)
    self.frame.grid_propagate(False)
    
    
    if self.app.high_score > 0:
      hs_label = ctk.CTkLabel(
        self.frame,
        text=f"High Score: {self.app.high_score}",
        fg_color="#212022",
        text_color="gold",
        font=ctk.CTkFont(size=18, weight="bold")
        )
      hs_label.grid(row=0, column=1)
    
    btn_spdrn = ctk.CTkButton(
      self.frame,
      text="Speedrun: OFF" if not self.app.speedrun_mode else "Speedrun: ON",
      fg_color="#4d1486",
      command=self.toggle_speedrun
    )
    btn_spdrn.grid(row=4, column=1)

    btn_one_chance = ctk.CTkButton(
      self.frame,
      text="One Chance: OFF" if not self.app.one_chance else "One Chance: ON",
      fg_color="#4d1486",
      command=self.toggle_one_chance
    )
    btn_one_chance.grid(row=5, column=1)

    label = ctk.CTkLabel(
      self.frame,
      text="Main menu",
      fg_color="#212022",
      text_color="white",
      font=ctk.CTkFont(size=24, weight="bold")
      )
    label.grid(row=1, column=1)
    
    button = ctk.CTkButton(
      self.frame,
      text="Start",
      command=lambda: self.app.scene_manager.switch("scene2")
      )
    button.grid(row=2, column=1)

  def toggle_speedrun(self):
    self.app.speedrun_mode = not self.app.speedrun_mode
    btn_text = "Speedrun: ON" if self.app.speedrun_mode else "Speedrun: OFF"
    for widget in self.frame.winfo_children():
      if isinstance(widget, ctk.CTkButton) and "Speedrun" in widget.cget("text"):
        widget.configure(text=btn_text)
        break
  
  def toggle_one_chance(self):
    self.app.one_chance = not self.app.one_chance
    btn_text = "One Chance: ON" if self.app.one_chance else "One Chance: OFF"
    for widget in self.frame.winfo_children():
      if isinstance(widget, ctk.CTkButton) and "One Chance" in widget.cget("text"):
        widget.configure(text=btn_text)
        break


# ===================== SCENE TWO =====================





def generate_example(): 
  a = random.randint(1, 25) 
  b = random.randint(1, 25) 
  op = random.choice(["+", "-"]) 
  
  if op == "-": 
    if b > a: 
      a, b = b, a 
    correct = a - b 
  else: 
    correct = a + b 
  return a, b, op, correct

def generate_answers(correct):
  answers = [correct]

  while len(answers) < 4:
    wrong = correct + random.randint(-10, 10)
    if wrong != correct and wrong not in answers:
      answers.append(wrong)

  random.shuffle(answers)
  return answers



class SceneTwo(BaseScene):
  def build(self):
    self.input_locked = False
    
    self.app.bind("1", lambda e: self.check_answer(self.q1))
    self.app.bind("2", lambda e: self.check_answer(self.q2))
    self.app.bind("3", lambda e: self.check_answer(self.q3))
    self.app.bind("4", lambda e: self.check_answer(self.q4))
    
    self.frame.configure(width=270, height=470, fg_color="#212022")
    self.frame.pack_propagate(False)
    self.frame.grid_propagate(False)
    
    self.score = 0
    self.lbl_score = ctk.CTkLabel(
      self.frame,
      text=f"Score: {self.score}",
      text_color="white",
      font=ctk.CTkFont(size=24, weight="bold")
    )
    self.lbl_score.place(relx=0.32, rely=0.04, anchor="center")


        
    btn_exit = ctk.CTkButton(
      self.frame,
      text="Exit",
      fg_color="#4d1486",
      width=50, height=30,
      command= self.exit_to_menu
    )
    btn_exit.place(relx=0.85, rely=0.05, anchor="center")


    
    self.frame1 = ctk.CTkFrame(self.frame, fg_color="#3b3a3d", width=220, height=100)
    self.frame1.place(relx=0.5, rely=0.22, anchor="center")
    
    self.label = ctk.CTkLabel( 
      self.frame1,
        text="",
        text_color="white",
        font=ctk.CTkFont(size=24, weight="bold")
      )
    self.label.place(relx=0.5, rely=0.5, anchor="center")

    self.frameq1 = ctk.CTkFrame(self.frame, fg_color="#3b3a3d", width=125, height=125)
    self.frameq1.place(relx=0.28, rely=0.54, anchor="center")

    self.frameq2 = ctk.CTkFrame(self.frame, fg_color="#3b3a3d", width=125, height=125)
    self.frameq2.place(relx=0.72, rely=0.54, anchor="center")

    self.frameq3 = ctk.CTkFrame(self.frame, fg_color="#3b3a3d", width=125, height=125)
    self.frameq3.place(relx=0.28, rely=0.75, anchor="center")

    self.frameq4 = ctk.CTkFrame(self.frame, fg_color="#3b3a3d", width=125, height=125)
    self.frameq4.place(relx=0.72, rely=0.75, anchor="center")

    self.q1 = ctk.CTkButton(
      self.frameq1, 
      fg_color="green",
      hover_color="#115d11", 
      width=100, height=80, 
      command=lambda: self.check_answer(self.q1))
    self.q1.pack(pady=5, padx=5)

    self.q2 = ctk.CTkButton(
      self.frameq2, 
      fg_color="red", 
      hover_color="#6c1111",
      width=100, height=80, 
      command=lambda: self.check_answer(self.q2))
    self.q2.pack(pady=5, padx=5)

    self.q3 = ctk.CTkButton(
      self.frameq3, 
      fg_color="#b19818",
      hover_color="#7a6b0c",
      width=100, height=80, 
      command=lambda: self.check_answer(self.q3))
    self.q3.pack(pady=5, padx=5)

    self.q4 = ctk.CTkButton(
      self.frameq4, 
      fg_color="blue",
      hover_color="#0c3a7a",
      width=100, height=80, 
      command=lambda: self.check_answer(self.q4))
    self.q4.pack(pady=5, padx=5)

    


    self.load_new_example()
    
    
  def exit_to_menu(self):
    self.unbind_keys()
    self.update_high_score()
    self.app.scene_manager.switch("scene1")
    
  def unbind_keys(self):
    self.app.unbind("1")
    self.app.unbind("2")
    self.app.unbind("3")
    self.app.unbind("4")
    
  def update_high_score(self):
    if self.score > self.app.high_score:
      self.app.high_score = self.score

  def load_new_example(self):
    self.a, self.b, self.op, self.correct = generate_example()
    self.answers = generate_answers(self.correct)

    self.label.configure(text=f"{self.a} {self.op} {self.b} = ?")

    self.q1.configure(text=str(self.answers[0]))
    self.q2.configure(text=str(self.answers[1]))
    self.q3.configure(text=str(self.answers[2]))
    self.q4.configure(text=str(self.answers[3]))

  def check_answer(self, button):
    if self.input_locked:
        return
    self.input_locked = True
    self.disable_buttons()
    if int(button.cget("text")) == self.correct:
      self.show_result(True)
    else:
      self.show_result(False)

  def show_result(self, is_correct):
    delay1 = 100 if self.app.speedrun_mode else 600
    delay2 = 100 if self.app.speedrun_mode else 400
    delay = delay1 if is_correct else delay2
    if is_correct:
      self.label.configure(text="Correct!", text_color="#0F3B11")
      
      self.frame1.configure(fg_color="#2e7d32")
      self.frame1.after(delay, lambda: self.frame1.configure(fg_color="#3b3a3d"))
      
      self.score += 1
      
      self.lbl_score.configure(text=f"Score: {self.score}")

      self.frame.after(delay, self.reset_after_result)


    else:
      self.label.configure(text="Wrong!", text_color="#310606")
      
      self.frame1.configure(fg_color="#d32f2f")
      self.frame1.after(delay, lambda: self.frame1.configure(fg_color="#3b3a3d"))

      self.frame.after(delay, lambda: self.label.configure(text=f"{self.a} {self.op} {self.b} = ?", text_color="white"))
      if self.app.one_chance:
        self.score -= 1 if self.score > 0 else 0
        self.lbl_score.configure(text=f"Score: {self.score}")
        self.frame.after(delay, self.reset_after_result)
        
    self.frame.after(delay, self.unlock_input)

  def unlock_input(self):
    self.input_locked = False
    self.enable_buttons()

  def disable_buttons(self):
    self.q1.configure(state="disabled")
    self.q2.configure(state="disabled")
    self.q3.configure(state="disabled")
    self.q4.configure(state="disabled")

  def enable_buttons(self):
    self.q1.configure(state="normal")
    self.q2.configure(state="normal")
    self.q3.configure(state="normal")
    self.q4.configure(state="normal")

  def reset_after_result(self):
    self.label.configure(text_color="white")
    self.load_new_example()

  
    
# ===================== APP =====================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Math Quiz")
        self.geometry("300x500")
        self.configure(fg_color="black")
        self.resizable(False, False)

        self.high_score = 0
        self.speedrun_mode = False
        self.one_chance = False
        # контейнер для сцен (width/height задаём при создании)
        self.container = ctk.CTkFrame(self, fg_color="black", width=300, height=500)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # менеджер сцен
        self.scene_manager = SceneManager(self.container, self)

        # регистрация сцен
        self.scene_manager.register("scene1", SceneOne)
        self.scene_manager.register("scene2", SceneTwo)

        # стартовая сцена
        self.scene_manager.switch("scene1")
        



# ===================== RUN =====================
if __name__ == "__main__":
    app = App()
    app.mainloop()
