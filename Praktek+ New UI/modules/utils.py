# modules/utils.py - Enhanced Visual Utilities
import os
import sys
import time
import threading
from colorama import Fore, Back, Style

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_banner():
    """Print enhanced welcome banner for the application."""
    print(Fore.CYAN + Style.BRIGHT + "╔" + "═" * 78 + "╗")
    print(Fore.CYAN + "║" + " " * 78 + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + "    ██████╗ ██████╗  █████╗ ██╗  ██╗████████╗███████╗██╗  ██╗   " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + "    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝╚══██╔══╝██╔════╝██║ ██╔╝   " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + "    ██████╔╝██████╔╝███████║█████╔╝    ██║   █████╗  █████╔╝    " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + "    ██╔═══╝ ██╔══██╗██╔══██║██╔═██╗    ██║   ██╔══╝  ██╔═██╗    " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + "    ██║     ██║  ██║██║  ██║██║  ██╗   ██║   ███████╗██║  ██╗   " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + "    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 78 + "║")
    print(Fore.CYAN + "║" + Fore.YELLOW + Style.BRIGHT + "                      🏥 SISTEM MANAJEMEN KLINIK 🏥                    " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + "                        📅 Kelola Jadwal dengan Mudah                     " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 78 + "║")
    print(Fore.CYAN + "╚" + "═" * 78 + "╝")
    print()

def print_banner(title, color="cyan"):
    """Print a decorative banner with title."""
    colors = {
        "cyan": Fore.CYAN,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "red": Fore.RED,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA
    }
    
    color_code = colors.get(color.lower(), Fore.CYAN)
    title_len = len(title)
    total_width = max(60, title_len + 20)
    
    print(color_code + "╔" + "═" * (total_width - 2) + "╗")
    print(color_code + "║" + " " * (total_width - 2) + "║")
    
    padding = (total_width - 2 - title_len) // 2
    print(color_code + "║" + " " * padding + Style.BRIGHT + title + Style.NORMAL + " " * (total_width - 2 - padding - title_len) + "║")
    
    print(color_code + "║" + " " * (total_width - 2) + "║")
    print(color_code + "╚" + "═" * (total_width - 2) + "╝")

def print_section_header(title, icon="📋"):
    """Print a section header with icon."""
    print(Fore.CYAN + "\n┌─" + "─" * (len(title) + 8) + "┐")
    print(Fore.CYAN + "│ " + icon + " " + Fore.YELLOW + Style.BRIGHT + title + Fore.CYAN + Style.RESET_ALL + " │")
    print(Fore.CYAN + "└─" + "─" * (len(title) + 8) + "┘")

def show_breadcrumbs(path):
    """Display enhanced navigation breadcrumbs."""
    print(Fore.WHITE + Style.DIM + "🏠 " + Fore.BLUE + " ▶ ".join(path))
    print(Fore.BLUE + "─" * 50)
    print()

def show_error(message):
    """Display an enhanced error message."""
    print(Fore.RED + "\n┌─" + "─" * (len(message) + 10) + "┐")
    print(Fore.RED + "│ ❌ ERROR: " + message + " │")
    print(Fore.RED + "└─" + "─" * (len(message) + 10) + "┘")
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk melanjutkan...")

def show_success(message):
    """Display an enhanced success message."""
    print(Fore.GREEN + "\n┌─" + "─" * (len(message) + 12) + "┐")
    print(Fore.GREEN + "│ ✅ SUKSES: " + message + " │")
    print(Fore.GREEN + "└─" + "─" * (len(message) + 12) + "┘")
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk melanjutkan...")

def show_info(message, icon="ℹ️"):
    """Display an enhanced info message."""
    print(Fore.BLUE + "\n┌─" + "─" * (len(message) + 8) + "┐")
    print(Fore.BLUE + "│ " + icon + " INFO: " + message + " │")
    print(Fore.BLUE + "└─" + "─" * (len(message) + 8) + "┘")

def print_menu_option(number, icon, text, color=Fore.YELLOW):
    """Print a formatted menu option."""
    print(Fore.CYAN + "║  " + Fore.GREEN + icon + f" {number}." + color + f" {text:<50}" + Fore.CYAN + " ║")

def print_data_table_header(title):
    """Print enhanced table header."""
    print(Fore.CYAN + Style.BRIGHT + "\n╔" + "═" * 100 + "╗")
    print(Fore.CYAN + "║" + " " * 100 + "║")
    
    padding = (100 - len(title)) // 2
    print(Fore.CYAN + "║" + " " * padding + Fore.YELLOW + Style.BRIGHT + title + " " * (100 - padding - len(title)) + Fore.CYAN + "║")
    
    print(Fore.CYAN + "║" + " " * 100 + "║")
    print(Fore.CYAN + "╚" + "═" * 100 + "╝")

def get_input_with_prompt(prompt, icon="➤"):
    """Get input with enhanced prompt styling."""
    print(Fore.WHITE + "\n┌─" + "─" * (len(prompt) + 4) + "┐")
    print(Fore.WHITE + "│ " + Fore.CYAN + prompt + ": " + Fore.WHITE + "│")
    print(Fore.WHITE + "└─" + "─" * (len(prompt) + 4) + "┘")
    return input(Fore.GREEN + icon + " " + Fore.WHITE)

def show_help(context):
    """Display enhanced help information based on context."""
    clear_screen()
    print_banner("BANTUAN & PANDUAN", "blue")
    
    if context == "main":
        print_section_header("Cara Menggunakan Praktek+", "📖")
        print(Fore.WHITE + "• " + Fore.YELLOW + "Gunakan angka untuk memilih menu")
        print(Fore.WHITE + "• " + Fore.YELLOW + "Tekan Enter untuk melanjutkan setelah melihat informasi")
        print(Fore.WHITE + "• " + Fore.YELLOW + "Untuk keluar dari aplikasi, pilih opsi 'Keluar' di menu utama")
        print(Fore.WHITE + "• " + Fore.YELLOW + "Ketik '?' pada menu mana pun untuk bantuan")
        
        print_section_header("Akun Default untuk Testing", "🔑")
        print(Fore.WHITE + "👨‍💼 " + Fore.GREEN + "Admin:")
        print(Fore.WHITE + "   Username: " + Fore.CYAN + "admin")
        print(Fore.WHITE + "   Password: " + Fore.CYAN + "admin123")
        
        print(Fore.WHITE + "\n👩‍⚕️ " + Fore.GREEN + "Dokter:")
        print(Fore.WHITE + "   Username: " + Fore.CYAN + "drandi, drbudi, drcitra, drdewi")
        print(Fore.WHITE + "   Password: " + Fore.CYAN + "doctor123")
        
        print(Fore.WHITE + "\n👤 " + Fore.GREEN + "Pasien:")
        print(Fore.WHITE + "   Username: " + Fore.CYAN + "pasien")
        print(Fore.WHITE + "   Password: " + Fore.CYAN + "pasien123")
    
    elif context == "admin":
        print_section_header("Panduan Menu Admin", "👨‍💼")
        print(Fore.WHITE + "📅 " + Fore.YELLOW + "Lihat Semua Jadwal: " + Fore.WHITE + "Melihat semua jadwal dokter yang terdaftar")
        print(Fore.WHITE + "➕ " + Fore.YELLOW + "Tambah Jadwal: " + Fore.WHITE + "Menambahkan jadwal praktik baru untuk dokter")
        print(Fore.WHITE + "✏️ " + Fore.YELLOW + "Edit Jadwal: " + Fore.WHITE + "Mengubah jadwal yang sudah ada")
        print(Fore.WHITE + "🗑️ " + Fore.YELLOW + "Hapus Jadwal: " + Fore.WHITE + "Menghapus jadwal yang sudah tidak diperlukan")
        print(Fore.WHITE + "👥 " + Fore.YELLOW + "Lihat Data Pasien: " + Fore.WHITE + "Melihat semua pasien yang terdaftar")
        print(Fore.WHITE + "📝 " + Fore.YELLOW + "Lihat Pendaftaran: " + Fore.WHITE + "Melihat semua pendaftaran konsultasi")
        print(Fore.WHITE + "📊 " + Fore.YELLOW + "Lihat Statistik: " + Fore.WHITE + "Melihat statistik dan analisis klinik")
    
    elif context == "doctor":
        print_section_header("Panduan Menu Dokter", "👩‍⚕️")
        print(Fore.WHITE + "📅 " + Fore.YELLOW + "Lihat Jadwal Praktik: " + Fore.WHITE + "Melihat jadwal praktik Anda")
        print(Fore.WHITE + "➕ " + Fore.YELLOW + "Tambah Jadwal: " + Fore.WHITE + "Menambahkan jadwal praktik baru")
        print(Fore.WHITE + "✏️ " + Fore.YELLOW + "Edit Jadwal: " + Fore.WHITE + "Mengubah jadwal yang sudah ada")
        print(Fore.WHITE + "👥 " + Fore.YELLOW + "Lihat Pasien Terdaftar: " + Fore.WHITE + "Melihat pasien yang terdaftar pada jadwal Anda")
    
    elif context == "patient":
        print_section_header("Panduan Menu Pasien", "👤")
        print(Fore.WHITE + "📅 " + Fore.YELLOW + "Lihat Jadwal Dokter: " + Fore.WHITE + "Melihat semua jadwal dokter yang tersedia")
        print(Fore.WHITE + "🔍 " + Fore.YELLOW + "Cari Jadwal Dokter: " + Fore.WHITE + "Mencari jadwal berdasarkan nama dokter/spesialisasi/hari")
        print(Fore.WHITE + "📝 " + Fore.YELLOW + "Mendaftar Konsultasi: " + Fore.WHITE + "Mendaftar untuk konsultasi dokter")
        print(Fore.WHITE + "🔄 " + Fore.YELLOW + "Mengajukan Perubahan Jadwal: " + Fore.WHITE + "Mengubah atau membatalkan pendaftaran")
        print(Fore.WHITE + "📋 " + Fore.YELLOW + "Lihat Status Pendaftaran: " + Fore.WHITE + "Melihat status pendaftaran Anda")
    
    print(Fore.CYAN + "\n" + "═" * 80)
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali...")

class EnhancedLoadingAnimation:
    def __init__(self, message="Loading...", style="dots"):
        self.message = message
        self.is_running = False
        self.animation_thread = None
        self.style = style
    
    def start(self):
        self.is_running = True
        self.animation_thread = threading.Thread(target=self._animate)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def stop(self):
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join()
        # Clear the loading line
        sys.stdout.write("\r" + " " * (len(self.message) + 15) + "\r")
        sys.stdout.flush()
    
    def _animate(self):
        if self.style == "dots":
            chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        elif self.style == "bars":
            chars = ["▁", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃"]
        else:
            chars = ["◐", "◓", "◑", "◒"]
        
        idx = 0
        while self.is_running:
            sys.stdout.write(f"\r{Fore.YELLOW}🔄 {self.message} {Fore.CYAN}{chars[idx % len(chars)]}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)

# Alias for backward compatibility
LoadingAnimation = EnhancedLoadingAnimation

def show_status_indicator(status):
    """Show colored status indicator."""
    if status.lower() == "terdaftar":
        return Fore.GREEN + "✅ " + status + Style.RESET_ALL
    elif status.lower() == "dibatalkan":
        return Fore.RED + "❌ " + status + Style.RESET_ALL
    elif status.lower() == "selesai":
        return Fore.BLUE + "✔️ " + status + Style.RESET_ALL
    else:
        return Fore.YELLOW + "⏳ " + status + Style.RESET_ALL

def print_separator(char="═", width=80, color=Fore.CYAN):
    """Print a separator line."""
    print(color + char * width)

def show_waiting_message(message="Silakan tunggu...", duration=1):
    """Show a temporary waiting message."""
    print(Fore.YELLOW + "⏳ " + message)
    time.sleep(duration)
    
def print_statistics_box(title, value, icon="📊", color=Fore.CYAN):
    """Print a statistics box."""
    print(color + "┌─────────────────┐")
    print(color + f"│ {icon} {title:<12} │")
    print(color + f"│ {Fore.WHITE + Style.BRIGHT}{str(value):>15}{color} │")
    print(color + "└─────────────────┘")