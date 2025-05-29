# modules/doctor.py - Enhanced Doctor functionality
import os
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Style
from .data_manager import read_csv, write_csv, get_patient_name
from .data_structures.linked_list import LinkedList
from .utils import (clear_screen, show_breadcrumbs, show_error, show_success, show_help, 
                   EnhancedLoadingAnimation, print_banner, get_input_with_prompt, 
                   print_data_table_header, print_section_header)

def doctor_menu(doctor_id):
    """Display enhanced doctor menu and handle doctor actions."""
    doctor_data = None
    doctors = read_csv("data/dokter.csv")
    for doctor in doctors:
        if doctor['id'] == doctor_id:
            doctor_data = doctor
            break
    
    if not doctor_data:
        show_error("Data dokter tidak ditemukan.")
        return
    
    while True:
        clear_screen()
        show_breadcrumbs(["🏠 Main Menu", "👩‍⚕️ Dokter Dashboard"])
        
        # Enhanced doctor header
        print(Fore.CYAN + "╔" + "═" * 80 + "╗")
        print(Fore.CYAN + "║" + " " * 80 + "║")
        print(Fore.CYAN + "║" + Fore.GREEN + Style.BRIGHT + f"    👩‍⚕️ DASHBOARD DOKTER - {doctor_data['nama']} ({doctor_data['spesialisasi']}) 👩‍⚕️    ".center(80) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + "                     🏥 Kelola Jadwal & Pasien Anda 🏥                      " + "║")
        print(Fore.CYAN + "║" + " " * 80 + "║")
        print(Fore.CYAN + "╠" + "═" * 80 + "╣")
        
        # Enhanced menu options
        print(Fore.CYAN + "║  " + Fore.GREEN + "📅 1." + Fore.YELLOW + " Lihat Jadwal Praktik Saya                                    " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "➕ 2." + Fore.YELLOW + " Tambah Jadwal Praktik Baru                                   " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "✏️  3." + Fore.YELLOW + " Edit Jadwal Praktik                                          " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "👥 4." + Fore.YELLOW + " Lihat Pasien Terdaftar                                      " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.RED + "🚪 5." + Fore.YELLOW + " Logout dari Dashboard                                        " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.BLUE + "❓ ?." + Fore.YELLOW + " Bantuan & Panduan Dokter                                     " + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + " " * 80 + "║")
        print(Fore.CYAN + "╚" + "═" * 80 + "╝")
        
        choice = input(Fore.GREEN + "\n➤ Pilihan Anda: " + Fore.WHITE)
        
        if choice == "1":
            view_doctor_schedules(doctor_id)
        elif choice == "2":
            add_doctor_schedule(doctor_id)
        elif choice == "3":
            edit_doctor_schedule(doctor_id)
        elif choice == "4":
            view_registered_patients(doctor_id)
        elif choice == "5":
            print(Fore.CYAN + "👋 Logout berhasil. Terima kasih atas pelayanan Anda!")
            break
        elif choice == "?":
            show_help("doctor")
        else:
            show_error("Pilihan tidak valid. Silakan pilih 1-5 atau ?")

