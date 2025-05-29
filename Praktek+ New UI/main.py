# main.py - Entry point for the application (Enhanced UI Version)
import os
import sys
from colorama import init, Fore, Back, Style
from modules.auth import authenticate_user
from modules.admin import admin_menu
from modules.doctor import doctor_menu
from modules.patient import patient_menu
from modules.data_manager import initialize_data
from modules.utils import clear_screen, show_breadcrumbs, show_help, print_banner, print_welcome_banner

init(autoreset=True)  # Initialize colorama with autoreset

def main_menu():
    """Display the enhanced main menu of the application."""
    clear_screen()
    
    # Enhanced welcome banner
    print_welcome_banner()
    
    # Enhanced menu design
    print(Fore.CYAN + "╔" + "═" * 68 + "╗")
    print(Fore.CYAN + "║" + " " * 68 + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + Style.BRIGHT + "                    🏥 MENU UTAMA PRAKTEK+ 🏥                    " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 68 + "║")
    print(Fore.CYAN + "╠" + "═" * 68 + "╣")
    print(Fore.CYAN + "║" + " " * 68 + "║")
    print(Fore.CYAN + "║  " + Fore.GREEN + "🔐 1." + Fore.YELLOW + " Login ke Sistem                                        " + Fore.CYAN + "║")
    print(Fore.CYAN + "║  " + Fore.GREEN + "👤 2." + Fore.YELLOW + " Registrasi Pasien Baru                                " + Fore.CYAN + "║")
    print(Fore.CYAN + "║  " + Fore.RED + "🚪 3." + Fore.YELLOW + " Keluar dari Aplikasi                                  " + Fore.CYAN + "║")
    print(Fore.CYAN + "║  " + Fore.BLUE + "❓ ?." + Fore.YELLOW + " Bantuan & Panduan                                     " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 68 + "║")
    print(Fore.CYAN + "╚" + "═" * 68 + "╝")
    
    # Enhanced input prompt
    print(Fore.WHITE + "\n┌─" + "─" * 20 + "┐")
    print(Fore.WHITE + "│ " + Fore.CYAN + "Masukkan Pilihan:" + Fore.WHITE + " │")
    print(Fore.WHITE + "└─" + "─" * 20 + "┘")
    choice = input(Fore.GREEN + "➤ " + Fore.WHITE)
    
    if choice == "1":
        user_type, user_id = authenticate_user()
        if user_type == "admin":
            admin_menu(user_id)
        elif user_type == "dokter":
            doctor_menu(user_id)
        elif user_type == "pasien":
            patient_menu(user_id)
        else:
            print(Fore.RED + "❌ Login gagal. Silakan coba lagi.")
            input(Fore.GREEN + "\n⏎ Tekan Enter untuk melanjutkan...")
            main_menu()
    elif choice == "2":
        from modules.auth import register_patient
        register_patient()
        main_menu()
    elif choice == "3":
        clear_screen()
        print_banner("TERIMA KASIH", "cyan")
        print(Fore.CYAN + "🙏 Terima kasih telah menggunakan Praktek+")
        print(Fore.YELLOW + "💝 Semoga hari Anda menyenangkan!")
        print(Fore.WHITE + "\n" + "═" * 50)
        sys.exit()
    elif choice == "?":
        show_help("main")
        main_menu()
    else:
        print(Fore.RED + "❌ Pilihan tidak valid. Silakan pilih 1, 2, 3, atau ?")
        input(Fore.GREEN + "\n⏎ Tekan Enter untuk melanjutkan...")
        main_menu()

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Initialize data if files don't exist
    initialize_data()
    
    try:
        while True:
            main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print(Fore.CYAN + "\n🙏 Keluar dari aplikasi. Terima kasih telah menggunakan Praktek+!")
        print(Fore.YELLOW + "💝 Sampai jumpa lagi!")
        sys.exit()