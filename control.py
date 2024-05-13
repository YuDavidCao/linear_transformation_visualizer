from tkinter import *
import time

VEC_MAX = 10
VEC_MIN = 0

class Control:

    def __init__(self, title, render = None) -> None:
        self.render = render
        self.root = Tk()
        self.root.attributes('-topmost', True)          
        self.height = self.root.winfo_screenheight()
        self.width  = self.root.winfo_screenwidth()
        self.cur_vector_counter = 1
        self.displayed_label = False
        # self.height = 400 # TODO
        # self.width  = 400 # TODO
        self.root.title(title)
        # self.root.geometry(f"{self.width}x{self.height}")
        self.run()
        self.root.mainloop() 

    def run(self):
        self.frames = [Frame(self.root)]
        self.frames[0].grid(row=0, column=0, sticky=N+S+E+W)
        self.gridMap = [[[0 for x in range(20)] for x in range(20)] for y in range(len(self.frames))]  
        self.varMap = [[[0 for x in range(20)] for x in range(20)] for y in range(len(self.frames))]
        self.addLabel(0,0,0, "Current transformation matrix:", cspan=3)
        self.addEntry(0,1,0,None, None, None, None,default="1")
        self.addEntry(0,1,1,None, None, None, None,default="0")
        self.addEntry(0,1,2,None, None, None, None,default="0")
        self.addEntry(0,2,0,None, None, None, None,default="0")
        self.addEntry(0,2,1,None, None, None, None,default="1")
        self.addEntry(0,2,2,None, None, None, None,default="0")
        self.addEntry(0,3,0,None, None, None, None,default="0")
        self.addEntry(0,3,1,None, None, None, None,default="0")
        self.addEntry(0,3,2,None, None, None, None,default="1")
        self.varMap[0][1][0].trace_add("write", lambda *args: self.modify_animation_matrix(1,0))
        self.varMap[0][1][1].trace_add("write", lambda *args: self.modify_animation_matrix(1,1))
        self.varMap[0][1][2].trace_add("write", lambda *args: self.modify_animation_matrix(1,2))
        self.varMap[0][2][0].trace_add("write", lambda *args: self.modify_animation_matrix(2,0))
        self.varMap[0][2][1].trace_add("write", lambda *args: self.modify_animation_matrix(2,1))
        self.varMap[0][2][2].trace_add("write", lambda *args: self.modify_animation_matrix(2,2))
        self.varMap[0][3][0].trace_add("write", lambda *args: self.modify_animation_matrix(3,0))
        self.varMap[0][3][1].trace_add("write", lambda *args: self.modify_animation_matrix(3,1))
        self.varMap[0][3][2].trace_add("write", lambda *args: self.modify_animation_matrix(3,2))
        self.addLabel(0,4,0, "Current animation duration:", cspan=3)
        self.addEntry(0,5,0,None, None, None, None,default="10", cspan=3)
        self.varMap[0][5][0].trace_add("write", lambda *args: self.update_animation_duration(5,0))
        self.addButton(0,6,0, 
                       "Hide coordinates" if self.render.setting["show_coordinates"] else "Show coordinates", 
                       command = lambda *arg: self.toggle_show_coordinate(), cspan=3
        )
        self.addButton(0,7,0, 
                       "Hide basis axis" if self.render.setting["show_basis_axis"] else "Show basis axis", 
                       command = lambda *arg: self.toggle_basis_axis(), cspan=3
        )      
        self.addButton(0,8,0, 
                       "Hide camera coordinate" if self.render.setting["show_camera_coordinate"] else "Show camera coordinate", 
                       command = lambda *arg: self.toggle_camera_coordinate(), cspan=3
        ) 
        if(self.render.setting["mode"] == "vector"):    
            self.addButton(0,9,0, 
                        "Change to square mode", 
                        command = lambda *arg: self.change_mode("square"), cspan=3
            )   
        elif (self.render.setting["mode"] == "square"):
            self.addButton(0,9,0, 
                        "Change to grid mode", 
                        command = lambda *arg: self.change_mode("grid"), cspan=3
            )
        elif (self.render.setting["mode"] == "grid"):
            self.addButton(0,9,0, 
                        "Change to vector mode", 
                        command = lambda *arg: self.change_mode("vector"), cspan=3
            )
        # self.addButton(0,9,0, 
        #                "Display square" if self.render.setting["mode"] == "vector" else "Display vector", 
        #                command = lambda *arg: self.toggle_object(), cspan=3
        # ) 
        self.addButton(0,10,0, 
                       "Reset transformation", 
                       command = lambda *arg: self.reset_transformation(), cspan=3
        )   
        self.addButton(0,11,0, 
                       "Hide vertices" if self.render.setting["show_vertices"] else "Show vertices", 
                       command = lambda *arg: self.toggle_vertices(), cspan=3
        )   
        self.addButton(0,12,0, 
                       "Not transpose" if self.render.setting["transpose"] else "Transpose", 
                       command = lambda *arg: self.toggle_transpose(), cspan=3
        )   
        self.addButton(0,13,0, 
                       "Not inverse" if self.render.setting["inverse"] else "Inverse",
                       command = lambda *arg: self.toggle_inverse(), cspan=3
        )   
        self.addButton(0,14,0, 
                       "Black background" if self.render.setting["bg_color"] == "white" else "White background",
                       command = lambda *arg: self.toggle_background(), cspan=3
        )
        self.addButton(0,15,0, 
                       "Hide animation" if self.render.setting["show_animation"] else "Display animation", 
                       command = lambda *arg: self.toggle_animation(), cspan=3
        )
        if(self.render.setting["mode"] == "vector"):
            self.addLabel(0,2,3,"x",)
            self.addLabel(0,2,4,"y",)
            self.addLabel(0,2,5,"z",)
            self.addButton(0,0,3, 
                        "Add a vector", 
                        command = lambda *arg: self.add_vector(), cspan=3
            )           
            self.addButton(0,1,3, 
                        "Delete a vector", 
                        command = lambda *arg: self.delete_vector(), cspan=3
            ) 
        if(self.render.setting["mode"] == "grid"):
            self.addLabel(0,0,3,"Grid size",cspan=3)
            self.addEntry(0,1,3,None, None, None, None,default=self.render.setting["grid_size"], cspan=3)
            self.varMap[0][1][3].trace_add("write", lambda *args: self.modify_grid_size(1,3))
            self.addLabel(0,2,3,"Grid gap",cspan=3)
            self.addEntry(0,3,3,None, None, None, None,default=self.render.setting["grid_gap"], cspan=3)
            self.varMap[0][3][3].trace_add("write", lambda *args: self.modify_grid_gap(3,3))
          
    def toggle_animation(self):
        self.render.setting["show_animation"] = not self.render.setting["show_animation"]
        self.refresh_widget(0,15,0)
        self.addButton(0,15,0, 
                       "Hide animation" if self.render.setting["show_animation"] else "Display animation", 
                       command = lambda *arg: self.toggle_animation(), cspan=3
        )
            
    def modify_grid_size(self, row, col):
        currentVar = self.varMap[0][row][col].get().strip()
        if("." in currentVar):
            return
        try:
            var = int(currentVar)
            if(var % 2 == 0):
                var += 1
            if(var < 1 or var > 11):
                return
            self.render.setting["grid_size"] = var
            self.render.change_object()
            self.render.change_axis()
        except Exception as e:
            print(e)
      
    def modify_grid_gap(self, row, col):
        currentVar = self.varMap[0][row][col].get().strip()
        if("." in currentVar):
            return
        try:
            var = int(currentVar)
            if(var < 1 or var > 10):
                return
            self.render.setting["grid_gap"] = var
            print(f"setting: {var}")
            self.render.change_object()
            self.render.change_axis()
        except Exception as e:
            print(e)
      
    def toggle_background(self):
        self.render.setting["bg_color"] = "black" if self.render.setting["bg_color"] == "white" else "white"
        self.refresh_widget(0,14,0)
        self.addButton(0,14,0,  "Black background" if self.render.setting["bg_color"] == "white" else "White background", lambda *arg: self.toggle_background(), cspan=3)

      
    def toggle_inverse(self):
        self.render.setting["inverse"] = not self.render.setting["inverse"]
        self.render.change_object()
        self.refresh_widget(0,13,0)
        self.addButton(0,13,0, "Not inverse" if self.render.setting["inverse"] else "Inverse", lambda *arg: self.toggle_inverse(), cspan=3)

    def toggle_transpose(self):
        self.render.setting["transpose"] = not self.render.setting["transpose"]
        self.render.change_object()
        self.refresh_widget(0,12,0)
        self.addButton(0,12,0, "Not transpose" if self.render.setting["transpose"] else "Transpose", lambda *arg: self.toggle_transpose(), cspan=3)
       
    def toggle_vertices(self):
        self.render.setting["show_vertices"] = not self.render.setting["show_vertices"]
        self.refresh_widget(0,11,0)
        self.addButton(0,11,0, "Hide vertices" if self.render.setting["show_vertices"] else "Show vertices", lambda *arg: self.toggle_vertices(), cspan=3)
       
    def display_label(self, text):
        self.addLabel(0,16,0,text, cspan=2)
        self.addButton(0,16,2, 
                        "Ok", 
                        command = lambda *arg: self.acknowledge_label()
            ) 
        self.displayed_label = True
        
    def acknowledge_label(self):
        if(self.displayed_label):
            self.refresh_widget(0,16,0)
            self.refresh_widget(0,16,2)
            self.displayed_label = False
       
    def edit_vector(self, row, col, debug_text = None):
        currentVar = self.varMap[0][2 + row][col].get().strip()
        if(currentVar!=""):
            try:
                self.render.vectors[row - 1][col-3] = float(currentVar)
                self.render.change_object()
            except Exception as e:
                print(e)  
       
    def add_vector(self):
        if(self.cur_vector_counter >= VEC_MAX):
            self.display_label("Max vector reached")
            return
        self.cur_vector_counter += 1
        # description: apparently if you just use self.cur_vector_counter in the lambda function, it will always use the last value of self.cur_vector_counter
        index = self.cur_vector_counter 
        self.addEntry(0, 2 + index,3,None, None, None, None,default="1")
        self.addEntry(0, 2 + index,4,None, None, None, None,default="1")
        self.addEntry(0, 2 + index,5,None, None, None, None,default="1")
        self.varMap[0][2 + index][3].trace_add("write", lambda *args: self.edit_vector(index,3))
        self.varMap[0][2 + index][4].trace_add("write", lambda *args: self.edit_vector(index,4))
        self.varMap[0][2 + index][5].trace_add("write", lambda *args: self.edit_vector(index,5))
        self.render.vectors.append([1,1,1,1])
        self.render.change_object()
        
    def delete_vector(self):
        if(self.cur_vector_counter == VEC_MIN):  
            self.display_label("No vector to delete")
            return
        index = self.cur_vector_counter
        self.refresh_widget(0, 2 + index,3)
        self.refresh_widget(0, 2 + index,4)
        self.refresh_widget(0, 2 + index,5)
        self.cur_vector_counter -= 1
        self.render.vectors.pop()
        self.render.change_object()

    def reset_transformation(self):
        for i in range(4):
            for j in range(4):
                if(i == j):
                    self.render.animation[i][j] = 1
                else:
                    self.render.animation[i][j] = 0
        self.refresh_widget(0,10,0)
        self.addButton(0,10,0,
                          "Reset transformation", 
                          command = lambda *arg: self.reset_transformation(), cspan=3
        )
        self.addEntry(0,1,0,None, None, None, None,default="1")
        self.addEntry(0,1,1,None, None, None, None,default="0")
        self.addEntry(0,1,2,None, None, None, None,default="0")
        self.addEntry(0,2,0,None, None, None, None,default="0")
        self.addEntry(0,2,1,None, None, None, None,default="1")
        self.addEntry(0,2,2,None, None, None, None,default="0")
        self.addEntry(0,3,0,None, None, None, None,default="0")
        self.addEntry(0,3,1,None, None, None, None,default="0")
        self.addEntry(0,3,2,None, None, None, None,default="1")
        self.varMap[0][1][0].trace_add("write", lambda *args: self.modify_animation_matrix(1,0))
        self.varMap[0][1][1].trace_add("write", lambda *args: self.modify_animation_matrix(1,1))
        self.varMap[0][1][2].trace_add("write", lambda *args: self.modify_animation_matrix(1,2))
        self.varMap[0][2][0].trace_add("write", lambda *args: self.modify_animation_matrix(2,0))
        self.varMap[0][2][1].trace_add("write", lambda *args: self.modify_animation_matrix(2,1))
        self.varMap[0][2][2].trace_add("write", lambda *args: self.modify_animation_matrix(2,2))
        self.varMap[0][3][0].trace_add("write", lambda *args: self.modify_animation_matrix(3,0))
        self.varMap[0][3][1].trace_add("write", lambda *args: self.modify_animation_matrix(3,1))
        self.varMap[0][3][2].trace_add("write", lambda *args: self.modify_animation_matrix(3,2))

    def change_mode(self, nextMode):
        self.render.setting["mode"] = nextMode
        if(nextMode == "vector"):
            self.addLabel(0,2,3,"x",)
            self.addLabel(0,2,4,"y",)
            self.addLabel(0,2,5,"z",)
            self.addButton(0,0,3, 
                        "Add a vector", 
                        command = lambda *arg: self.add_vector(), cspan=3
            )           
            self.addButton(0,1,3, 
                        "Delete a vector", 
                        command = lambda *arg: self.delete_vector(), cspan=3
            )  
            for i in range(len(self.render.vectors)):
                index = i + 1
                self.addEntry(0, 2 + index,3,None, None, None, None,default=f"{self.render.vectors[i][0]}")
                self.addEntry(0, 2 + index,4,None, None, None, None,default=f"{self.render.vectors[i][1]}")
                self.addEntry(0, 2 + index,5,None, None, None, None,default=f"{self.render.vectors[i][2]}")
                self.varMap[0][2 + index][3].trace_add("write", lambda *args: self.edit_vector(index,3))
                self.varMap[0][2 + index][4].trace_add("write", lambda *args: self.edit_vector(index,4))
                self.varMap[0][2 + index][5].trace_add("write", lambda *args: self.edit_vector(index,5))
        elif(nextMode == "square"):
            for i in range(len(self.render.vectors)):
                index = i + 1
                self.refresh_widget(0, 2 + index,3)
                self.refresh_widget(0, 2 + index,4)
                self.refresh_widget(0, 2 + index,5)
            self.refresh_widget(0,0,3)
            self.refresh_widget(0,1,3)
            self.refresh_widget(0,2,3)
            self.refresh_widget(0,2,4)
            self.refresh_widget(0,2,5)
        elif(nextMode == "grid"):
            self.addLabel(0,0,3,"Grid size",cspan=3)
            self.addEntry(0,1,3,None, None, None, None,default=self.render.setting["grid_size"], cspan=3)
            self.varMap[0][1][3].trace_add("write", lambda *args: self.modify_grid_size(1,3))
            self.addLabel(0,2,3,"Grid gap",cspan=3)
            self.addEntry(0,3,3,None, None, None, None,default=self.render.setting["grid_gap"], cspan=3)
            self.varMap[0][3][3].trace_add("write", lambda *args: self.modify_grid_gap(3,3))
        self.render.change_object()
        self.refresh_widget(0,9,0)
        if(nextMode == "vector"):
            self.addButton(0,9,0, 
                           "Change to square mode", 
                           command = lambda *arg: self.change_mode("square"), cspan=3
            )
        elif(nextMode == "square"):
            self.addButton(0,9,0, 
                           "Change to grid mode", 
                           command = lambda *arg: self.change_mode("grid"), cspan=3
            )
        elif(nextMode == "grid"):
            self.addButton(0,9,0, 
                           "Change to vector mode", 
                           command = lambda *arg: self.change_mode("vector"), cspan=3
            )

    def toggle_camera_coordinate(self):
        self.render.setting["show_camera_coordinate"] = not self.render.setting["show_camera_coordinate"]
        self.refresh_widget(0,8,0)
        self.addButton(0,8,0, 
                       "Hide camera coordinate" if self.render.setting["show_basis_axis"] else "Show camera coordinate", 
                       command = lambda *arg: self.toggle_camera_coordinate(), cspan=3
        ) 

    def toggle_basis_axis(self):
        self.render.setting["show_basis_axis"] = not self.render.setting["show_basis_axis"]
        self.refresh_widget(0,7,0)
        self.addButton(0,7,0, 
                       "Hide basis axis" if self.render.setting["show_basis_axis"] else "Show basis axis", 
                       command = lambda *arg: self.toggle_basis_axis(), cspan=3
        ) 

    def toggle_show_coordinate(self):
        self.render.setting["show_coordinates"] = not self.render.setting["show_coordinates"]
        self.refresh_widget(0,6,0)
        self.addButton(0,6,0, "Hide coordinates" if self.render.setting["show_coordinates"] else "Show coordinates", lambda *arg: self.toggle_show_coordinate(), cspan=3)

    def update_animation_duration(self, row, col): 
        currentVar = self.varMap[0][row][col].get().strip()
        if(currentVar!="" and currentVar != "0"):
            try:
                self.render.setting["animation_duration"] = float(currentVar) * 1000
            except Exception as e:
                print(e)

        if(currentVar!=""):
            try:
                self.render.vectors[row - 1][col-3] = float(currentVar)
                self.render.change_object()
            except Exception as e:
                print(e)  

    def modify_animation_matrix(self, row, col):
        currentVar = self.varMap[0][row][col].get().strip()
        if(currentVar!=""):
            try:
                self.render.animation[row-1][col] = float(currentVar)
            except Exception as e:
                print(e)

    def show_frame(self,frame):
        """raise the selected frame from self.frames"""
        self.frames[frame].tkraise()

    def refresh(original_function):
        """wrapper function for every "add" functions, clear the existing widget"""
        def wrapper_function(*args,**kwargs):
            self,frame,row,column = args[0:4]
            if  self.gridMap[frame][row][column]:
                self.gridMap[frame][row][column].grid_remove()
            if  self.varMap[frame][row][column]:
                self.varMap[frame][row][column] = 0
            self.gridMap[frame][row][column] = None
            original_function(*args,**kwargs)
        return wrapper_function  

    def refresh_widget(self,frame,row,column):
        """refresh selected tkinter widget"""
        if self.gridMap[frame][row][column]:
            self.gridMap[frame][row][column].grid_remove()
        self.gridMap[frame][row][column] = None  

    @refresh
    def addScale(self,frame,row,column,command,text = "",rspan = 1,cspan = 1, horizontal = False, f = 0, t = 100):
        if(horizontal):
            self.gridMap[frame][row][column] = Scale(self.frames[frame], orient=HORIZONTAL, from_=f, to=t, label=text, command=command)
        else:
            self.gridMap[frame][row][column] = Scale(self.frames[frame], from_=f, to=t, label=text, command=command)
        self.gridMap[frame][row][column].grid(row = row, column = column, padx = 2, pady = 2, sticky = NSEW, rowspan = rspan, columnspan = cspan)

    @refresh
    def addText(self,frame,row,column, width = 0, height = 0, rspan = 1, cspan = 1):
        """add a tkinter Text widget"""
        self.gridMap[frame][row][column] = Text(self.frames[frame])
        self.gridMap[frame][row][column].grid(row = row, column = column, padx = 2, pady = 2, sticky = NSEW, rowspan = rspan, columnspan = cspan)
        if width:
            self.gridMap[frame][row][column].config(width = width)
        if height:
            self.gridMap[frame][row][column].config(height = height)

    @refresh
    def addLabel(self,frame,row,column,text,cspan = 1,rspan = 1, img = None):
        """add a tkinter label"""
        self.gridMap[frame][row][column] = Label(self.frames[frame],text = text, image = img, compound = LEFT, )
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)
        
    @refresh
    def addButton(self,frame,row,column,text,command,cspan = 1,rspan = 1):
        """add a tkinter button"""
        self.gridMap[frame][row][column] = Button(self.frames[frame],text = text,command = command)
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)        

    @refresh
    def addonepbutton(self,frame,row,column,text,command,p1,cspan = 1,rspan = 1):
        """add a tkinter button with one parameter"""
        self.gridMap[frame][row][column] = Button(self.frames[frame],text = text, command = lambda:command(p1))
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)         

    @refresh
    def addtwopbutton(self,frame,row,column,text,command,p1,p2,cspan = 1,rspan = 1):
        """add a tkinter button with two parameter"""
        self.gridMap[frame][row][column] = Button(self.frames[frame],text = text,command = lambda:command(p1,p2))
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)         

    @refresh
    def addEntry(self,frame,row,column,key1,key2,command1,command2,cspan = 1,rspan = 1, default = "", width=1):
        """add a tkinter entry"""
        self.varMap[frame][row][column] = StringVar()
        self.gridMap[frame][row][column] = Entry(self.frames[frame], width=width, textvariable=self.varMap[frame][row][column])
        self.gridMap[frame][row][column].insert(END, default)
        if command1:
            self.gridMap[frame][row][column].bind(key1,command1)
        if command2:
            self.gridMap[frame][row][column].bind(key2,command2)
        self.gridMap[frame][row][column].grid(row = row, column = column, padx = 2,pady = 2, sticky=NSEW, columnspan = cspan, rowspan = rspan)    

    @refresh
    def addcombobox(self,frame,row,column,options,command): 
        """add a tkinter combobox, also generates a tkinter.StringVar() object"""
        self.varMap[frame][row][column] = StringVar()
        self.gridMap[frame][row][column] = ttk.ComboBox(self.frames[frame],values = options, variable=self.varMap[frame][row][column], command = command)
        self.gridMap[frame][row][column].grid(row = row, column = column, padx = 2,pady = 2, sticky=NSEW)  

    @refresh
    def addlistbox(self,frame,row,column, height = 10, rspan = 1, cspan = 1):
        """add a tkinter listbox"""
        self.gridMap[frame][row][column] = Listbox(self.frames[frame],height=height,yscrollcommand = self.gridMap[frame][row][column+1].set)
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2, pady = 2, sticky=NSEW, rowspan = rspan, columnspan = cspan)
        self.gridMap[frame][row][column].config(highlightbackground="#0b5162", highlightcolor="#0b5162", highlightthickness=2, relief="solid")

    @refresh
    def addscrollbar(self,frame,row,column, rspan = 1, cspan = 1):
        """add a tkinter scrollbar"""
        self.gridMap[frame][row][column] = Scrollbar(self.frames[frame])
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2, pady = 2, sticky=NSEW, rowspan = rspan, columnspan = cspan)

if __name__ == "__main__":
    Control("test")