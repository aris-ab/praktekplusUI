# modules/patient.py - Enhanced Patient functionality
import os
from datetime import datetime, timedelta
from tabulate import tabulate
from colorama import Fore, Style
from .data_manager import read_csv, write_csv, get_doctor_name
from .data_structures.queue import Queue
from .data_structures.bst import BST
from .utils import (clear_screen, show_breadcrumbs, show_error, show_success, show_help, 
                   EnhancedLoadingAnimation, print_banner, get_input_with_prompt, 
                   print_data_table_header, print_section_header)

def patient_menu(patient_id):
    """Display enhanced patient menu and handle patient actions."""
    patient_data = None
    patients = read_csv("data/pasien.csv")
    for patient in patients:
        if patient['id'] == patient_id:
            patient_data = patient
            break
    
    if not patient_data:
        show_error("Data pasien tidak ditemukan.")
        return
    
    while True:
        clear_screen()
        show_breadcrumbs(["🏠 Main Menu", "👤 Patient Dashboard"])
        
        # Enhanced patient header
        print(Fore.CYAN + "╔" + "═" * 80 + "╗")
        print(Fore.CYAN + "║" + " " * 80 + "║")
        print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + f"           👤 DASHBOARD PASIEN - {patient_data['nama']} 👤           ".center(80) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + "                    🏥 Kelola Konsultasi & Jadwal Anda 🏥                   " + "║")
        print(Fore.CYAN + "║" + " " * 80 + "║")
        print(Fore.CYAN + "╠" + "═" * 80 + "╣")
        
        # Enhanced menu options
        print(Fore.CYAN + "║  " + Fore.GREEN + "📅 1." + Fore.YELLOW + " Lihat Jadwal Dokter Tersedia                                 " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "🔍 2." + Fore.YELLOW + " Cari Jadwal Dokter (Nama/Spesialisasi/Hari)                 " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "📝 3." + Fore.YELLOW + " Mendaftar Konsultasi Dokter                                  " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "🔄 4." + Fore.YELLOW + " Mengajukan Perubahan Jadwal                                  " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "📋 5." + Fore.YELLOW + " Lihat Status Pendaftaran Saya                               " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.RED + "🚪 6." + Fore.YELLOW + " Logout dari Dashboard                                        " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.BLUE + "❓ ?." + Fore.YELLOW + " Bantuan & Panduan Pasien                                     " + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + " " * 80 + "║")
        print(Fore.CYAN + "╚" + "═" * 80 + "╝")
        
        # Show patient info summary
        registrations = read_csv("data/pendaftaran.csv")
        patient_regs = [r for r in registrations if r['pasien_id'] == patient_id]
        active_regs = [r for r in patient_regs if r['status'] != 'Dibatalkan']
        
        print(Fore.CYAN + "\n📊 Ringkasan Akun Anda:")
        print(Fore.WHITE + f"   • ID Pasien: {Fore.YELLOW}{patient_data['id']}")
        print(Fore.WHITE + f"   • Kontak: {Fore.YELLOW}{patient_data['kontak']}")
        print(Fore.WHITE + f"   • Pendaftaran Aktif: {Fore.GREEN}{len(active_regs)}")
        print(Fore.WHITE + f"   • Total Riwayat: {Fore.CYAN}{len(patient_regs)}")
        
        choice = input(Fore.GREEN + "\n➤ Pilihan Anda: " + Fore.WHITE)
        
        if choice == "1":
            view_doctor_schedules()
        elif choice == "2":
            search_doctor_schedules()
        elif choice == "3":
            register_consultation(patient_id)
        elif choice == "4":
            request_schedule_change(patient_id)
        elif choice == "5":
            view_registration_status(patient_id)
        elif choice == "6":
            print(Fore.CYAN + "👋 Logout berhasil. Semoga lekas sembuh!")
            break
        elif choice == "?":
            show_help("patient")
        else:
            show_error("Pilihan tidak valid. Silakan pilih 1-6 atau ?")

