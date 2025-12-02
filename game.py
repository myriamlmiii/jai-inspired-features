
"""
Beautiful Memory Hunt Game - Separate Window
Real-time metrics with colors
"""

import sys
import random
import time
import csv
from pathlib import Path

sys.path.insert(0, 'src')
from feature1_memory.tracker import MemoryTracker

# ANSI color codes
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BG_BLACK = '\033[40m'
    BOLD = '\033[1m'


class BeautifulGame:
    def __init__(self):
        self.tracker = MemoryTracker()
        self.player_x = 0
        self.player_y = 0
        self.score = 0
        self.moves = 0
        self.collectibles = []
        self.particles = []
        self.frame = 0
        
    def clear_screen(self):
        """Clear terminal"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def setup(self):
        """Initialize game"""
        self.tracker.track(self)
        
        # Spawn collectibles in a circle pattern
        import math
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            c = {
                'x': int(4 * math.cos(angle)),
                'y': int(4 * math.sin(angle)),
                'active': True,
                'data': list(range(100))
            }
            self.collectibles.append(c)
            self.tracker.track(c)
    
    def render(self):
        """Beautiful rendering with colors"""
        self.clear_screen()
        
        # Header with colors
        print(Colors.CYAN + Colors.BOLD + "="*70)
        print(f"{'MEMORY HUNT GAME':^70}")
        print("="*70 + Colors.RESET)
        print()
        print(f"{Colors.YELLOW}Score: {Colors.WHITE}{self.score:3d}  {Colors.YELLOW}|  Moves: {Colors.WHITE}{self.moves:3d}  {Colors.YELLOW}|  Frame: {Colors.WHITE}{self.frame:3d}{Colors.RESET}")
        print(Colors.CYAN + "-"*70 + Colors.RESET)
        print()
        
        # Draw beautiful map with colors
        for y in range(-6, 7):
            line = "  "
            for x in range(-6, 7):
                if x == self.player_x and y == self.player_y:
                    # Player in green
                    line += Colors.GREEN + Colors.BOLD + "P " + Colors.RESET
                elif any(c['x']==x and c['y']==y and c['active'] for c in self.collectibles):
                    # Collectibles in yellow
                    line += Colors.YELLOW + Colors.BOLD + "◆ " + Colors.RESET
                elif any(abs(p['x']-x)<1 and abs(p['y']-y)<1 for p in self.particles):
                    # Particles in magenta
                    line += Colors.MAGENTA + "* " + Colors.RESET
                else:
                    # Empty space
                    line += Colors.BLUE + "· " + Colors.RESET
            print(line)
        
        # Metrics box with colors
        print()
        print(Colors.CYAN + "-"*70 + Colors.RESET)
        print(Colors.WHITE + Colors.BOLD + "  REAL-TIME METRICS:" + Colors.RESET)
        print(Colors.CYAN + "-"*70 + Colors.RESET)
        
        metrics = self.tracker.get_metrics()
        stats = metrics['current_stats']
        
        memory_kb = stats['total_bytes'] / 1024
        memory_bar = "█" * int(memory_kb / 10)
        
        print(f"  {Colors.YELLOW}Memory Usage:{Colors.RESET}    {Colors.RED}{memory_kb:6.1f} KB {Colors.RESET} {memory_bar}")
        print(f"  {Colors.YELLOW}Objects Tracked:{Colors.RESET} {Colors.GREEN}{stats['count']:4d}{Colors.RESET}")
        print(f"  {Colors.YELLOW}Particles:{Colors.RESET}       {Colors.MAGENTA}{len(self.particles):4d}{Colors.RESET}")
        
        print(Colors.CYAN + "-"*70 + Colors.RESET)
        print(f"\n  {Colors.WHITE}Controls: {Colors.GREEN}w{Colors.WHITE}=up {Colors.GREEN}s{Colors.WHITE}=down {Colors.GREEN}a{Colors.WHITE}=left {Colors.GREEN}d{Colors.WHITE}=right {Colors.RED}q{Colors.WHITE}=quit{Colors.RESET}")
        print(Colors.CYAN + "="*70 + Colors.RESET)
    
    def move(self, direction):
        """Move player"""
        if direction == 'w':
            self.player_y = max(-6, self.player_y - 1)
        elif direction == 's':
            self.player_y = min(6, self.player_y + 1)
        elif direction == 'a':
            self.player_x = max(-6, self.player_x - 1)
        elif direction == 'd':
            self.player_x = min(6, self.player_x + 1)
        
        self.moves += 1
        
        # Check collection
        for c in self.collectibles:
            if c['active'] and c['x'] == self.player_x and c['y'] == self.player_y:
                c['active'] = False
                self.score += 10
                
                # Spawn particles
                for _ in range(30):
                    p = {
                        'x': self.player_x + random.uniform(-1, 1),
                        'y': self.player_y + random.uniform(-1, 1),
                        'life': 1.0
                    }
                    self.particles.append(p)
                    self.tracker.track(p)
        
        # Update particles
        self.particles = [p for p in self.particles if p['life'] > 0]
        for p in self.particles:
            p['life'] -= 0.15
        
        self.frame += 1
        self.tracker.next_frame()
    
    def play(self):
        """Main game loop"""
        self.clear_screen()
        print(Colors.CYAN + Colors.BOLD + "\n" + "="*70)
        print(f"{'MEMORY HUNT - JAI DEBUGGER DEMO':^70}")
        print("="*70 + Colors.RESET)
        print(f"\n{Colors.YELLOW}  Goal:{Colors.RESET} Collect all diamonds (◆) while watching memory grow!")
        print(f"{Colors.YELLOW}  Legend:{Colors.RESET}")
        print(f"    {Colors.GREEN}P{Colors.RESET} = You (Player)")
        print(f"    {Colors.YELLOW}◆{Colors.RESET} = Diamond (Collectible)")
        print(f"    {Colors.MAGENTA}*{Colors.RESET} = Particle Effect")
        print(f"\n{Colors.WHITE}  Press ENTER to start...{Colors.RESET}")
        input()
        
        self.setup()
        self.render()
        
        while True:
            cmd = input(f"\n  {Colors.GREEN}>{Colors.RESET} ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd in ['w', 'a', 's', 'd']:
                self.move(cmd)
                self.render()
                
                if all(not c['active'] for c in self.collectibles):
                    print(f"\n{Colors.GREEN + Colors.BOLD}  YOU WON! All diamonds collected!{Colors.RESET}\n")
                    break
        
        self.save_metrics()
    
    def save_metrics(self):
        """Save game metrics"""
        Path("outputs/metrics").mkdir(parents=True, exist_ok=True)
        
        metrics = self.tracker.get_metrics()
        with open('outputs/metrics/game_metrics.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['frame', 'allocations', 'bytes'])
            writer.writeheader()
            writer.writerows(metrics['frames'])
        
        print(f"\n{Colors.YELLOW}Metrics saved:{Colors.RESET} outputs/metrics/game_metrics.csv")
        print(f"{Colors.YELLOW}Final Score:{Colors.RESET} {self.score}")
        print(f"{Colors.YELLOW}Total Moves:{Colors.RESET} {self.moves}\n")


if __name__ == "__main__":
    game = BeautifulGame()
    game.play()
