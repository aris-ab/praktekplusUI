# modules/admin.py - Enhanced Admin functionality
import os
from tabulate import tabulate
from colorama import Fore, Style
# Perbaikan import menggunakan alias (solusi alternatif opsi 3)
import modules.data_manager as dm
import modules.data_structures.linked_list as ll
import modules.utils as utils

def admin_menu(admin_id):
    """Display enhanced admin menu and handle admin actions."""
    # Get admin info
    admin_data = None
    admins = dm.read_csv("data/admin.csv")
    for admin in admins:
        if admin['id'] == admin_id:
            admin_data = admin
            break
    
    admin_name = admin_data['nama'] if admin_data else "Admin"
    
    while True:
        utils.clear_screen()
        utils.show_breadcrumbs(["🏠 Main Menu", "👨‍💼 Admin Dashboard"])
        
        # Enhanced admin header
        print(Fore.CYAN + "╔" + "═" * 80 + "╗")
        print(Fore.CYAN + "║" + " " * 80 + "║")
        print(Fore.CYAN + "║" + Fore.YELLOW + Style.BRIGHT + f"       👨‍💼 DASHBOARD ADMINISTRASI - {admin_name} 👨‍💼       ".center(80) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + "                    🏥 Kelola Sistem Klinik dengan Mudah 🏥                    " + "║")
        print(Fore.CYAN + "║" + " " * 80 + "║")
        print(Fore.CYAN + "╠" + "═" * 80 + "╣")
        
        # Enhanced menu options
        print(Fore.CYAN + "║  " + Fore.GREEN + "📅 1." + Fore.YELLOW + " Lihat Semua Jadwal Dokter                                    " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "➕ 2." + Fore.YELLOW + " Tambah Jadwal Dokter Baru                                    " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "✏️  3." + Fore.YELLOW + " Edit Jadwal Dokter                                           " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "🗑️  4." + Fore.YELLOW + " Hapus Jadwal Dokter                                          " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "👥 5." + Fore.YELLOW + " Lihat Data Pasien Terdaftar                                 " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "📝 6." + Fore.YELLOW + " Lihat Pendaftaran Konsultasi                                " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.GREEN + "📊 7." + Fore.YELLOW + " Lihat Statistik & Analisis Klinik                           " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.RED + "🚪 8." + Fore.YELLOW + " Logout dari Dashboard                                        " + Fore.CYAN + "║")
        print(Fore.CYAN + "║  " + Fore.BLUE + "❓ ?." + Fore.YELLOW + " Bantuan & Panduan Admin                                      " + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + " " * 80 + "║")
        print(Fore.CYAN + "╚" + "═" * 80 + "╝")
        
        choice = input(Fore.GREEN + "\n➤ Pilihan Anda: " + Fore.WHITE)
        
        if choice == "1":
            view_all_schedules()
        elif choice == "2":
            add_doctor_schedule()
        elif choice == "3":
            edit_doctor_schedule()
        elif choice == "4":
            delete_doctor_schedule()
        elif choice == "5":
            view_patient_data()
        elif choice == "6":
            view_all_registrations()
        elif choice == "7":
            view_clinic_statistics()
        elif choice == "8":
            print(Fore.CYAN + "👋 Logout berhasil. Sampai jumpa!")
            break
        elif choice == "?":
            utils.show_help("admin")
        else:
            utils.show_error("Pilihan tidak valid. Silakan pilih 1-8 atau ?")

