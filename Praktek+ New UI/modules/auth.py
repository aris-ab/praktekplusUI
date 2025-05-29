# modules/auth.py - Enhanced Authentication module
import csv
import os
from colorama import Fore, Style
from .data_structures.linked_list import LinkedList
from .data_manager import read_csv, write_csv
from .utils import clear_screen, show_error, show_success, print_banner, get_input_with_prompt, EnhancedLoadingAnimation

def authenticate_user():
    """Authenticate a user with enhanced UI and return user type and ID."""
    clear_screen()
    print_banner("🔐 LOGIN SISTEM", "green")
    
    print(Fore.CYAN + "╔" + "═" * 50 + "╗")
    print(Fore.CYAN + "║" + " " * 50 + "║")
    print(Fore.CYAN + "║" + Fore.YELLOW + Style.BRIGHT + "         🏥 MASUK KE SISTEM PRAKTEK+ 🏥         " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 50 + "║")
    print(Fore.CYAN + "╚" + "═" * 50 + "╝")
    
    print(Fore.WHITE + "\n📝 Silakan masukkan kredensial Anda:")
    print(Fore.BLUE + "─" * 40)
    
    username = get_input_with_prompt("Username", "👤")
    password = get_input_with_prompt("Password", "🔑")
    
    if not username or not password:
        show_error("Username dan password harus diisi!")
        return None, None
    
    # Show loading animation
    loading = EnhancedLoadingAnimation("Memverifikasi kredensial", "dots")
    loading.start()
    
    # Check admin credentials
    admin_data = read_csv("data/admin.csv")
    for admin in admin_data:
        if admin['username'] == username and admin['password'] == password:
            loading.stop()
            print(Fore.GREEN + "\n✅ Login berhasil sebagai " + Fore.YELLOW + Style.BRIGHT + "ADMIN")
            print(Fore.CYAN + f"👋 Selamat datang, {admin['nama']}!")
            input(Fore.GREEN + "\n⏎ Tekan Enter untuk melanjutkan...")
            return "admin", admin['id']
    
    # Check doctor credentials
    doctor_data = read_csv("data/dokter.csv")
    for doctor in doctor_data:
        if doctor['username'] == username and doctor['password'] == password:
            loading.stop()
            print(Fore.GREEN + "\n✅ Login berhasil sebagai " + Fore.YELLOW + Style.BRIGHT + "DOKTER")
            print(Fore.CYAN + f"👋 Selamat datang, {doctor['nama']} - {doctor['spesialisasi']}")
            input(Fore.GREEN + "\n⏎ Tekan Enter untuk melanjutkan...")
            return "dokter", doctor['id']
    
    # Check patient credentials
    patient_data = read_csv("data/pasien.csv")
    for patient in patient_data:
        if patient['username'] == username and patient['password'] == password:
            loading.stop()
            print(Fore.GREEN + "\n✅ Login berhasil sebagai " + Fore.YELLOW + Style.BRIGHT + "PASIEN")
            print(Fore.CYAN + f"👋 Selamat datang, {patient['nama']}!")
            input(Fore.GREEN + "\n⏎ Tekan Enter untuk melanjutkan...")
            return "pasien", patient['id']
    
    loading.stop()
    print(Fore.RED + "\n❌ Login gagal!")
    print(Fore.YELLOW + "⚠️  Username atau password tidak ditemukan")
    print(Fore.WHITE + "\n💡 Tips:")
    print(Fore.WHITE + "   • Pastikan username dan password benar")
    print(Fore.WHITE + "   • Gunakan akun default untuk testing (ketik '?' di menu utama)")
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali...")
    
    return None, None

