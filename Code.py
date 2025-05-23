#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
import numpy as np
class CountHolesApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Count Holes")
        
        # initialize the checkerboard
        self.checkerboard = np.random.randint(0, 2, (10, 10)).tolist()
        
        # create the canvas
        self.canvas = tk.Canvas(self.master, width=500, height=500)
        self.canvas.pack()
        
        # update the canvas
        self.update_canvas()
        
        # create the count holes button
        self.btn_count_holes = tk.Button(self.master, text="Count Holes", font="bold, 10", command=self.count_holes, bg='lightblue')
        self.btn_count_holes.pack()
        
        # create the label to display the number of holes and white squares in each hole
        self.lbl_holes = tk.Label(self.master, text="")
        self.lbl_holes.pack()
    
    def update_canvas(self):
        # clear the canvas
        self.canvas.delete(tk.ALL)
        
        # draw the squares on the canvas
        for i in range(10):
            for j in range(10):
                x0 = j * 50
                y0 = i * 50
                x1 = x0 + 50
                y1 = y0 + 50
                if self.checkerboard[i][j] == 1:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
        
        # update the canvas
        self.canvas.update()
        
    def find_hole(self, i, j):
        hole = set()

        # initialize the stack for DFS
        stack = [(i, j)]

        # get the size of the checkerboard
        n = len(self.checkerboard)
        m = len(self.checkerboard[0])

        # perform DFS to find all squares in the hole
        while stack:
            x, y = stack.pop()

            # add the current square to the hole
            hole.add((x, y))

            # check the neighbors (up, down, left, right)
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for nx, ny in neighbors:
                if 0 <= nx < n and 0 <= ny < m and self.checkerboard[nx][ny] == 1 and (nx, ny) not in hole:
                    stack.append((nx, ny))

        return hole



    def count_holes(self):
        delay = 100 # Set the delay to 500 milliseconds
        holes = []
        colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'brown', 'pink', 'gray', 'cyan'] # Assign different colors to holes
        color_counts = {color: 0 for color in colors} # Initialize the color counts to zero
        for i in range(len(self.checkerboard)):
            for j in range(len(self.checkerboard[0])):
                if self.checkerboard[i][j] == 1:
                    in_a_hole = False
                    for hole in holes:
                        if (i, j) in hole:
                            in_a_hole = True
                            break
                    if in_a_hole:
                        continue
                    hole = self.find_hole(i, j)
                    if len(hole) > 0:
                        holes.append(hole)
                        # Get the index of the color to use for this hole
                        color_index = len(holes) - 1
                        if color_index < len(colors):
                            color = colors[color_index]
                        else:
                            # If there are more holes than available colors, repeat the colors
                            color = colors[color_index % len(colors)]
                        # Color the squares in the current hole
                        for x, y in hole:
                            x0 = y * 50
                            y0 = x * 50
                            x1 = x0 + 50
                            y1 = y0 + 50
                            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                            # Increment the color count
                            color_counts[color] += 1
        # Update the canvas
        self.canvas.update()
        # Update the label with the number of holes and color counts
        hole_count_str = "Number of holes: {}".format(len(holes))
        color_counts_str = "Color counts: "
        for color, count in color_counts.items():
            color_counts_str += "{}: {}, ".format(color, count)
        self.lbl_holes.configure(text=hole_count_str + "\n" + color_counts_str)


    

                        
root = tk.Tk()
app = CountHolesApp(root)
root.mainloop()