def view_all_schedules():
    """View all doctor schedules with enhanced display."""
    utils.clear_screen()
    utils.show_breadcrumbs(["🏠 Main Menu", "👨‍💼 Admin", "📅 Lihat Jadwal"])
    
    utils.print_data_table_header("📅 JADWAL PRAKTIK SEMUA DOKTER 📅")
    
    loading = utils.EnhancedLoadingAnimation("Memuat data jadwal dokter", "dots")
    loading.start()
    
    schedules = dm.read_csv("data/jadwal_dokter.csv")
    doctors = dm.read_csv("data/dokter.csv")
    
    # Create doctor dictionary for quick lookup
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = {
            'nama': doctor['nama'], 
            'spesialisasi': doctor['spesialisasi']
        }
    
    # Create linked list to store schedule data
    schedule_list = ll.LinkedList()
    for schedule in schedules:
        doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
        schedule_data = {
            'id': schedule['id'],
            'dokter': f"{doctor_info['nama']} ({doctor_info['spesialisasi']})",
            'hari': schedule['hari'],
            'waktu': f"{schedule['jam_mulai']} - {schedule['jam_selesai']}",
            'kuota': schedule['kuota']
        }
        schedule_list.append(schedule_data)
    
    loading.stop()
    
    # Display schedules
    all_schedules = schedule_list.display()
    if not all_schedules:
        print(Fore.YELLOW + "⚠️  Tidak ada jadwal yang tersedia.")
        print(Fore.WHITE + "💡 Gunakan menu 'Tambah Jadwal' untuk menambah jadwal baru.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for schedule in all_schedules:
            table_data.append([
                Fore.CYAN + schedule['id'] + Style.RESET_ALL,
                Fore.GREEN + schedule['dokter'] + Style.RESET_ALL, 
                Fore.YELLOW + schedule['hari'] + Style.RESET_ALL, 
                Fore.WHITE + schedule['waktu'] + Style.RESET_ALL, 
                Fore.MAGENTA + schedule['kuota'] + Style.RESET_ALL
            ])
        
        headers = [
            Fore.BLUE + Style.BRIGHT + "ID Jadwal" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Dokter (Spesialisasi)" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Hari" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Waktu" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Kuota" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        print(Fore.CYAN + f"\n📊 Total Jadwal: {Fore.YELLOW}{len(all_schedules)} jadwal")
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")

def add_doctor_schedule():
    """Add a new doctor schedule with enhanced UI."""
    utils.clear_screen()
    utils.show_breadcrumbs(["🏠 Main Menu", "👨‍💼 Admin", "➕ Tambah Jadwal"])
    utils.print_banner("➕ TAMBAH JADWAL DOKTER BARU", "green")
    
    # Show available doctors
    doctors = dm.read_csv("data/dokter.csv")
    
    if not doctors:
        utils.show_error("Tidak ada data dokter. Hubungi administrator sistem.")
        return
    
    print(Fore.YELLOW + "👩‍⚕️ Dokter yang tersedia:")
    print(Fore.CYAN + "┌─────┬─────────────────────────────────────────┐")
    print(Fore.CYAN + "│ No. │ Dokter & Spesialisasi                   │")
    print(Fore.CYAN + "├─────┼─────────────────────────────────────────┤")
    
    for i, doctor in enumerate(doctors, 1):
        doctor_text = f"{doctor['nama']} - {doctor['spesialisasi']}"
        print(Fore.CYAN + f"│ {Fore.WHITE}{i:2d}{Fore.CYAN}  │ {Fore.GREEN}{doctor_text:<39}{Fore.CYAN} │")
    
    print(Fore.CYAN + "└─────┴─────────────────────────────────────────┘")
    
    try:
        doctor_choice = input(Fore.GREEN + "\n👨‍⚕️ Pilih dokter (nomor): " + Fore.WHITE)
        doctor_index = int(doctor_choice) - 1
        
        if doctor_index < 0 or doctor_index >= len(doctors):
            utils.show_error("Dokter tidak ditemukan.")
            return
        
        selected_doctor = doctors[doctor_index]
        doctor_id = selected_doctor['id']
        
        print(Fore.GREEN + f"\n✅ Dokter dipilih: {selected_doctor['nama']} ({selected_doctor['spesialisasi']})")
        
        # Day selection with enhanced UI
        days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
        day_icons = ["📅", "📅", "📅", "📅", "📅", "📅"]
        
        print(Fore.YELLOW + "\n📅 Hari yang tersedia:")
        print(Fore.CYAN + "┌─────┬─────────────┐")
        print(Fore.CYAN + "│ No. │ Hari        │")
        print(Fore.CYAN + "├─────┼─────────────┤")
        
        for i, day in enumerate(days, 1):
            print(Fore.CYAN + f"│ {Fore.WHITE}{i:2d}{Fore.CYAN}  │ {day_icons[i-1]} {Fore.YELLOW}{day:<8}{Fore.CYAN} │")
        
        print(Fore.CYAN + "└─────┴─────────────┘")
        
        day_choice = input(Fore.GREEN + "\n📅 Pilih hari (nomor): " + Fore.WHITE)
        day_index = int(day_choice) - 1
        
        if day_index < 0 or day_index >= len(days):
            utils.show_error("Hari tidak valid.")
            return
        
        selected_day = days[day_index]
        print(Fore.GREEN + f"✅ Hari dipilih: {selected_day}")
        
        # Time input with validation
        print(Fore.YELLOW + "\n⏰ Masukkan waktu praktik:")
        start_time = utils.get_input_with_prompt("Jam mulai (HH:MM)", "🕐")
        end_time = utils.get_input_with_prompt("Jam selesai (HH:MM)", "🕐")
        quota = utils.get_input_with_prompt("Kuota pasien", "👥")
        
        # Enhanced validation
        if not start_time or not end_time or not quota.isdigit():
            utils.show_error("Input tidak valid. Pastikan format waktu HH:MM dan kuota berupa angka.")
            return
        
        if int(quota) <= 0:
            utils.show_error("Kuota harus lebih dari 0.")
            return
        
        # Check for time conflicts
        loading = utils.EnhancedLoadingAnimation("Memeriksa konflik jadwal", "dots")
        loading.start()
        
        schedules = dm.read_csv("data/jadwal_dokter.csv")
        for schedule in schedules:
            if (schedule['dokter_id'] == doctor_id and 
                schedule['hari'] == selected_day):
                # Simple time overlap check
                existing_start = schedule['jam_mulai']
                existing_end = schedule['jam_selesai']
                
                if ((start_time >= existing_start and start_time < existing_end) or
                    (end_time > existing_start and end_time <= existing_end) or
                    (start_time <= existing_start and end_time >= existing_end)):
                    loading.stop()
                    utils.show_error(f"Jadwal bertabrakan dengan jadwal existing: {selected_day} {existing_start}-{existing_end}")
                    return
        
        loading.stop()
        
        # Generate new schedule ID
        new_id = f"J{len(schedules) + 1:03d}"
        
        # Confirmation
        print(Fore.YELLOW + "\n📋 Konfirmasi Jadwal Baru:")
        print(Fore.CYAN + "┌─" + "─" * 40 + "┐")
        print(Fore.CYAN + f"│ ID Jadwal : {Fore.WHITE}{new_id:<26}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Dokter    : {Fore.WHITE}{selected_doctor['nama']:<26}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Hari      : {Fore.WHITE}{selected_day:<26}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Waktu     : {Fore.WHITE}{start_time}-{end_time:<20}{Fore.CYAN} │")
        print(Fore.CYAN + f"│ Kuota     : {Fore.WHITE}{quota} pasien{'':<20}{Fore.CYAN} │")
        print(Fore.CYAN + "└─" + "─" * 40 + "┘")
        
        confirm = input(Fore.GREEN + "\n✅ Simpan jadwal ini? (y/n): " + Fore.WHITE).lower()
        
        if confirm != 'y':
            print(Fore.YELLOW + "❌ Jadwal dibatalkan.")
            input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
            return
        
        loading = utils.EnhancedLoadingAnimation("Menyimpan jadwal baru", "bars")
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
        dm.write_csv("data/jadwal_dokter.csv", schedules)
        
        loading.stop()
        
        utils.show_success(f"Jadwal berhasil ditambahkan dengan ID {new_id}")
        
    except ValueError:
        utils.show_error("Input tidak valid. Pastikan menggunakan angka yang benar.")
    except Exception as e:
        utils.show_error(f"Terjadi kesalahan: {str(e)}")

# Continue with remaining admin functions...
def edit_doctor_schedule():
    """Edit an existing doctor schedule with enhanced UI."""
    utils.clear_screen()
    utils.show_breadcrumbs(["🏠 Main Menu", "👨‍💼 Admin", "✏️ Edit Jadwal"])
    utils.print_banner("✏️ EDIT JADWAL DOKTER", "yellow")
    
    # Show existing schedules first
    print(Fore.YELLOW + "📅 Jadwal yang tersedia untuk diedit:")
    view_all_schedules()
    
    schedule_id = utils.get_input_with_prompt("ID jadwal yang akan diedit", "🆔")
    
    if not schedule_id:
        utils.show_error("ID jadwal harus diisi.")
        return
    
    loading = utils.EnhancedLoadingAnimation("Mencari jadwal", "dots")
    loading.start()
    
    schedules = dm.read_csv("data/jadwal_dokter.csv")
    found_schedule = None
    schedule_index = -1
    
    for i, schedule in enumerate(schedules):
        if schedule['id'] == schedule_id:
            found_schedule = schedule
            schedule_index = i
            break
    
    loading.stop()
    
    if not found_schedule:
        utils.show_error("Jadwal tidak ditemukan.")
        return
    
    # Get doctor info
    doctors = dm.read_csv("data/dokter.csv")
    doctor_name = "Unknown"
    for doctor in doctors:
        if doctor['id'] == found_schedule['dokter_id']:
            doctor_name = f"{doctor['nama']} ({doctor['spesialisasi']})"
            break
    
    # Show current schedule info
    print(Fore.YELLOW + f"\n📋 Jadwal yang akan diedit:")
    print(Fore.CYAN + "┌─" + "─" * 40 + "┐")
    print(Fore.CYAN + f"│ ID        : {Fore.WHITE}{found_schedule['id']:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Dokter    : {Fore.WHITE}{doctor_name:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Hari      : {Fore.WHITE}{found_schedule['hari']:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Waktu     : {Fore.WHITE}{found_schedule['jam_mulai']}-{found_schedule['jam_selesai']:<20}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Kuota     : {Fore.WHITE}{found_schedule['kuota']} pasien{'':<20}{Fore.CYAN} │")
    print(Fore.CYAN + "└─" + "─" * 40 + "┘")
    
    # Day selection
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    print(Fore.YELLOW + "\n📅 Pilih hari baru:")
    print(Fore.CYAN + "┌─────┬─────────────┐")
    print(Fore.CYAN + "│ No. │ Hari        │")
    print(Fore.CYAN + "├─────┼─────────────┤")
    
    for i, day in enumerate(days, 1):
        current_marker = " ✓" if day == found_schedule['hari'] else ""
        print(Fore.CYAN + f"│ {Fore.WHITE}{i:2d}{Fore.CYAN}  │ 📅 {Fore.YELLOW}{day:<8}{Fore.GREEN}{current_marker:<2}{Fore.CYAN} │")
    
    print(Fore.CYAN + "└─────┴─────────────┘")
    
    try:
        day_choice = input(Fore.GREEN + "\n📅 Pilih hari baru (nomor): " + Fore.WHITE)
        day_index = int(day_choice) - 1
        
        if day_index < 0 or day_index >= len(days):
            utils.show_error("Hari tidak valid.")
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
            utils.show_error("Kuota harus berupa angka positif.")
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
        
        loading = utils.EnhancedLoadingAnimation("Menyimpan perubahan", "bars")
        loading.start()
        
        # Update schedule
        schedules[schedule_index]['hari'] = selected_day
        schedules[schedule_index]['jam_mulai'] = start_time
        schedules[schedule_index]['jam_selesai'] = end_time
        schedules[schedule_index]['kuota'] = quota
        
        dm.write_csv("data/jadwal_dokter.csv", schedules)
        loading.stop()
        
        utils.show_success("Jadwal berhasil diperbarui.")
        
    except ValueError:
        utils.show_error("Input tidak valid.")
    except Exception as e:
        utils.show_error(f"Terjadi kesalahan: {str(e)}")

# Continuation of modules/admin.py - Remaining admin functions

def delete_doctor_schedule():
    """Delete a doctor schedule with enhanced UI and safety checks."""
    utils.clear_screen()
    utils.show_breadcrumbs(["🏠 Main Menu", "👨‍💼 Admin", "🗑️ Hapus Jadwal"])
    utils.print_banner("🗑️ HAPUS JADWAL DOKTER", "red")
    
    print(Fore.RED + "⚠️  " + Style.BRIGHT + "PERINGATAN: Aksi ini tidak dapat dibatalkan!")
    print(Fore.YELLOW + "💡 Pastikan tidak ada pendaftaran aktif sebelum menghapus jadwal.")
    print()
    
    # Show existing schedules
    print(Fore.YELLOW + "📅 Jadwal yang tersedia:")
    view_all_schedules()
    
    schedule_id = utils.get_input_with_prompt("ID jadwal yang akan dihapus", "🗑️")
    
    if not schedule_id:
        utils.show_error("ID jadwal harus diisi.")
        return
    
    loading = utils.EnhancedLoadingAnimation("Memeriksa jadwal dan pendaftaran", "dots")
    loading.start()
    
    schedules = dm.read_csv("data/jadwal_dokter.csv")
    registrations = dm.read_csv("data/pendaftaran.csv")
    
    # Find the schedule
    target_schedule = None
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            target_schedule = schedule
            break
    
    if not target_schedule:
        loading.stop()
        utils.show_error("Jadwal tidak ditemukan.")
        return
    
    # Get doctor info
    doctors = dm.read_csv("data/dokter.csv")
    doctor_name = "Unknown"
    for doctor in doctors:
        if doctor['id'] == target_schedule['dokter_id']:
            doctor_name = f"{doctor['nama']} ({doctor['spesialisasi']})"
            break
    
    # Check for active registrations
    active_registrations = [reg for reg in registrations 
                           if reg['jadwal_id'] == schedule_id and reg['status'] != 'Dibatalkan']
    
    loading.stop()
    
    # Show schedule details
    print(Fore.RED + f"\n🗑️ Jadwal yang akan dihapus:")
    print(Fore.CYAN + "┌─" + "─" * 40 + "┐")
    print(Fore.CYAN + f"│ ID        : {Fore.WHITE}{target_schedule['id']:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Dokter    : {Fore.WHITE}{doctor_name:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Hari      : {Fore.WHITE}{target_schedule['hari']:<26}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Waktu     : {Fore.WHITE}{target_schedule['jam_mulai']}-{target_schedule['jam_selesai']:<20}{Fore.CYAN} │")
    print(Fore.CYAN + f"│ Kuota     : {Fore.WHITE}{target_schedule['kuota']} pasien{'':<20}{Fore.CYAN} │")
    print(Fore.CYAN + "└─" + "─" * 40 + "┘")
    
    if active_registrations:
        print(Fore.RED + f"\n❌ TIDAK DAPAT MENGHAPUS!")
        print(Fore.YELLOW + f"⚠️  Terdapat {len(active_registrations)} pendaftaran aktif pada jadwal ini.")
        print(Fore.WHITE + "💡 Batalkan semua pendaftaran terlebih dahulu atau tunggu hingga selesai.")
        
        print(Fore.CYAN + "\n📋 Pendaftaran aktif:")
        for i, reg in enumerate(active_registrations[:5], 1):  # Show max 5
            patient_name = dm.get_patient_name(reg['pasien_id'])
            print(Fore.WHITE + f"   {i}. {patient_name} - {reg['tanggal']} (Antrian {reg['nomor_antrian']})")
        
        if len(active_registrations) > 5:
            print(Fore.WHITE + f"   ... dan {len(active_registrations) - 5} pendaftaran lainnya")
        
        input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali...")
        return
    
    # Final confirmation
    print(Fore.GREEN + "\n✅ Jadwal dapat dihapus (tidak ada pendaftaran aktif)")
    print(Fore.RED + "⚠️  Apakah Anda yakin ingin menghapus jadwal ini?")
    
    confirm1 = input(Fore.YELLOW + "Ketik 'HAPUS' untuk konfirmasi: " + Fore.WHITE)
    
    if confirm1 != 'HAPUS':
        print(Fore.YELLOW + "❌ Penghapusan dibatalkan.")
        input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
        return
    
    confirm2 = input(Fore.RED + "Apakah Anda benar-benar yakin? (y/n): " + Fore.WHITE).lower()
    
    if confirm2 != 'y':
        print(Fore.YELLOW + "❌ Penghapusan dibatalkan.")
        input(Fore.GREEN + "⏎ Tekan Enter untuk kembali...")
        return
    
    loading = utils.EnhancedLoadingAnimation("Menghapus jadwal", "bars")
    loading.start()
    
    # Remove schedule
    updated_schedules = [sch for sch in schedules if sch['id'] != schedule_id]
    dm.write_csv("data/jadwal_dokter.csv", updated_schedules)
    
    loading.stop()
    
    utils.show_success("Jadwal berhasil dihapus.")

def view_patient_data():
    """View registered patients with enhanced display."""
    utils.clear_screen()
    utils.show_breadcrumbs(["🏠 Main Menu", "👨‍💼 Admin", "👥 Data Pasien"])
    
    utils.print_data_table_header("👥 DATA PASIEN TERDAFTAR 👥")
    
    loading = utils.EnhancedLoadingAnimation("Memuat data pasien", "dots")
    loading.start()
    
    patients = dm.read_csv("data/pasien.csv")
    
    loading.stop()
    
    if not patients:
        print(Fore.YELLOW + "⚠️  Tidak ada data pasien terdaftar.")
        print(Fore.WHITE + "💡 Pasien dapat mendaftar melalui menu 'Registrasi' di halaman utama.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for i, patient in enumerate(patients, 1):
            table_data.append([
                Fore.CYAN + str(i) + Style.RESET_ALL,
                Fore.GREEN + patient['id'] + Style.RESET_ALL,
                Fore.YELLOW + patient['nama'] + Style.RESET_ALL,
                Fore.WHITE + patient['username'] + Style.RESET_ALL,
                Fore.MAGENTA + patient['kontak'] + Style.RESET_ALL
            ])
        
        headers = [
            Fore.BLUE + Style.BRIGHT + "No." + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "ID Pasien" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Nama Lengkap" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Username" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Kontak" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        print(Fore.CYAN + f"\n📊 Total Pasien Terdaftar: {Fore.YELLOW}{len(patients)} pasien")
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")

def view_all_registrations():
    """View all consultation registrations with enhanced display."""
    utils.clear_screen()
    utils.show_breadcrumbs(["🏠 Main Menu", "👨‍💼 Admin", "📝 Data Pendaftaran"])
    
    utils.print_data_table_header("📝 DATA PENDAFTARAN KONSULTASI 📝")
    
    loading = utils.EnhancedLoadingAnimation("Memuat data pendaftaran", "dots")
    loading.start()
    
    registrations = dm.read_csv("data/pendaftaran.csv")
    
    loading.stop()
    
    if not registrations:
        print(Fore.YELLOW + "⚠️  Tidak ada data pendaftaran.")
        print(Fore.WHITE + "💡 Pasien dapat mendaftar konsultasi melalui menu pasien.")
    else:
        # Enhanced statistics
        total_reg = len(registrations)
        active_reg = len([r for r in registrations if r['status'] != 'Dibatalkan'])
        canceled_reg = len([r for r in registrations if r['status'] == 'Dibatalkan'])
        
        print(Fore.CYAN + "📊 Statistik Pendaftaran:")
        print(Fore.WHITE + f"   • Total: {Fore.YELLOW}{total_reg}")
        print(Fore.WHITE + f"   • Aktif: {Fore.GREEN}{active_reg}")
        print(Fore.WHITE + f"   • Dibatalkan: {Fore.RED}{canceled_reg}")
        print()
        
        # Convert to list of lists for tabulate
        table_data = []
        for i, reg in enumerate(registrations, 1):
            patient_name = dm.get_patient_name(reg['pasien_id'])
            schedule_details = dm.get_schedule_details(reg['jadwal_id'])
            
            # Enhanced status display
            status = reg['status']
            if status == 'Terdaftar':
                status_display = Fore.GREEN + "✅ " + status + Style.RESET_ALL
            elif status == 'Dibatalkan':
                status_display = Fore.RED + "❌ " + status + Style.RESET_ALL
            else:
                status_display = Fore.YELLOW + "⏳ " + status + Style.RESET_ALL
            
            table_data.append([
                Fore.CYAN + str(i) + Style.RESET_ALL,
                Fore.GREEN + reg['id'] + Style.RESET_ALL,
                Fore.YELLOW + patient_name + Style.RESET_ALL,
                Fore.WHITE + schedule_details + Style.RESET_ALL,
                Fore.MAGENTA + reg['tanggal'] + Style.RESET_ALL,
                status_display,
                Fore.BLUE + reg['nomor_antrian'] + Style.RESET_ALL
            ])
        
        headers = [
            Fore.BLUE + Style.BRIGHT + "No." + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "ID" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Pasien" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Dokter & Jadwal" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Tanggal" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Status" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Antrian" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")

def view_clinic_statistics():
    """View comprehensive clinic statistics with enhanced visualization."""
    utils.clear_screen()
    utils.show_breadcrumbs(["🏠 Main Menu", "👨‍💼 Admin", "📊 Statistik"])
    
    utils.print_banner("📊 STATISTIK & ANALISIS KLINIK", "magenta")
    
    loading = utils.EnhancedLoadingAnimation("Menganalisis data klinik", "bars")
    loading.start()
    
    schedules = dm.read_csv("data/jadwal_dokter.csv")
    doctors = dm.read_csv("data/dokter.csv")
    patients = dm.read_csv("data/pasien.csv")
    registrations = dm.read_csv("data/pendaftaran.csv")
    
    # Calculate statistics
    active_registrations = [reg for reg in registrations if reg['status'] != 'Dibatalkan']
    canceled_registrations = [reg for reg in registrations if reg['status'] == 'Dibatalkan']
    
    # Count registrations by day
    reg_by_day = {}
    for reg in active_registrations:
        schedule_id = reg['jadwal_id']
        day = None
        for sch in schedules:
            if sch['id'] == schedule_id:
                day = sch['hari']
                break
        
        if day:
            reg_by_day[day] = reg_by_day.get(day, 0) + 1
    
    # Count registrations by doctor
    reg_by_doctor = {}
    for reg in active_registrations:
        schedule_id = reg['jadwal_id']
        doctor_id = None
        for sch in schedules:
            if sch['id'] == schedule_id:
                doctor_id = sch['dokter_id']
                break
        
        if doctor_id:
            doctor_name = None
            for doc in doctors:
                if doc['id'] == doctor_id:
                    doctor_name = doc['nama']
                    break
            
            if doctor_name:
                reg_by_doctor[doctor_name] = reg_by_doctor.get(doctor_name, 0) + 1
    
    # Count by specialty
    reg_by_specialty = {}
    for reg in active_registrations:
        schedule_id = reg['jadwal_id']
        doctor_id = None
        for sch in schedules:
            if sch['id'] == schedule_id:
                doctor_id = sch['dokter_id']
                break
        
        if doctor_id:
            specialty = None
            for doc in doctors:
                if doc['id'] == doctor_id:
                    specialty = doc['spesialisasi']
                    break
            
            if specialty:
                reg_by_specialty[specialty] = reg_by_specialty.get(specialty, 0) + 1
    
    loading.stop()
    
    # Display enhanced statistics
    print(Fore.CYAN + "╔" + "═" * 60 + "╗")
    print(Fore.CYAN + "║" + Fore.YELLOW + Style.BRIGHT + "              📈 RINGKASAN STATISTIK              ".center(60) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 60 + "╣")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "║ " + Fore.GREEN + f"👩‍⚕️ Total Dokter:" + f"{len(doctors):>38}" + Fore.CYAN + " ║")
    print(Fore.CYAN + "║ " + Fore.GREEN + f"👥 Total Pasien:" + f"{len(patients):>38}" + Fore.CYAN + " ║")
    print(Fore.CYAN + "║ " + Fore.GREEN + f"📅 Total Jadwal:" + f"{len(schedules):>38}" + Fore.CYAN + " ║")
    print(Fore.CYAN + "║ " + Fore.GREEN + f"📝 Pendaftaran Aktif:" + f"{len(active_registrations):>31}" + Fore.CYAN + " ║")
    print(Fore.CYAN + "║ " + Fore.RED + f"❌ Pendaftaran Dibatalkan:" + f"{len(canceled_registrations):>27}" + Fore.CYAN + " ║")
    print(Fore.CYAN + "║" + " " * 60 + "║")
    print(Fore.CYAN + "╚" + "═" * 60 + "╝")
    
    # Registrations by day
    if reg_by_day:
        utils.print_section_header("📅 PENDAFTARAN PER HARI", "📊")
        table_data = []
        for day, count in sorted(reg_by_day.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(active_registrations)) * 100 if active_registrations else 0
            bar = "█" * min(int(percentage / 5), 20)  # Visual bar
            table_data.append([
                Fore.YELLOW + day,
                Fore.WHITE + str(count),
                Fore.GREEN + f"{percentage:.1f}%",
                Fore.CYAN + bar + Style.RESET_ALL
            ])
        
        headers = ["Hari", "Jumlah", "Persentase", "Visualisasi"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    # Registrations by doctor
    if reg_by_doctor:
        utils.print_section_header("👩‍⚕️ PENDAFTARAN PER DOKTER", "📊")
        table_data = []
        for doctor, count in sorted(reg_by_doctor.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(active_registrations)) * 100 if active_registrations else 0
            bar = "█" * min(int(percentage / 5), 20)
            table_data.append([
                Fore.GREEN + doctor,
                Fore.WHITE + str(count),
                Fore.YELLOW + f"{percentage:.1f}%",
                Fore.CYAN + bar + Style.RESET_ALL
            ])
        
        headers = ["Dokter", "Jumlah", "Persentase", "Visualisasi"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    # Registrations by specialty
    if reg_by_specialty:
        utils.print_section_header("🏥 PENDAFTARAN PER SPESIALISASI", "📊")
        table_data = []
        for specialty, count in sorted(reg_by_specialty.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(active_registrations)) * 100 if active_registrations else 0
            bar = "█" * min(int(percentage / 5), 20)
            table_data.append([
                Fore.MAGENTA + specialty,
                Fore.WHITE + str(count),
                Fore.YELLOW + f"{percentage:.1f}%",
                Fore.CYAN + bar + Style.RESET_ALL
            ])
        
        headers = ["Spesialisasi", "Jumlah", "Persentase", "Visualisasi"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    if not reg_by_day and not reg_by_doctor:
        print(Fore.YELLOW + "\n⚠️  Belum ada data pendaftaran untuk dianalisis.")
        print(Fore.WHITE + "💡 Statistik akan muncul setelah ada pendaftaran konsultasi.")
    
    print(Fore.CYAN + "\n" + "═" * 80)
    input(Fore.GREEN + "\n⏎ Tekan Enter untuk kembali ke menu...")