import tkinter as tk
import random
import os

def clear():
    """Clears the terminal screen based on the Operating System."""
    # 'nt' is Windows, 'posix' is macOS/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix System Failure")
        
        # Cross-platform Fullscreen
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.root.focus_set() # Ensures keys are captured on startup

        # --- Configuration ---
        self.MESSAGE = "SYSTEM FAILURE: REALITY NOT FOUND"
        self.FONT_SIZE = 16
        self.CHARS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ1234567890"
        
        # Colors
        self.COLOR_HEAD = "#FFFFFF"   # White
        self.COLOR_BRIGHT = "#2ECC71" # Bright Green
        self.COLOR_DIM = "#27AE60"    # Dim Green
        self.COLOR_DARK = "#145A32"   # Dark Green

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.root.update()
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

        # Grid setup based on font size
        self.columns_count = self.width // self.FONT_SIZE
        # [y_pos, speed_delay, trail_length]
        self.columns = [[random.randint(-self.height, 0), random.randint(10, 30), random.randint(10, 25)] 
                        for _ in range(self.columns_count)]

        # Bindings
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        self.animate()

    def animate(self):
        # Clear the canvas for the next frame
        self.canvas.delete("all")
        
        msg_y_idx = (self.height // self.FONT_SIZE) // 2
        msg_start_col = (self.columns_count // 2) - (len(self.MESSAGE) // 2)

        for x_idx, col in enumerate(self.columns):
            y, speed, length = col
            
            # Draw the trail
            for i in range(length):
                char_y_idx = (y // self.FONT_SIZE) - i
                draw_y = char_y_idx * self.FONT_SIZE
                draw_x = x_idx * self.FONT_SIZE

                if 0 <= draw_y < self.height:
                    # Message Logic
                    is_msg_area = (char_y_idx == msg_y_idx and msg_start_col <= x_idx < msg_start_col + len(self.MESSAGE))
                    
                    if is_msg_area:
                        char = self.MESSAGE[x_idx - msg_start_col]
                        color = self.COLOR_HEAD
                    else:
                        char = random.choice(self.CHARS)
                        # Gradient coloring
                        if i == 0: color = self.COLOR_HEAD
                        elif i < length * 0.4: color = self.COLOR_BRIGHT
                        else: color = self.COLOR_DARK

                    # Using "monospace" as it's the most compatible font alias
                    self.canvas.create_text(draw_x, draw_y, text=char, fill=color, 
                                            font=("monospace", self.FONT_SIZE, "bold"), anchor="nw")

            # Movement (adjusting speed logic for smoother delta)
            self.columns[x_idx][0] += speed

            # Reset column when it leaves screen
            if (y - (length * self.FONT_SIZE)) > self.height:
                self.columns[x_idx][0] = 0
                self.columns[x_idx][1] = random.randint(10, 30) # Randomize speed on reset

        # Schedule next frame
        self.root.after(50, self.animate)

if __name__ == "__main__":
    # First, clear the terminal
    clear()
    
    root = tk.Tk()
    app = MatrixApp(root)
    root.mainloop()