def view_doctor_schedules(doctor_id):
    """View schedules for the specified doctor with enhanced display."""
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👩‍⚕️ Dokter", "📅 Jadwal Praktik"])
    
    print_data_table_header("📅 JADWAL PRAKTIK SAYA 📅")
    
    loading = EnhancedLoadingAnimation("Memuat jadwal praktik Anda", "dots")
    loading.start()
    
    schedules = read_csv("data/jadwal_dokter.csv")
    
    # Filter schedules for this doctor
    doctor_schedules = [sch for sch in schedules if sch['dokter_id'] == doctor_id]
    
    # Create linked list to store schedule data
    schedule_list = LinkedList()
    for schedule in doctor_schedules:
        schedule_data = {
            'id': schedule['id'],
            'hari': schedule['hari'],
            'waktu': f"{schedule['jam_mulai']} - {schedule['jam_selesai']}",
            'kuota': schedule['kuota']
        }
        schedule_list.append(schedule_data)
    
    loading.stop()
    
    # Display schedules
    all_schedules = schedule_list.display()
    if not all_schedules:
        print(Fore.YELLOW + "⚠️  Anda belum memiliki jadwal praktik.")
        print(Fore.WHITE + "💡 Gunakan menu 'Tambah Jadwal' untuk membuat jadwal baru.")
        
        print(Fore.CYAN + "\n┌─────────────────────────────────────────┐")
        print(Fore.CYAN + "│ " + Fore.GREEN + "🆕 Ingin menambah jadwal sekarang?     " + Fore.CYAN + "│")
        print(Fore.CYAN + "└─────────────────────────────────────────┘")
        
        choice = input(Fore.GREEN + "Tambah jadwal baru? (y/n): " + Fore.WHITE).lower()
        if choice == 'y':
            add_doctor_schedule(doctor_id)
            return
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for i, schedule in enumerate(all_schedules, 1):
            # Count registered patients for this schedule
            registrations = read_csv("data/pendaftaran.csv")
            registered_count = len([r for r in registrations 
                                 if r['jadwal_id'] == schedule['id'] and r['status'] != 'Dibatalkan'])
            
            availability = f"{registered_count}/{schedule['kuota']}"
            
            # Color coding for availability
            if registered_count == 0:
                availability_color = Fore.GREEN
            elif registered_count >= int(schedule['kuota']):
                availability_color = Fore.RED
            else:
                availability_color = Fore.YELLOW
            
            table_data.append([
                Fore.CYAN + str(i) + Style.RESET_ALL,
                Fore.GREEN + schedule['id'] + Style.RESET_ALL,
                Fore.YELLOW + schedule['hari'] + Style.RESET_ALL,
                Fore.WHITE + schedule['waktu'] + Style.RESET_ALL,
                Fore.MAGENTA + schedule['kuota'] + Style.RESET_ALL,
                availability_color + availability + Style.RESET_ALL
            ])
        
        headers = [
            Fore.BLUE + Style.BRIGHT + "No." + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "ID Jadwal" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Hari" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Waktu" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Kuota" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Terdaftar" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        print(Fore.CYAN + f"\n📊 Total Jadwal Anda: {Fore.YELLOW}{len(all_schedules)} jadwal")
        
        # Calculate total capacity and utilization
        total_capacity = sum(int(s['kuota']) for s in all_schedules)
        total_registered = sum(len([r for r in read_csv("data/pendaftaran.csv") 
                                  if r['jadwal_id'] == s['id'] and r['status'] != 'Dibatalkan']) 
                             for s in all_schedules)
        
        utilization = (total_registered / total_capacity * 100) if total_capacity > 0 else 0
        
        print(Fore.CYAN + f"📈 Utilisasi Jadwal: {Fore.YELLOW}{utilization:.1f}% " + 
              f"({total_registered}/{total_capacity})")
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")

def add_doctor_schedule(doctor_id):
    """Add a new schedule for the doctor with enhanced UI."""
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👩‍⚕️ Dokter", "➕ Tambah Jadwal"])
    print_banner("➕ TAMBAH JADWAL PRAKTIK BARU", "green")
    
    # Get doctor info
    doctors = read_csv("data/dokter.csv")
    doctor_name = "Unknown"
    for doctor in doctors:
        if doctor['id'] == doctor_id:
            doctor_name = f"Dr. {doctor['nama']} ({doctor['spesialisasi']})"
            break
    
    print(Fore.GREEN + f"👩‍⚕️ Menambah jadwal untuk: {Fore.YELLOW}{doctor_name}")
    print(Fore.BLUE + "─" * 60)
    
    # Day selection with enhanced UI
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    day_icons = ["📅", "📅", "📅", "📅", "📅", "📅"]
    
    print(Fore.YELLOW + "\n📅 Pilih hari praktik:")
    print(Fore.CYAN + "┌─────┬──────────────────┐")
    print(Fore.CYAN + "│ No. │ Hari             │")
    print(Fore.CYAN + "├─────┼──────────────────┤")
    
    for i, day in enumerate(days, 1):
        print(Fore.CYAN + f"│ {Fore.WHITE}{i:2d}{Fore.CYAN}  │ {day_icons[i-1]} {Fore.YELLOW}{day:<12}{Fore.CYAN} │")
    
    print(Fore.CYAN + "└─────┴──────────────────┘")
    
    try:
        day_choice = input(Fore.GREEN + "\n📅 Pilih hari (nomor): " + Fore.WHITE)
        day_index = int(day_choice) - 1
        
        if day_index < 0 or day_index >= len(days):
            show_error("Hari tidak valid.")
            return
        
        selected_day = days[day_index]
        print(Fore.GREEN + f"✅ Hari dipilih: {selected_day}")
        
        # Time input with validation
        print(Fore.YELLOW + "\n⏰ Masukkan waktu praktik:")
        start_time = get_input_with_prompt("Jam mulai (HH:MM)", "🕐")
        end_time = get_input_with_prompt("Jam selesai (HH:MM)", "🕐")
        quota = get_input_with_prompt("Kuota pasien", "👥")
        
        # Enhanced validation
        if not start_time or not end_time or not quota.isdigit():
            show_error("Input tidak valid. Pastikan format waktu HH:MM dan kuota berupa angka.")
            return
        
        if int(quota) <= 0 or int(quota) > 50:
            show_error("Kuota harus antara 1-50 pasien.")
            return
        
        # Validate time format
        try:
            start_hour, start_min = map(int, start_time.split(':'))
            end_hour, end_min = map(int, end_time.split(':'))
            
            if not (0 <= start_hour <= 23 and 0 <= start_min <= 59):
                raise ValueError
            if not (0 <= end_hour <= 23 and 0 <= end_min <= 59):
                raise ValueError
            if start_hour * 60 + start_min >= end_hour * 60 + end_min:
                show_error("Jam mulai harus lebih awal dari jam selesai.")
                return
                
        except ValueError:
            show_error("Format waktu tidak valid. Gunakan format HH:MM (contoh: 08:30)")
            return
        
        # Check for overlapping schedules
        loading = EnhancedLoadingAnimation("Memeriksa konflik jadwal", "dots")
        loading.start()
        
        schedules = read_csv("data/jadwal_dokter.csv")
        for schedule in schedules:
            if (schedule['dokter_id'] == doctor_id and 
                schedule['hari'] == selected_day and
                ((start_time >= schedule['jam_mulai'] and start_time < schedule['jam_selesai']) or
                 (end_time > schedule['jam_mulai'] and end_time <= schedule['jam_selesai']) or
                 (start_time <= schedule['jam_mulai'] and end_time >= schedule['jam_selesai']))):
                loading.stop()
                show_error(f"Jadwal bertabrakan dengan jadwal existing: {selected_day} {schedule['jam_mulai']}-{schedule['jam_selesai']}")
                return
        
        loading.stop()
        
        # Generate new schedule ID
        new_id = f"J{len(schedules) + 1:03d}"
        
        # Confirmation
        print(Fore.YELLOW + "\n📋 Konfirmasi Jadwal Baru:")
        print(Fore.CYAN + "┌─" + "─" * 40 + "┐")
        print(Fore.CYAN + f"│ ID Jadwal : {Fore.WHITE}{new_id:<26}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Dokter    : {Fore.WHITE}{doctor_name:<26}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Hari      : {Fore.WHITE}{selected_day:<26}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Waktu     : {Fore.WHITE}{start_time}-{end_time:<20}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Kuota     : {Fore.WHITE}{quota} pasien{'':<20}{Fore.CYAN} │")
        print(Fore.CYAN + "└─" + "─" * 40 + "┘")
        
        confirm = input(Fore.GREEN + "\n✅ Simpan jadwal ini? (y/n): " + Fore.WHITE).lower()
        
        if confirm != 'y':
            print(Fore.YELLOW + "❌ Jadwal dibatalkan.")
            input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
            return
        
        loading = EnhancedLoadingAnimation("Menyimpan jadwal baru", "bars")
        loading.start()
        
        # Add new schedule
        new_schedule = {
            'id': new_id,
            'dokter_id': doctor_id,
            'hari': selected_day,
            'jam_mulai': start_time,
            'jam_selesai': end_time,
            'kuota': quota
        }
        
        schedules.append(new_schedule)
        write_csv("data/jadwal_dokter.csv", schedules)
        
        loading.stop()
        
        show_success(f"Jadwal berhasil ditambahkan dengan ID {new_id}")
        
    except ValueError:
        show_error("Input tidak valid. Pastikan menggunakan angka yang benar.")
    except Exception as e:
        show_error(f"Terjadi kesalahan: {str(e)}")

def edit_doctor_schedule(doctor_id):
    """Edit doctor's schedule with enhanced UI."""
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👩‍⚕️ Dokter", "✏️ Edit Jadwal"])
    print_banner("✏️ EDIT JADWAL PRAKTIK", "yellow")
    
    # Show doctor's schedules first
    print(Fore.YELLOW + "📅 Jadwal praktik Anda:")
    schedules = read_csv("data/jadwal_dokter.csv")
    doctor_schedules = [sch for sch in schedules if sch['dokter_id'] == doctor_id]
    
    if not doctor_schedules:
        print(Fore.YELLOW + "⚠️  Anda belum memiliki jadwal praktik.")
        print(Fore.WHITE + "💡 Gunakan menu 'Tambah Jadwal' untuk membuat jadwal baru.")
        input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali...")
        return
    
    # Display doctor's schedules in a table
    table_data = []
    for i, schedule in enumerate(doctor_schedules, 1):
        table_data.append([
            str(i),
            schedule['id'],
            schedule['hari'],
            f"{schedule['jam_mulai']}-{schedule['jam_selesai']}",
            schedule['kuota']
        ])
    
    headers = ["No.", "ID", "Hari", "Waktu", "Kuota"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    schedule_id = get_input_with_prompt("ID jadwal yang akan diedit", "✏️")
    
    if not schedule_id:
        show_error("ID jadwal harus diisi.")
        return
    
    loading = EnhancedLoadingAnimation("Mencari jadwal", "dots")
    loading.start()
    
    found_schedule = None
    schedule_index = -1
    
    for i, schedule in enumerate(schedules):
        if schedule['id'] == schedule_id and schedule['dokter_id'] == doctor_id:
            found_schedule = schedule
            schedule_index = i
            break
    
    loading.stop()
    
    if not found_schedule:
        show_error("Jadwal tidak ditemukan atau bukan milik Anda.")
        return
    
    # Show current schedule info
    print(Fore.YELLOW + f"\n📋 Jadwal yang akan diedit:")
    print(Fore.CYAN + "┌─" + "─" * 40 + "┐")
    print(Fore.CYAN + f"│ ID        : {Fore.WHITE}{found_schedule['id']:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Hari      : {Fore.WHITE}{found_schedule['hari']:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Waktu     : {Fore.WHITE}{found_schedule['jam_mulai']}-{found_schedule['jam_selesai']:<20}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Kuota     : {Fore.WHITE}{found_schedule['kuota']} pasien{'':<20}{Fore.CYAN} │")
    print(Fore.CYAN + "└─" + "─" * 40 + "┘")
    
    # Check if there are active registrations
    registrations = read_csv("data/pendaftaran.csv")
    active_registrations = [r for r in registrations 
                          if r['jadwal_id'] == schedule_id and r['status'] != 'Dibatalkan']
    
    if active_registrations:
        print(Fore.YELLOW + f"\n⚠️  Terdapat {len(active_registrations)} pendaftaran aktif pada jadwal ini.")
        print(Fore.WHITE + "💡 Perubahan jadwal mungkin mempengaruhi pasien yang sudah terdaftar.")
        
        proceed = input(Fore.YELLOW + "Lanjutkan edit jadwal? (y/n): " + Fore.WHITE).lower()
        if proceed != 'y':
            print(Fore.CYAN + "Edit jadwal dibatalkan.")
            input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
            return
    
    # Day selection
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    print(Fore.YELLOW + "\n📅 Pilih hari baru:")
    print(Fore.CYAN + "┌─────┬─────────────────┐")
    print(Fore.CYAN + "│ No. │ Hari            │")
    print(Fore.CYAN + "├─────┼─────────────────┤")
    
    for i, day in enumerate(days, 1):
        current_marker = " ✓" if day == found_schedule['hari'] else ""
        print(Fore.CYAN + f"│ {Fore.WHITE}{i:2d}{Fore.CYAN}  │ 📅 {Fore.YELLOW}{day:<8}{Fore.GREEN}{current_marker:<2}{Fore.CYAN} │")
    
    print(Fore.CYAN + "└─────┴─────────────────┘")
    
    try:
        day_choice = input(Fore.GREEN + "\n📅 Pilih hari baru (nomor): " + Fore.WHITE)
        day_index = int(day_choice) - 1
        
        if day_index < 0 or day_index >= len(days):
            show_error("Hari tidak valid.")
            return
        
        selected_day = days[day_index]
        
        print(Fore.YELLOW + "\n⏰ Masukkan waktu baru (kosongkan untuk tetap sama):")
        start_time = input(Fore.GREEN + f"🕐 Jam mulai (sekarang: {found_schedule['jam_mulai']}): " + Fore.WHITE)
        end_time = input(Fore.GREEN + f"🕐 Jam selesai (sekarang: {found_schedule['jam_selesai']}): " + Fore.WHITE)
        quota = input(Fore.GREEN + f"👥 Kuota pasien (sekarang: {found_schedule['kuota']}): " + Fore.WHITE)
        
        # Use previous values if fields are left empty
        if not start_time:
            start_time = found_schedule['jam_mulai']
        if not end_time:
            end_time = found_schedule['jam_selesai']
        if not quota:
            quota = found_schedule['kuota']
        elif not quota.isdigit() or int(quota) <= 0:
            show_error("Kuota harus berupa angka positif.")
            return
        
        # Confirmation
        print(Fore.YELLOW + "\n📋 Konfirmasi Perubahan:")
        print(Fore.CYAN + "┌─" + "─" * 50 + "┐")
        print(Fore.CYAN + f"│ {'Sebelum':<24} │ {'Sesudah':<24} │")
        print(Fore.CYAN + "├─" + "─" * 24 + "┼─" + "─" * 24 + "┤")
        print(Fore.CYAN + f"│ Hari: {Fore.RED}{found_schedule['hari']:<18}{Fore.CYAN} │ Hari: {Fore.GREEN}{selected_day:<18}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Waktu: {Fore.RED}{found_schedule['jam_mulai']}-{found_schedule['jam_selesai']:<12}{Fore.CYAN} │ Waktu: {Fore.GREEN}{start_time}-{end_time:<12}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Kuota: {Fore.RED}{found_schedule['kuota']:<18}{Fore.CYAN} │ Kuota: {Fore.GREEN}{quota:<18}{Fore.CYAN} │")
        print(Fore.CYAN + "└─" + "─" * 24 + "┴─" + "─" * 24 + "┘")
        
        confirm = input(Fore.GREEN + "\n✅ Simpan perubahan? (y/n): " + Fore.WHITE).lower()
        
        if confirm != 'y':
            print(Fore.YELLOW + "❌ Perubahan dibatalkan.")
            input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
            return
        
        loading = EnhancedLoadingAnimation("Menyimpan perubahan", "bars")
        loading.start()
        
        # Update schedule
        schedules[schedule_index]['hari'] = selected_day
        schedules[schedule_index]['jam_mulai'] = start_time
        schedules[schedule_index]['jam_selesai'] = end_time
        schedules[schedule_index]['kuota'] = quota
        
        write_csv("data/jadwal_dokter.csv", schedules)
        loading.stop()
        
        show_success("Jadwal berhasil diperbarui.")
        
    except ValueError:
        show_error("Input tidak valid.")
    except Exception as e:
        show_error(f"Terjadi kesalahan: {str(e)}")

def view_registered_patients(doctor_id):
    """View patients registered for doctor's schedules with enhanced display."""
    clear_screen()
    show_breadcrumbs(["🏠 Main Menu", "👩‍⚕️ Dokter", "👥 Pasien Terdaftar"])
    
    print_data_table_header("👥 PASIEN TERDAFTAR PADA JADWAL SAYA 👥")
    
    loading = EnhancedLoadingAnimation("Memuat data pasien terdaftar", "dots")
    loading.start()
    
    # Get doctor's schedules
    schedules = read_csv("data/jadwal_dokter.csv")
    doctor_schedule_ids = [sch['id'] for sch in schedules if sch['dokter_id'] == doctor_id]
    
    if not doctor_schedule_ids:
        loading.stop()
        print(Fore.YELLOW + "⚠️  Anda tidak memiliki jadwal praktik.")
        print(Fore.WHITE + "💡 Gunakan menu 'Tambah Jadwal' untuk membuat jadwal baru.")
        input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")
        return
    
    # Get registrations for doctor's schedules
    registrations = read_csv("data/pendaftaran.csv")
    doctor_registrations = [reg for reg in registrations if reg['jadwal_id'] in doctor_schedule_ids]
    
    loading.stop()
    
    if not doctor_registrations:
        print(Fore.YELLOW + "⚠️  Belum ada pasien yang terdaftar pada jadwal Anda.")
        print(Fore.WHITE + "💡 Pasien dapat mendaftar melalui aplikasi.")
        
        print(Fore.CYAN + "\n📊 Statistik Jadwal Anda:")
        print(Fore.WHITE + f"   • Total Jadwal: {Fore.YELLOW}{len(doctor_schedule_ids)}")
        print(Fore.WHITE + f"   • Total Pendaftaran: {Fore.RED}0")
        
    else:
        # Enhanced statistics
        active_registrations = [r for r in doctor_registrations if r['status'] != 'Dibatalkan']
        canceled_registrations = [r for r in doctor_registrations if r['status'] == 'Dibatalkan']
        
        print(Fore.CYAN + "📊 Statistik Pendaftaran:")
        print(Fore.WHITE + f"   • Total Pendaftaran: {Fore.YELLOW}{len(doctor_registrations)}")
        print(Fore.WHITE + f"   • Aktif: {Fore.GREEN}{len(active_registrations)}")
        print(Fore.WHITE + f"   • Dibatalkan: {Fore.RED}{len(canceled_registrations)}")
        print()
        
        # Get schedule details
        schedule_dict = {}
        for sch in schedules:
            if sch['id'] in doctor_schedule_ids:
                schedule_dict[sch['id']] = f"{sch['hari']} {sch['jam_mulai']}-{sch['jam_selesai']}"
        
        # Convert to list of lists for tabulate
        table_data = []
        for i, reg in enumerate(doctor_registrations, 1):
            patient_name = get_patient_name(reg['pasien_id'])
            schedule_info = schedule_dict.get(reg['jadwal_id'], "Unknown")
            
            # Enhanced status display with icons
            status = reg['status']
            if status == 'Terdaftar':
                status_display = Fore.GREEN + "✅ " + status + Style.RESET_ALL
            elif status == 'Dibatalkan':
                status_display = Fore.RED + "❌ " + status + Style.RESET_ALL
            else:
                status_display = Fore.YELLOW + "⏳ " + status + Style.RESET_ALL
            
            # Format date
            try:
                date_obj = datetime.strptime(reg['tanggal'], '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d/%m/%Y')
            except:
                formatted_date = reg['tanggal']
                
            table_data.append([
                Fore.CYAN + str(i) + Style.RESET_ALL,
                Fore.GREEN + reg['id'] + Style.RESET_ALL,
                Fore.YELLOW + patient_name + Style.RESET_ALL,
                Fore.WHITE + schedule_info + Style.RESET_ALL,
                Fore.MAGENTA + formatted_date + Style.RESET_ALL,
                status_display,
                Fore.BLUE + reg['nomor_antrian'] + Style.RESET_ALL
            ])
        
        headers = [
            Fore.BLUE + Style.BRIGHT + "No." + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "ID Pendaftaran" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Nama Pasien" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Jadwal" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Tanggal" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Status" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Antrian" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        # Group by schedule for better overview
        reg_by_schedule = {}
        for reg in active_registrations:
            schedule_id = reg['jadwal_id']
            if schedule_id not in reg_by_schedule:
                reg_by_schedule[schedule_id] = []
            reg_by_schedule[schedule_id].append(reg)
        
        if reg_by_schedule:
            print_section_header("📅 RINGKASAN PER JADWAL", "📊")
            
            summary_data = []
            for schedule_id, regs in reg_by_schedule.items():
                schedule_info = schedule_dict.get(schedule_id, "Unknown")
                schedule_obj = next((s for s in schedules if s['id'] == schedule_id), None)
                quota = int(schedule_obj['kuota']) if schedule_obj else 0
                utilization = f"{len(regs)}/{quota}" if quota > 0 else f"{len(regs)}/0"
                
                utilization_pct = (len(regs) / quota * 100) if quota > 0 else 0
                if utilization_pct >= 100:
                    util_color = Fore.RED
                elif utilization_pct >= 80:
                    util_color = Fore.YELLOW
                else:
                    util_color = Fore.GREEN
                
                summary_data.append([
                    Fore.CYAN + schedule_id,
                    Fore.WHITE + schedule_info,
                    util_color + utilization + Style.RESET_ALL,
                    util_color + f"{utilization_pct:.1f}%" + Style.RESET_ALL
                ])
            
            summary_headers = ["ID Jadwal", "Hari & Waktu", "Terdaftar/Kuota", "Utilisasi"]
            print(tabulate(summary_data, headers=summary_headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")