def register_patient():
    """Register a new patient with enhanced UI."""
    clear_screen()
    print_banner("👤 REGISTRASI PASIEN BARU", "yellow")
    
    print(Fore.CYAN + "╔" + "═" * 60 + "╗")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + "       🆕 DAFTARKAN AKUN PASIEN BARU 🆕           " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "╚" + "═" * 60 + "╝")
    
    print(Fore.WHITE + "\n📋 Silakan lengkapi data berikut:")
    print(Fore.BLUE + "─" * 50)
    
    name = get_input_with_prompt("Nama Lengkap", "👤")
    username = get_input_with_prompt("Username", "🆔")
    password = get_input_with_prompt("Password", "🔑")
    contact = get_input_with_prompt("Nomor Telepon", "📞")
    
    # Enhanced validation
    validation_errors = []
    
    if not name or len(name.strip()) < 2:
        validation_errors.append("Nama lengkap minimal 2 karakter")
    
    if not username or len(username.strip()) < 3:
        validation_errors.append("Username minimal 3 karakter")
        
    if not password or len(password) < 6:
        validation_errors.append("Password minimal 6 karakter")
        
    if not contact or len(contact.strip()) < 10:
        validation_errors.append("Nomor telepon minimal 10 digit")
    
    if validation_errors:
        print(Fore.RED + "\n❌ Terdapat kesalahan input:")
        for i, error in enumerate(validation_errors, 1):
            print(Fore.RED + f"   {i}. {error}")
        input(Fore.GREEN + "\n⏎ Tekan Enter untuk coba lagi...")
        return register_patient()  # Retry registration
    
    # Show loading animation
    loading = EnhancedLoadingAnimation("Memeriksa ketersediaan username", "dots")
    loading.start()
    
    # Check if username already exists
    patient_data = read_csv("data/pasien.csv")
    for patient in patient_data:
        if patient['username'].lower() == username.lower():
            loading.stop()
            show_error("Username sudah digunakan. Silakan pilih username lain.")
            return register_patient()  # Retry registration
    
    loading.stop()
    
    # Show confirmation
    print(Fore.YELLOW + "\n📋 Konfirmasi Data Registrasi:")
    print(Fore.CYAN + "┌─" + "─" * 40 + "┐")
    print(Fore.CYAN + f"│ Nama      : {Fore.WHITE}{name:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Username  : {Fore.WHITE}{username:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Password  : {Fore.WHITE}{'*' * len(password):<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Telepon   : {Fore.WHITE}{contact:<26}{Fore.CYAN} │")
    print(Fore.CYAN + "└─" + "─" * 40 + "┘")
    
    confirm = input(Fore.GREEN + "\n✅ Apakah data sudah benar? (y/n): " + Fore.WHITE).lower()
    
    if confirm != 'y':
        print(Fore.YELLOW + "📝 Silakan input ulang data Anda")
        input(Fore.GREEN + "⏎ Tekan Enter untuk melanjutkan...")
        return register_patient()
    
    loading = EnhancedLoadingAnimation("Menyimpan data registrasi", "bars")
    loading.start()
    
    # Generate new ID
    new_id = f"P{len(patient_data) + 1:03d}"
    
    # Add new patient
    new_patient = {
        'id': new_id,
        'nama': name.strip(),
        'username': username.strip(),
        'password': password,
        'kontak': contact.strip()
    }
    
    patient_data.append(new_patient)
    write_csv("data/pasien.csv", patient_data)
    
    loading.stop()
    
    # Enhanced success message
    print(Fore.GREEN + "\n🎉 " + Style.BRIGHT + "REGISTRASI BERHASIL!" + Style.RESET_ALL)
    print(Fore.CYAN + "╔" + "═" * 50 + "╗")
    print(Fore.CYAN + "║" + " " * 50 + "║")
    print(Fore.CYAN + "║ " + Fore.GREEN + "✅ Akun Anda telah berhasil dibuat!      " + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.YELLOW + f"🆔 ID Pasien: {new_id}                      " + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.YELLOW + f"👤 Username: {username}                    " + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "💡 Simpan informasi ini untuk login!     " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 50 + "║")
    print(Fore.CYAN + "╚" + "═" * 50 + "╝")
    
    print(Fore.CYAN + "\n🏥 Sekarang Anda dapat:")
    print(Fore.WHITE + "   • 👀 Melihat jadwal dokter")
    print(Fore.WHITE + "   • 📝 Mendaftar konsultasi")
    print(Fore.WHITE + "   • 📋 Melihat status pendaftaran")
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu utama...")