def view_doctor_schedules():
    """View all available doctor schedules with enhanced display."""
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👤 Pasien", "📅 Lihat Jadwal"])
    
    print_data_table_header("📅 JADWAL PRAKTIK DOKTER TERSEDIA 📅")
    
    loading = EnhancedLoadingAnimation("Memuat jadwal dokter tersedia", "dots")
    loading.start()
    
    schedules = read_csv("data/jadwal_dokter.csv")
    doctors = read_csv("data/dokter.csv")
    registrations = read_csv("data/pendaftaran.csv")
    
    # Create doctor dictionary for quick lookup
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = {
            "nama": doctor['nama'], 
            "spesialisasi": doctor['spesialisasi']
        }
    
    loading.stop()
    
    if not schedules:
        print(Fore.YELLOW + "⚠️  Tidak ada jadwal dokter yang tersedia.")
        print(Fore.WHITE + "💡 Silakan hubungi administrasi klinik.")
    else:
        # Enhanced display with availability status
        table_data = []
        for i, schedule in enumerate(schedules, 1):
            doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
            
            # Calculate availability
            registered_count = len([r for r in registrations 
                                  if r['jadwal_id'] == schedule['id'] and r['status'] != 'Dibatalkan'])
            quota = int(schedule['kuota'])
            available = quota - registered_count
            
            # Availability status with colors
            if available <= 0:
                availability_status = Fore.RED + "❌ Penuh" + Style.RESET_ALL
                available_text = Fore.RED + "0" + Style.RESET_ALL
            elif available <= 2:
                availability_status = Fore.YELLOW + "⚠️ Terbatas" + Style.RESET_ALL
                available_text = Fore.YELLOW + str(available) + Style.RESET_ALL
            else:
                availability_status = Fore.GREEN + "✅ Tersedia" + Style.RESET_ALL
                available_text = Fore.GREEN + str(available) + Style.RESET_ALL
            
            table_data.append([
                Fore.CYAN + str(i) + Style.RESET_ALL,
                Fore.GREEN + schedule['id'] + Style.RESET_ALL,
                Fore.YELLOW + doctor_info['nama'] + Style.RESET_ALL,
                Fore.MAGENTA + doctor_info['spesialisasi'] + Style.RESET_ALL,
                Fore.WHITE + schedule['hari'] + Style.RESET_ALL,
                Fore.CYAN + f"{schedule['jam_mulai']}-{schedule['jam_selesai']}" + Style.RESET_ALL,
                available_text + "/" + Fore.BLUE + str(quota) + Style.RESET_ALL,
                availability_status
            ])
        
        headers = [
            Fore.BLUE + Style.BRIGHT + "No." + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "ID" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Dokter" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Spesialisasi" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Hari" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Waktu" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Sisa/Total" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Status" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        # Summary statistics
        total_slots = sum(int(s['kuota']) for s in schedules)
        total_registered = len([r for r in registrations if r['status'] != 'Dibatalkan'])
        available_slots = total_slots - total_registered
        
        print(Fore.CYAN + f"\n📊 Ringkasan Ketersediaan:")
        print(Fore.WHITE + f"   • Total Slot: {Fore.BLUE}{total_slots}")
        print(Fore.WHITE + f"   • Terisi: {Fore.YELLOW}{total_registered}")
        print(Fore.WHITE + f"   • Tersedia: {Fore.GREEN}{available_slots}")
        
        utilization = (total_registered / total_slots * 100) if total_slots > 0 else 0
        print(Fore.WHITE + f"   • Utilisasi: {Fore.MAGENTA}{utilization:.1f}%")
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")

def search_doctor_schedules():
    """Search for doctor schedules with enhanced search options and UI."""
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👤 Pasien", "🔍 Cari Jadwal"])
    print_banner("🔍 PENCARIAN JADWAL DOKTER", "blue")
    
    print(Fore.CYAN + "╔" + "═" * 60 + "╗")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "║" + Fore.YELLOW + Style.BRIGHT + "               🔎 PILIH KRITERIA PENCARIAN               " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "╠" + "═" * 60 + "╣")
    print(Fore.CYAN + "║  " + Fore.GREEN + "👨‍⚕️ 1." + Fore.YELLOW + " Cari berdasarkan Nama Dokter                   " + Fore.CYAN + "║")
    print(Fore.CYAN + "║  " + Fore.GREEN + "🏥 2." + Fore.YELLOW + " Cari berdasarkan Spesialisasi                  " + Fore.CYAN + "║")
    print(Fore.CYAN + "║  " + Fore.GREEN + "📅 3." + Fore.YELLOW + " Cari berdasarkan Hari Praktik                  " + Fore.CYAN + "║")
    print(Fore.CYAN + "║  " + Fore.RED + "🔙 4." + Fore.YELLOW + " Kembali ke Menu Utama                          " + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "╚" + "═" * 60 + "╝")
    
    choice = input(Fore.GREEN + "\n🔍 Pilihan pencarian: " + Fore.WHITE)
    
    if choice not in ["1", "2", "3"]:
        return
    
    loading = EnhancedLoadingAnimation("Menyiapkan data untuk pencarian", "dots")
    loading.start()
    
    schedules = read_csv("data/jadwal_dokter.csv")
    doctors = read_csv("data/dokter.csv")
    registrations = read_csv("data/pendaftaran.csv")
    
    # Create doctor dictionary for quick lookup
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = {
            "nama": doctor['nama'], 
            "spesialisasi": doctor['spesialisasi']
        }
    
    results = []
    loading.stop()
    
    if choice == "1":
        print(Fore.YELLOW + "\n👨‍⚕️ Daftar Dokter Tersedia:")
        available_doctors = list(set([doctor_dict[s['dokter_id']]['nama'] 
                                    for s in schedules if s['dokter_id'] in doctor_dict]))
        
        for i, doc_name in enumerate(sorted(available_doctors), 1):
            print(Fore.WHITE + f"   {i}. {Fore.GREEN}{doc_name}")
        
        search_key = get_input_with_prompt("Nama dokter (atau sebagian nama)", "👨‍⚕️").lower()
        
        if not search_key:
            show_error("Nama dokter harus diisi.")
            return
        
        loading = EnhancedLoadingAnimation("Mencari berdasarkan nama dokter", "dots")
        loading.start()
        
        for schedule in schedules:
            doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasI": "Unknown"})
            if search_key in doctor_info['nama'].lower():
                results.append((schedule, doctor_info))
        
        loading.stop()
    
    elif choice == "2":
        available_specialties = list(set([doctor_dict[s['dokter_id']]['spesialisasi'] 
                                        for s in schedules if s['dokter_id'] in doctor_dict]))
        
        print(Fore.YELLOW + "\n🏥 Spesialisasi Tersedia:")
        for i, specialty in enumerate(sorted(available_specialties), 1):
            print(Fore.WHITE + f"   {i}. {Fore.MAGENTA}{specialty}")
        
        search_key = get_input_with_prompt("Spesialisasi (atau sebagian)", "🏥").lower()
        
        if not search_key:
            show_error("Spesialisasi harus diisi.")
            return
        
        loading = EnhancedLoadingAnimation("Mencari berdasarkan spesialisasi", "dots")
        loading.start()
        
        for schedule in schedules:
            doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
            if search_key in doctor_info['spesialisasi'].lower():
                results.append((schedule, doctor_info))
        
        loading.stop()
    
    elif choice == "3":
        days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
        
        print(Fore.YELLOW + "\n📅 Hari yang Tersedia:")
        print(Fore.CYAN + "┌─────┬─────────────────┐")
        print(Fore.CYAN + "│ No. │ Hari            │")
        print(Fore.CYAN + "├─────┼─────────────────┤")
        
        for i, day in enumerate(days, 1):
            print(Fore.CYAN + f"│ {Fore.WHITE}{i:2d}{Fore.CYAN}  │ 📅 {Fore.YELLOW}{day:<12}{Fore.CYAN} │")
        
        print(Fore.CYAN + "└─────┴─────────────────┘")
        
        try:
            day_choice = input(Fore.GREEN + "\n📅 Pilih hari (nomor): " + Fore.WHITE)
            day_index = int(day_choice) - 1
            
            if day_index < 0 or day_index >= len(days):
                show_error("Hari tidak valid.")
                return
            
            selected_day = days[day_index]
            
            loading = EnhancedLoadingAnimation(f"Mencari jadwal hari {selected_day}", "dots")
            loading.start()
            
            for schedule in schedules:
                doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
                if schedule['hari'] == selected_day:
                    results.append((schedule, doctor_info))
            
            loading.stop()
                    
        except ValueError:
            show_error("Input tidak valid.")
            return
    
    # Display results
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👤 Pasien", "🔍 Cari Jadwal", "📋 Hasil"])
    
    print_data_table_header("📋 HASIL PENCARIAN JADWAL 📋")
    
    if not results:
        print(Fore.YELLOW + "⚠️  Tidak ditemukan jadwal yang sesuai kriteria.")
        print(Fore.WHITE + "💡 Coba gunakan kata kunci yang berbeda atau lihat semua jadwal.")
        
        view_all = input(Fore.GREEN + "\n👀 Lihat semua jadwal tersedia? (y/n): " + Fore.WHITE).lower()
        if view_all == 'y':
            view_doctor_schedules()
            return
    else:
        # Display results with enhanced formatting
        table_data = []
        for i, (schedule, doctor_info) in enumerate(results, 1):
            # Calculate availability
            registered_count = len([r for r in registrations 
                                  if r['jadwal_id'] == schedule['id'] and r['status'] != 'Dibatalkan'])
            quota = int(schedule['kuota'])
            available = quota - registered_count
            
            # Availability status
            if available <= 0:
                availability_status = Fore.RED + "❌ Penuh" + Style.RESET_ALL
            elif available <= 2:
                availability_status = Fore.YELLOW + "⚠️ Terbatas" + Style.RESET_ALL
            else:
                availability_status = Fore.GREEN + "✅ Tersedia" + Style.RESET_ALL
            
            table_data.append([
                Fore.CYAN + str(i) + Style.RESET_ALL,
                Fore.GREEN + schedule['id'] + Style.RESET_ALL,
                Fore.YELLOW + doctor_info['nama'] + Style.RESET_ALL,
                Fore.MAGENTA + doctor_info['spesialisasi'] + Style.RESET_ALL,
                Fore.WHITE + schedule['hari'] + Style.RESET_ALL,
                Fore.CYAN + f"{schedule['jam_mulai']}-{schedule['jam_selesai']}" + Style.RESET_ALL,
                Fore.BLUE + f"{available}/{quota}" + Style.RESET_ALL,
                availability_status
            ])
        
        headers = [
            "No.", "ID", "Dokter", "Spesialisasi", 
            "Hari", "Waktu", "Tersedia", "Status"
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        print(Fore.GREEN + f"\n✅ Ditemukan {len(results)} jadwal yang sesuai")
        
        # Quick registration option
        register_now = input(Fore.GREEN + "\n📝 Ingin mendaftar sekarang? (y/n): " + Fore.WHITE).lower()
        if register_now == 'y':
            schedule_id = get_input_with_prompt("ID jadwal yang dipilih", "📝")
            if schedule_id:
                # Validate schedule ID from results
                valid_ids = [s[0]['id'] for s in results]
                if schedule_id in valid_ids:
                    # Get patient ID and call registration
                    patient_id = input(Fore.BLUE + "Masukkan ID pasien Anda: " + Fore.WHITE)
                    register_consultation_direct(patient_id, schedule_id)
                else:
                    show_error("ID jadwal tidak valid dari hasil pencarian.")
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")

def register_consultation(patient_id):
    """Register for a doctor consultation with enhanced UI and validation."""
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👤 Pasien", "📝 Daftar Konsultasi"])
    print_banner("📝 PENDAFTARAN KONSULTASI DOKTER", "green")
    
    # Show available schedules first
    print(Fore.YELLOW + "📅 Jadwal Dokter yang Tersedia:")
    print(Fore.BLUE + "─" * 60)
    
    loading = EnhancedLoadingAnimation("Memuat jadwal tersedia", "dots")
    loading.start()
    
    schedules = read_csv("data/jadwal_dokter.csv")
    doctors = read_csv("data/dokter.csv")
    registrations = read_csv("data/pendaftaran.csv")
    
    # Create doctor dictionary
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = {
            "nama": doctor['nama'], 
            "spesialisasi": doctor['spesialisasi']
        }
    
    # Filter available schedules (not full)
    available_schedules = []
    for schedule in schedules:
        registered_count = len([r for r in registrations 
                              if r['jadwal_id'] == schedule['id'] and r['status'] != 'Dibatalkan'])
        if registered_count < int(schedule['kuota']):
            available_schedules.append(schedule)
    
    loading.stop()
    
    if not available_schedules:
        print(Fore.RED + "❌ Maaf, semua jadwal dokter sudah penuh.")
        print(Fore.WHITE + "💡 Silakan coba lagi nanti atau hubungi administrasi.")
        input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali...")
        return
    
    # Display available schedules
    table_data = []
    for i, schedule in enumerate(available_schedules, 1):
        doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
        registered_count = len([r for r in registrations 
                              if r['jadwal_id'] == schedule['id'] and r['status'] != 'Dibatalkan'])
        available_spots = int(schedule['kuota']) - registered_count
        
        table_data.append([
            Fore.CYAN + str(i) + Style.RESET_ALL,
            Fore.GREEN + schedule['id'] + Style.RESET_ALL,
            Fore.YELLOW + doctor_info['nama'] + Style.RESET_ALL,
            Fore.MAGENTA + doctor_info['spesialisasi'] + Style.RESET_ALL,
            Fore.WHITE + schedule['hari'] + Style.RESET_ALL,
            Fore.CYAN + f"{schedule['jam_mulai']}-{schedule['jam_selesai']}" + Style.RESET_ALL,
            Fore.GREEN + str(available_spots) + Style.RESET_ALL
        ])
    
    headers = ["No.", "ID", "Dokter", "Spesialisasi", "Hari", "Waktu", "Sisa Slot"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    schedule_id = get_input_with_prompt("ID jadwal yang dipilih", "📝")
    
    if not schedule_id:
        show_error("ID jadwal harus diisi.")
        return
    
    # Continue with registration process
    register_consultation_direct(patient_id, schedule_id)

def register_consultation_direct(patient_id, schedule_id):
    """Direct registration with schedule ID."""
    loading = EnhancedLoadingAnimation("Memproses pendaftaran", "bars")
    loading.start()
    
    # Validate schedule
    schedules = read_csv("data/jadwal_dokter.csv")
    selected_schedule = None
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            selected_schedule = schedule
            break
    
    if not selected_schedule:
        loading.stop()
        show_error("Jadwal tidak ditemukan.")
        return
    
    # Get doctor info
    doctors = read_csv("data/dokter.csv")
    doctor_name = "Unknown Doctor"
    doctor_specialty = "Unknown"
    for doctor in doctors:
        if doctor['id'] == selected_schedule['dokter_id']:
            doctor_name = doctor['nama']
            doctor_specialty = doctor['spesialisasi']
            break
    
    # Calculate next appointment date
    days_map = {
        "Senin": 0, "Selasa": 1, "Rabu": 2, "Kamis": 3, 
        "Jumat": 4, "Sabtu": 5, "Minggu": 6
    }
    day_index = days_map.get(selected_schedule['hari'])
    
    if day_index is None:
        loading.stop()
        show_error("Hari jadwal tidak valid.")
        return
    
    # Find next occurrence
    today = datetime.now()
    days_ahead = (day_index - today.weekday()) % 7
    if days_ahead == 0:  # Today
        current_time = today.time()
        end_time = datetime.strptime(selected_schedule['jam_selesai'], '%H:%M').time()
        if current_time >= end_time:
            days_ahead = 7  # Next week
    
    next_occurrence = today + timedelta(days=days_ahead)
    date_str = next_occurrence.strftime("%Y-%m-%d")
    formatted_date = next_occurrence.strftime("%A, %d %B %Y")
    
    # Check existing registration
    registrations = read_csv("data/pendaftaran.csv")
    for reg in registrations:
        if (reg['pasien_id'] == patient_id and reg['jadwal_id'] == schedule_id and 
            reg['tanggal'] == date_str and reg['status'] != 'Dibatalkan'):
            loading.stop()
            show_error("Anda sudah terdaftar pada jadwal ini untuk tanggal tersebut.")
            return
    
    # Check quota
    quota = int(selected_schedule['kuota'])
    registered_count = sum(1 for reg in registrations if 
                           reg['jadwal_id'] == schedule_id and 
                           reg['tanggal'] == date_str and 
                           reg['status'] != 'Dibatalkan')
    
    if registered_count >= quota:
        loading.stop()
        show_error("Maaf, kuota untuk jadwal ini sudah penuh.")
        return
    
    # Generate queue number
    queue = Queue()
    for i in range(1, quota + 1):
        queue.enqueue(i)
    
    # Remove taken queue numbers
    for reg in registrations:
        if (reg['jadwal_id'] == schedule_id and reg['tanggal'] == date_str and 
            reg['status'] != 'Dibatalkan' and reg['nomor_antrian'].isdigit()):
            queue_num = int(reg['nomor_antrian'])
            # Remove from queue
            temp_queue = Queue()
            while not queue.is_empty():
                num = queue.dequeue()
                if num != queue_num:
                    temp_queue.enqueue(num)
            queue = temp_queue
    
    if queue.is_empty():
        loading.stop()
        show_error("Semua nomor antrian sudah terisi.")
        return
    
    queue_number = queue.dequeue()
    loading.stop()
    
    # Show confirmation
    print(Fore.YELLOW + "\n📋 Konfirmasi Pendaftaran:")
    print(Fore.CYAN + "╔" + "═" * 60 + "╗")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "║ " + Fore.GREEN + f"👨‍⚕️ Dokter: {doctor_name} ({doctor_specialty})" + " " * (60 - len(f"👨‍⚕️ Dokter: {doctor_name} ({doctor_specialty})") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.YELLOW + f"📅 Jadwal: {selected_schedule['hari']}, {selected_schedule['jam_mulai']}-{selected_schedule['jam_selesai']}" + " " * (60 - len(f"📅 Jadwal: {selected_schedule['hari']}, {selected_schedule['jam_mulai']}-{selected_schedule['jam_selesai']}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + f"📆 Tanggal: {formatted_date}" + " " * (60 - len(f"📆 Tanggal: {formatted_date}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.MAGENTA + f"🎫 Nomor Antrian: {queue_number}" + " " * (60 - len(f"🎫 Nomor Antrian: {queue_number}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "╚" + "═" * 60 + "╝")
    
    confirm = input(Fore.GREEN + "\n✅ Konfirmasi pendaftaran? (y/n): " + Fore.WHITE).lower()
    
    if confirm != 'y':
        print(Fore.YELLOW + "❌ Pendaftaran dibatalkan.")
        input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
        return
    
    loading = EnhancedLoadingAnimation("Menyimpan data pendaftaran", "bars")
    loading.start()
    
    # Generate registration ID
    new_reg_id = f"R{len(registrations) + 1:03d}"
    
    # Add registration
    new_registration = {
        'id': new_reg_id,
        'pasien_id': patient_id,
        'jadwal_id': schedule_id,
        'tanggal': date_str,
        'status': 'Terdaftar',
        'nomor_antrian': str(queue_number)
    }
    
    registrations.append(new_registration)
    write_csv("data/pendaftaran.csv", registrations)
    
    loading.stop()
    
    # Success message with ticket-like design
    print(Fore.GREEN + "\n🎉 " + Style.BRIGHT + "PENDAFTARAN BERHASIL!" + Style.RESET_ALL)
    
    print(Fore.CYAN + "╔" + "═" * 60 + "╗")
    print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + "              🎫 TIKET KONSULTASI 🎫              ".center(60) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 60 + "╣")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "║ " + Fore.YELLOW + f"📝 ID Pendaftaran: {new_reg_id}" + " " * (60 - len(f"📝 ID Pendaftaran: {new_reg_id}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.GREEN + f"👨‍⚕️ Dokter: {doctor_name}" + " " * (60 - len(f"👨‍⚕️ Dokter: {doctor_name}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.MAGENTA + f"🏥 Spesialisasi: {doctor_specialty}" + " " * (60 - len(f"🏥 Spesialisasi: {doctor_specialty}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + f"📅 Hari: {selected_schedule['hari']}" + " " * (60 - len(f"📅 Hari: {selected_schedule['hari']}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.CYAN + f"⏰ Waktu: {selected_schedule['jam_mulai']} - {selected_schedule['jam_selesai']}" + " " * (60 - len(f"⏰ Waktu: {selected_schedule['jam_mulai']} - {selected_schedule['jam_selesai']}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.BLUE + f"📆 Tanggal: {formatted_date}" + " " * (60 - len(f"📆 Tanggal: {formatted_date}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.RED + Style.BRIGHT + f"🎫 NOMOR ANTRIAN: {queue_number}" + " " * (60 - len(f"🎫 NOMOR ANTRIAN: {queue_number}") - 1) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "╚" + "═" * 60 + "╝")
    
    print(Fore.GREEN + "\n💡 Penting untuk diingat:")
    print(Fore.WHITE + "   • Datang 15 menit sebelum waktu praktik")
    print(Fore.WHITE + "   • Bawa kartu identitas dan tiket ini")
    print(Fore.WHITE + "   • Hubungi klinik jika berhalangan hadir")
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")

# Continuation of modules/patient.py - Remaining patient functions

def request_schedule_change(patient_id):
    """Request a change to a registered consultation with enhanced UI."""
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👤 Pasien", "🔄 Ubah Jadwal"])
    print_banner("🔄 PENGAJUAN PERUBAHAN JADWAL", "yellow")
    
    loading = EnhancedLoadingAnimation("Memuat pendaftaran Anda", "dots")
    loading.start()
    
    # Get patient's active registrations
    registrations = read_csv("data/pendaftaran.csv")
    patient_registrations = [reg for reg in registrations if 
                            reg['pasien_id'] == patient_id and 
                            reg['status'] == 'Terdaftar']
    
    schedules = read_csv("data/jadwal_dokter.csv")
    doctors = read_csv("data/dokter.csv")
    
    # Create lookup dictionaries
    schedule_dict = {}
    for schedule in schedules:
        schedule_dict[schedule['id']] = schedule
    
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = doctor['nama']
    
    loading.stop()
    
    if not patient_registrations:
        print(Fore.YELLOW + "⚠️  Anda tidak memiliki pendaftaran aktif.")
        print(Fore.WHITE + "💡 Gunakan menu 'Mendaftar Konsultasi' untuk membuat janji baru.")
        
        register_new = input(Fore.GREEN + "\n📝 Ingin mendaftar konsultasi baru? (y/n): " + Fore.WHITE).lower()
        if register_new == 'y':
            register_consultation(patient_id)
        
        input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")
        return
    
    print(Fore.YELLOW + "📋 Pendaftaran Aktif Anda:")
    print(Fore.BLUE + "─" * 80)
    
    # Enhanced display of active registrations
    table_data = []
    for i, reg in enumerate(patient_registrations, 1):
        schedule = schedule_dict.get(reg['jadwal_id'], None)
        if schedule:
            doctor_name = doctor_dict.get(schedule['dokter_id'], "Unknown")
            schedule_info = f"{schedule['hari']} {schedule['jam_mulai']}-{schedule['jam_selesai']}"
            
            # Format date
            try:
                date_obj = datetime.strptime(reg['tanggal'], '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d/%m/%Y (%A)')
                
                # Check if appointment is today or upcoming
                days_until = (date_obj.date() - datetime.now().date()).days
                if days_until == 0:
                    date_status = Fore.RED + "HARI INI" + Style.RESET_ALL
                elif days_until == 1:
                    date_status = Fore.YELLOW + "BESOK" + Style.RESET_ALL
                elif days_until > 0:
                    date_status = Fore.GREEN + f"{days_until} hari lagi" + Style.RESET_ALL
                else:
                    date_status = Fore.RED + "TERLEWAT" + Style.RESET_ALL
                    
            except:
                formatted_date = reg['tanggal']
                date_status = ""
            
            table_data.append([
                Fore.CYAN + str(i) + Style.RESET_ALL,
                Fore.GREEN + reg['id'] + Style.RESET_ALL,
                Fore.YELLOW + doctor_name + Style.RESET_ALL,
                Fore.WHITE + schedule_info + Style.RESET_ALL,
                Fore.MAGENTA + formatted_date + Style.RESET_ALL,
                date_status,
                Fore.BLUE + reg['nomor_antrian'] + Style.RESET_ALL
            ])
    
    headers = [
        "No.", "ID Daftar", "Dokter", "Jadwal", 
        "Tanggal", "Status", "Antrian"
    ]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    try:
        reg_choice = input(Fore.GREEN + "\n🔄 Pilih nomor pendaftaran yang ingin diubah: " + Fore.WHITE)
        reg_index = int(reg_choice) - 1
        
        if reg_index < 0 or reg_index >= len(patient_registrations):
            show_error("Nomor tidak valid.")
            return
        
        selected_reg = patient_registrations[reg_index]
        selected_schedule = schedule_dict.get(selected_reg['jadwal_id'])
        doctor_name = doctor_dict.get(selected_schedule['dokter_id'], "Unknown") if selected_schedule else "Unknown"
        
        # Show selected registration details
        print(Fore.YELLOW + f"\n📋 Pendaftaran yang dipilih:")
        print(Fore.CYAN + "┌─" + "─" * 50 + "┐")
        print(Fore.CYAN + f"│ ID Pendaftaran: {Fore.WHITE}{selected_reg['id']:<32}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Dokter: {Fore.WHITE}{doctor_name:<40}{Fore.CYAN} │")
        if selected_schedule:
            print(Fore.CYAN + f"│ Jadwal: {Fore.WHITE}{selected_schedule['hari']} {selected_schedule['jam_mulai']}-{selected_schedule['jam_selesai']:<25}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Tanggal: {Fore.WHITE}{selected_reg['tanggal']:<39}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Nomor Antrian: {Fore.WHITE}{selected_reg['nomor_antrian']:<30}{Fore.CYAN} │")
        print(Fore.CYAN + "└─" + "─" * 50 + "┘")
        
        # Check if appointment is too soon to cancel
        try:
            appt_date = datetime.strptime(selected_reg['tanggal'], '%Y-%m-%d')
            hours_until = (appt_date - datetime.now()).total_seconds() / 3600
            
            if hours_until < 24:
                print(Fore.RED + "\n⚠️  PERINGATAN: Pendaftaran kurang dari 24 jam!")
                print(Fore.YELLOW + "💡 Pembatalan mungkin dikenakan biaya atau tidak diizinkan.")
                
                proceed = input(Fore.YELLOW + "Tetap lanjutkan? (y/n): " + Fore.WHITE).lower()
                if proceed != 'y':
                    print(Fore.CYAN + "Operasi dibatalkan.")
                    input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
                    return
        except:
            pass
        
        # Show change options
        print(Fore.YELLOW + "\n🔄 Opsi Perubahan:")
        print(Fore.CYAN + "╔" + "═" * 60 + "╗")
        print(Fore.CYAN + "║" + " " * 60 + "║")
        print(Fore.CYAN + "║ " + Fore.GREEN + "❌ 1." + Fore.YELLOW + " Batalkan Pendaftaran                              " + Fore.CYAN + "║")
        print(Fore.CYAN + "║ " + Fore.GREEN + "🔄 2." + Fore.YELLOW + " Reschedule ke Jadwal Lain                         " + Fore.CYAN + "║")
        print(Fore.CYAN + "║ " + Fore.RED + "🔙 3." + Fore.YELLOW + " Kembali ke Menu                                   " + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + " " * 60 + "║")
        print(Fore.CYAN + "╚" + "═" * 60 + "╝")
        
        change_choice = input(Fore.GREEN + "\n🔄 Pilihan Anda: " + Fore.WHITE)
        
        if change_choice == "1":
            # Cancel registration
            print(Fore.RED + "\n❌ KONFIRMASI PEMBATALAN")
            print(Fore.YELLOW + "⚠️  Anda akan membatalkan pendaftaran konsultasi.")
            print(Fore.WHITE + "💡 Slot akan tersedia untuk pasien lain.")
            
            final_confirm = input(Fore.RED + "\nKetik 'BATAL' untuk konfirmasi: " + Fore.WHITE)
            
            if final_confirm != 'BATAL':
                print(Fore.YELLOW + "❌ Pembatalan dibatalkan.")
                input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
                return
            
            loading = EnhancedLoadingAnimation("Membatalkan pendaftaran", "bars")
            loading.start()
            
            # Update registration status
            for i, reg in enumerate(registrations):
                if reg['id'] == selected_reg['id']:
                    registrations[i]['status'] = 'Dibatalkan'
                    write_csv("data/pendaftaran.csv", registrations)
                    loading.stop()
                    
                    print(Fore.GREEN + "\n✅ " + Style.BRIGHT + "PEMBATALAN BERHASIL!")
                    print(Fore.CYAN + "╔" + "═" * 50 + "╗")
                    print(Fore.CYAN + "║" + " " * 50 + "║")
                    print(Fore.CYAN + "║ " + Fore.GREEN + "✅ Pendaftaran berhasil dibatalkan      " + Fore.CYAN + "║")
                    print(Fore.CYAN + "║ " + Fore.YELLOW + f"📝 ID: {selected_reg['id']:<35}" + Fore.CYAN + "║")
                    print(Fore.CYAN + "║ " + Fore.WHITE + "💡 Slot tersedia untuk pasien lain     " + Fore.CYAN + "║")
                    print(Fore.CYAN + "║" + " " * 50 + "║")
                    print(Fore.CYAN + "╚" + "═" * 50 + "╝")
                    break
            
        elif change_choice == "2":
            # Reschedule to another appointment
            print(Fore.BLUE + "\n🔄 RESCHEDULE PENDAFTARAN")
            print(Fore.YELLOW + "💡 Pilih jadwal baru untuk mengganti yang lama.")
            
            # Show available schedules excluding current one
            available_schedules = []
            for schedule in schedules:
                if schedule['id'] != selected_reg['jadwal_id']:
                    # Check availability
                    reg_count = len([r for r in registrations 
                                   if r['jadwal_id'] == schedule['id'] and r['status'] != 'Dibatalkan'])
                    if reg_count < int(schedule['kuota']):
                        available_schedules.append(schedule)
            
            if not available_schedules:
                print(Fore.RED + "❌ Tidak ada jadwal lain yang tersedia.")
                input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
                return
            
            print(Fore.YELLOW + "\n📅 Jadwal Tersedia untuk Reschedule:")
            table_data = []
            for i, schedule in enumerate(available_schedules, 1):
                doctor_name_new = doctor_dict.get(schedule['dokter_id'], "Unknown")
                reg_count = len([r for r in registrations 
                               if r['jadwal_id'] == schedule['id'] and r['status'] != 'Dibatalkan'])
                available_spots = int(schedule['kuota']) - reg_count
                
                table_data.append([
                    str(i),
                    schedule['id'],
                    doctor_name_new,
                    schedule['hari'],
                    f"{schedule['jam_mulai']}-{schedule['jam_selesai']}",
                    str(available_spots)
                ])
            
            headers = ["No.", "ID", "Dokter", "Hari", "Waktu", "Sisa Slot"]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
            
            try:
                new_choice = int(input(Fore.GREEN + "\n🔄 Pilih jadwal baru (nomor): " + Fore.WHITE)) - 1
                
                if new_choice < 0 or new_choice >= len(available_schedules):
                    show_error("Pilihan tidak valid.")
                    return
                
                new_schedule = available_schedules[new_choice]
                new_doctor_name = doctor_dict.get(new_schedule['dokter_id'], "Unknown")
                
                # Show reschedule confirmation
                print(Fore.YELLOW + "\n📋 Konfirmasi Reschedule:")
                print(Fore.CYAN + "┌─" + "─" * 60 + "┐")
                print(Fore.CYAN + f"│ {'DARI':<29} │ {'KE':<29} │")
                print(Fore.CYAN + "├─" + "─" * 29 + "┼─" + "─" * 29 + "┤")
                print(Fore.CYAN + f"│ {Fore.RED}Dokter: {doctor_name:<20}{Fore.CYAN} │ {Fore.GREEN}Dokter: {new_doctor_name:<20}{Fore.CYAN} │")
                if selected_schedule:
                    old_schedule_info = f"{selected_schedule['hari']} {selected_schedule['jam_mulai']}-{selected_schedule['jam_selesai']}"
                    new_schedule_info = f"{new_schedule['hari']} {new_schedule['jam_mulai']}-{new_schedule['jam_selesai']}"
                    print(Fore.CYAN + f"│ {Fore.RED}Jadwal: {old_schedule_info:<18}{Fore.CYAN} │ {Fore.GREEN}Jadwal: {new_schedule_info:<18}{Fore.CYAN} │")
                print(Fore.CYAN + "└─" + "─" * 29 + "┴─" + "─" * 29 + "┘")
                
                confirm_reschedule = input(Fore.GREEN + "\n✅ Konfirmasi reschedule? (y/n): " + Fore.WHITE).lower()
                
                if confirm_reschedule != 'y':
                    print(Fore.YELLOW + "❌ Reschedule dibatalkan.")
                    input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
                    return
                
                loading = EnhancedLoadingAnimation("Memproses reschedule", "bars")
                loading.start()
                
                # Calculate new date and queue
                days_map = {
                    "Senin": 0, "Selasa": 1, "Rabu": 2, "Kamis": 3, 
                    "Jumat": 4, "Sabtu": 5, "Minggu": 6
                }
                new_day_index = days_map.get(new_schedule['hari'])
                today = datetime.now()
                days_ahead = (new_day_index - today.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7
                
                new_date = today + timedelta(days=days_ahead)
                new_date_str = new_date.strftime("%Y-%m-%d")
                
                # Get new queue number
                new_queue = Queue()
                for i in range(1, int(new_schedule['kuota']) + 1):
                    new_queue.enqueue(i)
                
                # Remove taken numbers
                for reg in registrations:
                    if (reg['jadwal_id'] == new_schedule['id'] and 
                        reg['tanggal'] == new_date_str and 
                        reg['status'] != 'Dibatalkan'):
                        if reg['nomor_antrian'].isdigit():
                            taken_num = int(reg['nomor_antrian'])
                            temp_queue = Queue()
                            while not new_queue.is_empty():
                                num = new_queue.dequeue()
                                if num != taken_num:
                                    temp_queue.enqueue(num)
                            new_queue = temp_queue
                
                new_queue_number = new_queue.dequeue() if not new_queue.is_empty() else 1
                
                # Update registration
                for i, reg in enumerate(registrations):
                    if reg['id'] == selected_reg['id']:
                        registrations[i]['jadwal_id'] = new_schedule['id']
                        registrations[i]['tanggal'] = new_date_str
                        registrations[i]['nomor_antrian'] = str(new_queue_number)
                        write_csv("data/pendaftaran.csv", registrations)
                        break
                
                loading.stop()
                
                print(Fore.GREEN + "\n🎉 " + Style.BRIGHT + "RESCHEDULE BERHASIL!")
                print(Fore.CYAN + "╔" + "═" * 60 + "╗")
                print(Fore.CYAN + "║" + " " * 60 + "║")
                print(Fore.CYAN + "║ " + Fore.GREEN + "✅ Jadwal berhasil diubah                      " + Fore.CYAN + "║")
                print(Fore.CYAN + "║ " + Fore.YELLOW + f"👨‍⚕️ Dokter: {new_doctor_name:<40}" + Fore.CYAN + "║")
                print(Fore.CYAN + "║ " + Fore.WHITE + f"📅 Jadwal: {new_schedule['hari']} {new_schedule['jam_mulai']}-{new_schedule['jam_selesai']:<30}" + Fore.CYAN + "║")
                print(Fore.CYAN + "║ " + Fore.MAGENTA + f"📆 Tanggal: {new_date.strftime('%d/%m/%Y (%A)'):<35}" + Fore.CYAN + "║")
                print(Fore.CYAN + "║ " + Fore.BLUE + f"🎫 Antrian: {new_queue_number:<40}" + Fore.CYAN + "║")
                print(Fore.CYAN + "║" + " " * 60 + "║")
                print(Fore.CYAN + "╚" + "═" * 60 + "╝")
                
            except ValueError:
                show_error("Input tidak valid.")
                return
        
        elif change_choice == "3":
            return
        else:
            show_error("Pilihan tidak valid.")
            return
        
    except ValueError:
        show_error("Input tidak valid.")
    except Exception as e:
        show_error(f"Terjadi kesalahan: {str(e)}")
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")

def view_registration_status(patient_id):
    """View patient's registration status with enhanced display and insights."""
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👤 Pasien", "📋 Status Pendaftaran"])
    
    print_data_table_header("📋 STATUS PENDAFTARAN KONSULTASI SAYA 📋")
    
    loading = EnhancedLoadingAnimation("Memuat riwayat pendaftaran Anda", "dots")
    loading.start()
    
    registrations = read_csv("data/pendaftaran.csv")
    patient_registrations = [reg for reg in registrations if reg['pasien_id'] == patient_id]
    
    schedules = read_csv("data/jadwal_dokter.csv")
    doctors = read_csv("data/dokter.csv")
    
    # Create lookup dictionaries
    schedule_dict = {}
    for schedule in schedules:
        schedule_dict[schedule['id']] = schedule
    
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = doctor
    
    loading.stop()
    
    if not patient_registrations:
        print(Fore.YELLOW + "⚠️  Anda belum memiliki riwayat pendaftaran konsultasi.")
        print(Fore.WHITE + "💡 Gunakan menu 'Mendaftar Konsultasi' untuk membuat janji dengan dokter.")
        
        # Quick registration option
        register_now = input(Fore.GREEN + "\n📝 Ingin mendaftar konsultasi sekarang? (y/n): " + Fore.WHITE).lower()
        if register_now == 'y':
            register_consultation(patient_id)
        
        input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")
        return
    
    # Categorize registrations
    active_regs = [r for r in patient_registrations if r['status'] == 'Terdaftar']
    canceled_regs = [r for r in patient_registrations if r['status'] == 'Dibatalkan']
    completed_regs = [r for r in patient_registrations if r['status'] == 'Selesai']
    
    # Enhanced statistics
    print(Fore.CYAN + "📊 Ringkasan Pendaftaran Anda:")
    print(Fore.WHITE + f"   • Total Pendaftaran: {Fore.YELLOW}{len(patient_registrations)}")
    print(Fore.WHITE + f"   • Aktif: {Fore.GREEN}{len(active_regs)}")
    print(Fore.WHITE + f"   • Selesai: {Fore.BLUE}{len(completed_regs)}")
    print(Fore.WHITE + f"   • Dibatalkan: {Fore.RED}{len(canceled_regs)}")
    print()
    
    # Display all registrations with enhanced formatting
    table_data = []
    for i, reg in enumerate(patient_registrations, 1):
        schedule = schedule_dict.get(reg['jadwal_id'], None)
        if schedule:
            doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
            doctor_name = f"{doctor_info['nama']} ({doctor_info['spesialisasi']})"
            schedule_info = f"{schedule['hari']} {schedule['jam_mulai']}-{schedule['jam_selesai']}"
            
            # Enhanced status display with icons and colors
            status = reg['status']
            if status == 'Terdaftar':
                # Check if appointment is upcoming, today, or overdue
                try:
                    appt_date = datetime.strptime(reg['tanggal'], '%Y-%m-%d')
                    days_until = (appt_date.date() - datetime.now().date()).days
                    
                    if days_until < 0:
                        status_display = Fore.RED + "⏰ Terlewat" + Style.RESET_ALL
                    elif days_until == 0:
                        status_display = Fore.YELLOW + "🔥 HARI INI" + Style.RESET_ALL
                    elif days_until == 1:
                        status_display = Fore.CYAN + "📅 BESOK" + Style.RESET_ALL
                    else:
                        status_display = Fore.GREEN + "✅ Terdaftar" + Style.RESET_ALL
                except:
                    status_display = Fore.GREEN + "✅ Terdaftar" + Style.RESET_ALL
            elif status == 'Dibatalkan':
                status_display = Fore.RED + "❌ Dibatalkan" + Style.RESET_ALL
            elif status == 'Selesai':
                status_display = Fore.BLUE + "✔️ Selesai" + Style.RESET_ALL
            else:
                status_display = Fore.YELLOW + "⏳ " + status + Style.RESET_ALL
            
            # Format date nicely
            try:
                date_obj = datetime.strptime(reg['tanggal'], '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d/%m/%Y')
                day_name = date_obj.strftime('%A')[:3]  # Mon, Tue, etc.
                date_display = f"{formatted_date} ({day_name})"
            except:
                date_display = reg['tanggal']
                
            table_data.append([
                Fore.CYAN + str(i) + Style.RESET_ALL,
                Fore.GREEN + reg['id'] + Style.RESET_ALL,
                Fore.YELLOW + doctor_name + Style.RESET_ALL,
                Fore.WHITE + schedule_info + Style.RESET_ALL,
                Fore.MAGENTA + date_display + Style.RESET_ALL,
                status_display,
                Fore.BLUE + reg['nomor_antrian'] + Style.RESET_ALL
            ])
    
    headers = [
        Fore.BLUE + Style.BRIGHT + "No." + Style.RESET_ALL,
        Fore.BLUE + Style.BRIGHT + "ID" + Style.RESET_ALL,
        Fore.BLUE + Style.BRIGHT + "Dokter (Spesialisasi)" + Style.RESET_ALL,
        Fore.BLUE + Style.BRIGHT + "Jadwal" + Style.RESET_ALL,
        Fore.BLUE + Style.BRIGHT + "Tanggal" + Style.RESET_ALL,
        Fore.BLUE + Style.BRIGHT + "Status" + Style.RESET_ALL,
        Fore.BLUE + Style.BRIGHT + "Antrian" + Style.RESET_ALL
    ]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    # Show upcoming appointments prominently
    if active_regs:
        print_section_header("🔜 JADWAL MENDATANG", "📅")
        
        upcoming_appointments = []
        for reg in active_regs:
            try:
                appt_date = datetime.strptime(reg['tanggal'], '%Y-%m-%d')
                if appt_date.date() >= datetime.now().date():
                    upcoming_appointments.append((reg, appt_date))
            except:
                pass
        
        # Sort by date
        upcoming_appointments.sort(key=lambda x: x[1])
        
        if upcoming_appointments:
            for reg, appt_date in upcoming_appointments[:3]:  # Show next 3 appointments
                schedule = schedule_dict.get(reg['jadwal_id'])
                if schedule:
                    doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
                    days_until = (appt_date.date() - datetime.now().date()).days
                    
                    print(Fore.CYAN + "┌─" + "─" * 60 + "┐")
                    print(Fore.CYAN + f"│ 🎫 {Fore.GREEN}{reg['id']}" + " " * (60 - len(f"🎫 {reg['id']}") - 1) + Fore.CYAN + "│")
                    print(Fore.CYAN + f"│ 👨‍⚕️ {Fore.YELLOW}{doctor_info['nama']} ({doctor_info['spesialisasi']})" + " " * (60 - len(f"👨‍⚕️ {doctor_info['nama']} ({doctor_info['spesialisasi']})") - 1) + Fore.CYAN + "│")
                    print(Fore.CYAN + f"│ 📅 {Fore.WHITE}{appt_date.strftime('%A, %d %B %Y')}" + " " * (60 - len(f"📅 {appt_date.strftime('%A, %d %B %Y')}") - 1) + Fore.CYAN + "│")
                    print(Fore.CYAN + f"│ ⏰ {Fore.CYAN}{schedule['jam_mulai']} - {schedule['jam_selesai']}" + " " * (60 - len(f"⏰ {schedule['jam_mulai']} - {schedule['jam_selesai']}") - 1) + Fore.CYAN + "│")
                    print(Fore.CYAN + f"│ 🎫 Antrian: {Fore.BLUE}{reg['nomor_antrian']}" + " " * (60 - len(f"🎫 Antrian: {reg['nomor_antrian']}") - 1) + Fore.CYAN + "│")
                    
                    if days_until == 0:
                        print(Fore.CYAN + f"│ {Fore.RED + Style.BRIGHT}🔥 HARI INI - Jangan sampai terlambat!" + " " * (57 - len("🔥 HARI INI - Jangan sampai terlambat!")) + Fore.CYAN + "│")
                    elif days_until == 1:
                        print(Fore.CYAN + f"│ {Fore.YELLOW}📅 BESOK - Siapkan diri Anda" + " " * (60 - len("📅 BESOK - Siapkan diri Anda") - 1) + Fore.CYAN + "│")
                    else:
                        print(Fore.CYAN + f"│ ⏳ {Fore.GREEN}{days_until} hari lagi" + " " * (60 - len(f"⏳ {days_until} hari lagi") - 1) + Fore.CYAN + "│")
                    
                    print(Fore.CYAN + "└─" + "─" * 60 + "┘")
                    print()
        else:
            print(Fore.YELLOW + "📅 Tidak ada jadwal mendatang yang aktif.")
    
    # Show quick actions
    if active_regs:
        print(Fore.CYAN + "\n🔧 Aksi Cepat:")
        print(Fore.WHITE + "   • Ketik 'ubah' untuk mengubah jadwal")
        print(Fore.WHITE + "   • Ketik 'batal' untuk membatalkan pendaftaran")
        
        quick_action = input(Fore.GREEN + "\n⚡ Aksi cepat (atau Enter untuk kembali): " + Fore.WHITE).lower()
        
        if quick_action == 'ubah':
            request_schedule_change(patient_id)
            return
        elif quick_action == 'batal':
            request_schedule_change(patient_id)
            return
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")