import tkinter as tk
from tkinter import messagebox
import random

class IslandCoinGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Island Coin Game")
        
        self.islands = [60, 18, 2, 18, 2]  # Center island has more coins
        self.players = ['red', 'yellow', 'blue', 'green']
        self.player_positions = [None] * 4
        self.active_players = set(range(4))
        self.human_player = 0  # The human controls the red player
        self.create_widgets()
        self.game_running = True

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg='lightblue')
        self.canvas.pack(padx=10, pady=10)
        
        # Draw islands
        self.island_positions = [(200, 200), (100, 100), (300, 100), (300, 300), (100, 300)]
        self.island_ids = []
        for i, (x, y) in enumerate(self.island_positions):
            island = self.canvas.create_oval(x-40, y-40, x+40, y+40, fill='sandy brown', outline='chocolate')
            text = self.canvas.create_text(x, y, text=str(self.islands[i]), font=('Arial', 12, 'bold'))
            self.island_ids.append((island, text))
        
        # Draw players
        player_positions = [(200, 50), (50, 200), (350, 200), (200, 350)]
        for i, (x, y) in enumerate(player_positions):
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=self.players[i], tags=f"player{i}")
        
        self.turn_label = tk.Label(self.master, text="Your turn (Red player)", font=('Arial', 12))
        self.turn_label.pack(pady=5)
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        if not self.game_running:
            return
        if self.human_player not in self.active_players:
            messagebox.showinfo("Game Over", "You have been eliminated!")
            return

        x, y = event.x, event.y
        for i, (island, text) in enumerate(self.island_ids):
            if self.canvas.coords(island)[0] < x < self.canvas.coords(island)[2] and \
               self.canvas.coords(island)[1] < y < self.canvas.coords(island)[3]:
                if self.is_valid_jump(self.human_player, i):
                    self.animate_jump(self.human_player, i)
                    self.check_conflicts()
                    if not self.check_game_over():
                        self.master.after(1000, self.ai_turns)  # AI turn delay
                break
        
    def is_valid_jump(self, player, target_island):
        current_position = self.player_positions[player]
        if current_position is None:
            return True  # First jump is always valid
        if target_island == current_position:
            return False  # Can't jump to the same island
        if current_position == 0:  # From the center island
            return target_island in [1, 2, 3, 4]
        if target_island == 0:  # To the center island
            return current_position in [1, 2, 3, 4]
        # Specific jump rules for edge islands
        if current_position == 1 and target_island in [0, 2]:
            return True
        if current_position == 2 and target_island in [0, 4]:
            return True
        if current_position == 3 and target_island in [0, 4]:
            return True
        if current_position == 4 and target_island in [0, 1]:
            return True
        return False

    def animate_jump(self, player, target_island):
        start_x, start_y = self.canvas.coords(f"player{player}")[0:2]
        end_x = (self.canvas.coords(self.island_ids[target_island][0])[0] + 
                 self.canvas.coords(self.island_ids[target_island][0])[2]) / 2 - 20
        end_y = (self.canvas.coords(self.island_ids[target_island][0])[1] + 
                 self.canvas.coords(self.island_ids[target_island][0])[3]) / 2 - 20
        
        frames = 20
        dx = (end_x - start_x) / frames
        dy = (end_y - start_y) / frames
        
        def animate_frame(frame):
            if frame < frames:
                self.canvas.move(f"player{player}", dx, dy)
                if frame < frames / 2:
                    self.canvas.move(f"player{player}", 0, -2)
                else:
                    self.canvas.move(f"player{player}", 0, 2)
                self.master.after(20, lambda: animate_frame(frame + 1))
            else:
                self.player_positions[player] = target_island
        
        animate_frame(0)

    def ai_turns(self):
        for ai_player in list(self.active_players - {self.human_player}):
            if ai_player in self.active_players:  # Check if still active
                available_islands = [i for i in range(5) if self.is_valid_jump(ai_player, i)]
                if available_islands:
                    chosen_island = random.choice(available_islands)
                    self.animate_jump(ai_player, chosen_island)
                    self.master.after(500, self.check_conflicts)  # Delay conflict check
                    if self.check_game_over():
                        break
        self.master.after(1000, self.update_turn_label)  # Update label after AI turns

    def check_conflicts(self):
        occupied_islands = {}
        players_to_eliminate = {}
        for player, position in enumerate(self.player_positions):
            if position is not None:
                if position in occupied_islands:
                    if position not in players_to_eliminate:
                        players_to_eliminate[position] = set()
                    players_to_eliminate[position].add(player)
                    players_to_eliminate[position].add(occupied_islands[position])
                else:
                    occupied_islands[position] = player
        
        for island, players in players_to_eliminate.items():
            self.eliminate_players(players, island)

    def eliminate_players(self, players, island):
        player_colors = [self.players[p] for p in players]
        message = f"Players {' and '.join(player_colors)} collided on island {island + 1} and were eliminated!"
        messagebox.showinfo("Players Eliminated", message)
        
        for player in players:
            if player in self.active_players:
                self.active_players.remove(player)
                self.player_positions[player] = None
                self.canvas.itemconfig(f"player{player}", state='hidden')

    def check_game_over(self):
        # Check for center island capture
        if 0 in self.player_positions:
            winner = self.player_positions.index(0)
            messagebox.showinfo("Game Over", f"Player {winner + 1} ({self.players[winner]}) wins by capturing the center!")
            self.game_running = False
            return True
        
        # Check if only one player remains
        if len(self.active_players) == 1:
            winner = list(self.active_players)[0]
            messagebox.showinfo("Game Over", f"Player {winner + 1} ({self.players[winner]}) wins! All others eliminated.")
            self.game_running = False
            return True
        
        return False

    def update_turn_label(self):
        if self.game_running:
            if self.human_player in self.active_players:
                self.turn_label.config(text="Your turn (Red player)")
            else:
                self.turn_label.config(text="You've been eliminated! Game continues...")
        else:
            self.turn_label.config(text="Game Over")

    def ai_game_loop(self):
        if self.game_running and self.human_player not in self.active_players:
            self.ai_turns()
            self.master.after(1500, self.ai_game_loop)  # Continue AI turns every 1.5 seconds

if __name__ == "__main__":
    root = tk.Tk()
    game = IslandCoinGame(root)
    root.mainloop()
