import os
import csv
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.core.window import Window
import platform

# File data
DATA_FILE = "absensi_guru.csv"

# Daftar guru
DAFTAR_GURU = ["H. M. Sukarmawijaya, S.Pd", "H. Azis Muslim, S.Pd.I", "Drs. H. R. Bichri, M.M", "Fanny Pandini Septiani, S.Pd., Gr.", "Ida Nuribar, S.Pd.I", "Ade Sukmana, S.Pd., Gr.", "Nilawati, S.Pd", "Sahada Azhar, S.Pd.I", "Nuraeni, S.Pd", "Ririn Ashshofa, S.Si, Gr.", "Santi Saparina Yasrifah, M.Pd", "Arif Priyono, S.S", "Riska Indriani", "Firhans Jan Hardianto, S.T", "Elsa Sandrianis Prawira", "Andini Mutiara Rahman, S.Pd., Gr."]

# Daftar mata pelajaran
DAFTAR_MAPEL = ["PAIBP", "Seni Budaya", "IPA Fisika", "B. Indonesia", "IPA Kimia", "IPS Sejarah", "Matematika Wajib", "IPS Ekonomi", "IPA Biologi", "IPS Sosiologi", "PJOK", "B. Inggris", "PSPJ PGRI", "Pend. Pancasila", "Basa Sunda", "IPS Geografi", "Informatika", "PABP", "Fisika", "Sejarah Indonesia", "Biologi", "Sosiologi", "Matematika TL"]

class AttendanceApp(App):
    def build(self):
        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50))
        header.add_widget(Label(
            text="SISTEM ABSENSI GURU", 
            font_size=dp(24), 
            bold=True,
            color=(1, 1, 1, 1) #putih
        ))
        self.layout.add_widget(header)
        
        # Input section
        input_layout = GridLayout(
            cols=2, 
            size_hint_y=None, 
            height=dp(150), 
            spacing=dp(10), 
            row_force_default=True, 
            row_default_height=dp(40)
        )
        
        # Input Guru
        input_layout.add_widget(Label(
            text="Nama Guru:",
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=None,
            height=dp(40)
        ))
        self.guru_spinner = Spinner(
            text='Pilih Guru',
            values=DAFTAR_GURU,
            size_hint_y=None,
            height=dp(40),
            color=(0, 0, 0, 1),
            font_size=dp(14))
        input_layout.add_widget(self.guru_spinner)
        
        # Input Mata Pelajaran
        input_layout.add_widget(Label(
            text="Mata Pelajaran:",
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=None,
            height=dp(40)
        ))
        self.mapel_spinner = Spinner(
            text='Pilih Mapel',
            values=DAFTAR_MAPEL,
            size_hint_y=None,
            height=dp(40),
            color=(0, 0, 0, 1),
            font_size=dp(14))
        input_layout.add_widget(self.mapel_spinner)
        
        # Input Jam Pelajaran
        input_layout.add_widget(Label(
            text="Jam Pelajaran:",
            bold=True,
            color=(1, 1, 0, 1),
            size_hint_y=None,
            height=dp(40)
        ))
        self.jam_spinner = Spinner(
            text='Pilih Jam', 
            values=[f"Jam ke-{i}" for i in range(1, 9)],
            size_hint_y=None,
            height=dp(40),
            color=(0, 0, 0, 1),
            font_size=dp(14))
        input_layout.add_widget(self.jam_spinner)
        
        self.layout.add_widget(input_layout)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.hadir_btn = Button(
            text="HADIR", 
            background_color=(0, 0.7, 0, 1),
            on_press=self.catat_kehadiran,
            color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(16))
        btn_layout.add_widget(self.hadir_btn)
        
        self.tidak_hadir_btn = Button(
            text="TIDAK HADIR", 
            background_color=(0.8, 0, 0, 1),
            on_press=self.catat_ketidakhadiran,
            color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(16))
        btn_layout.add_widget(self.tidak_hadir_btn)
        
        self.layout.add_widget(btn_layout)
        
        # TAMBAHKAN TOMBOL HAPUS RIWAYAT DI SINI
        self.hapus_btn = Button(
            text="HAPUS RIWAYAT", 
            background_color=(0.8, 0.8, 0, 1),
            on_press=self.konfirmasi_hapus_riwayat,
            color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(40))
        self.layout.add_widget(self.hapus_btn)
        
        # Attendance history
        history_header = BoxLayout(size_hint_y=None, height=dp(30))
        history_header.add_widget(Label(
            text="RIWAYAT ABSENSI", 
            bold=True,
            color=(1, 1, 1, 1),
            font_size=dp(16)))
        self.layout.add_widget(history_header)
        
        # Tabel riwayat absensi
        table_container = BoxLayout(orientation='vertical', size_hint_y=1)
        
        # Header tabel
        header_layout = GridLayout(
            cols=5, 
            size_hint_y=None, 
            height=dp(40), 
            spacing=dp(5),
            row_force_default=True,
            row_default_height=dp(40))
        
        headers = ["Tanggal", "Guru", "Mapel", "Jam", "Status"]
        for header in headers:
            header_layout.add_widget(Label(
                text=header, 
                bold=True, 
                color=(0, 0.8, 0, 1),
                font_size=dp(14))
        )
        table_container.add_widget(header_layout)
        
        # Scrollable history
        scroll = ScrollView()
        self.history_layout = GridLayout(
            cols=5, 
            spacing=dp(5), 
            size_hint_y=None,
            padding=[dp(5), dp(5), dp(5), dp(5)])
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        
        scroll.add_widget(self.history_layout)
        table_container.add_widget(scroll)
        self.layout.add_widget(table_container)
        
        # Load existing data
        self.load_data()
        
        return self.layout
    
    def load_data(self):
        # Create file if not exists
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Tanggal", "Nama", "Mapel", "Jam", "Status"])
        
        # Clear existing widgets
        self.history_layout.clear_widgets()
        
        # Load data from CSV
        try:
            with open(DATA_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 5:
                        # Format tanggal untuk tampilan lebih pendek
                        date_parts = row[0].split()
                        short_date = f"{date_parts[0]}\n{date_parts[1]}" if len(date_parts) > 1 else row[0]
                        
                        # Tambahkan data ke tabel
                        self.history_layout.add_widget(Label(
                            text=short_date, 
                            color=(0, 0.8, 0, 1),
                            font_size=dp(12),
                            halign='center',
                            valign='middle',
                            size_hint_y=None,
                            height=dp(40))
                            )
                        self.history_layout.add_widget(Label(
                            text=row[1], 
                            color=(0, 0.8, 0, 1),
                            font_size=dp(12),
                            halign='center',
                            valign='middle',
                            size_hint_y=None,
                            height=dp(40))
                            )
                        self.history_layout.add_widget(Label(
                            text=row[2], 
                            color=(1, 1, 0, 1),
                            font_size=dp(12),
                            halign='center',
                            valign='middle',
                            size_hint_y=None,
                            height=dp(40))
                            )
                        self.history_layout.add_widget(Label(
                            text=row[3], 
                            color=(0, 0.8, 0, 1),
                            font_size=dp(12),
                            halign='center',
                            valign='middle',
                            size_hint_y=None,
                            height=dp(40))
                            )
                        status_color = (0, 0.7, 0, 1) if row[4] == "Hadir" else (0.8, 0, 0, 1)
                        self.history_layout.add_widget(Label(
                            text=row[4], 
                            color=status_color, 
                            bold=True,
                            font_size=dp(12),
                            halign='center',
                            valign='middle',
                            size_hint_y=None,
                            height=dp(40))
                            )
        except Exception as e:
            self.show_popup("Error", f"Gagal memuat data: {str(e)}")
    
    # TAMBAHKAN FUNGSI UNTUK HAPUS RIWAYAT
    def konfirmasi_hapus_riwayat(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(
            text="Apakah Anda yakin ingin menghapus semua riwayat absensi?",
            color=(0, 0, 0, 1),
            halign='center'
        ))
        
        btn_layout = BoxLayout(spacing=dp(10))
        ya_btn = Button(
            text="Ya", 
            background_color=(0.8, 0, 0, 1),
            on_press=self.hapus_riwayat,
            color=(1, 1, 1, 1))
        tidak_btn = Button(
            text="Tidak", 
            background_color=(0, 0.7, 0, 1),
            color=(1, 1, 1, 1))
        
        popup = Popup(
            title="Konfirmasi", 
            content=content, 
            size_hint=(0.7, 0.4),
            title_color=(0, 0, 0, 1))
        
        ya_btn.bind(on_press=popup.dismiss)
        tidak_btn.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(ya_btn)
        btn_layout.add_widget(tidak_btn)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def hapus_riwayat(self, instance=None):
        try:
            # Hapus file CSV
            with open(DATA_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Tanggal", "Nama", "Mapel", "Jam", "Status"])
            
            # Hapus tampilan di antarmuka
            self.history_layout.clear_widgets()
            
            self.show_popup("Sukses", "Riwayat absensi berhasil dihapus.")
        except Exception as e:
            self.show_popup("Error", f"Gagal menghapus riwayat: {str(e)}")
    
    def catat_kehadiran(self, instance):
        self.catat_absensi("Hadir")
    
    def catat_ketidakhadiran(self, instance):
        self.catat_absensi("Tidak Hadir")
    
    def catat_absensi(self, status):
        # Get current date and time
        full_date = datetime.now().strftime("%d-%m-%Y %H:%M")
        short_date = datetime.now().strftime("%d-%m-%Y\n%H:%M")  # Format untuk tampilan
        
        # Get input values
        nama = self.guru_spinner.text
        mapel = self.mapel_spinner.text
        jam = self.jam_spinner.text
        
        # Validation
        if nama == "Pilih Guru":
            self.show_popup("Peringatan", "Pilih guru terlebih dahulu!")
            return
            
        if mapel == "Pilih Mapel":
            self.show_popup("Peringatan", "Pilih mata pelajaran terlebih dahulu!")
            return
            
        if jam == "Pilih Jam":
            self.show_popup("Peringatan", "Pilih jam pelajaran terlebih dahulu!")
            return
        
        # Save to CSV
        try:
            with open(DATA_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([full_date, nama, mapel, jam, status])
        except Exception as e:
            self.show_popup("Error", f"Gagal menyimpan data: {str(e)}")
            return
        
        # Add to history
        self.history_layout.add_widget(Label(
            text=short_date, 
            color=(0, 0, 0, 1),
            font_size=dp(12),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(40))
            )
        self.history_layout.add_widget(Label(
            text=nama, 
            color=(0, 0, 0, 1),
            font_size=dp(12),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(40))
            )
        self.history_layout.add_widget(Label(
            text=mapel, 
            color=(0, 0, 0, 1),
            font_size=dp(12),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(40))
            )
        self.history_layout.add_widget(Label(
            text=jam, 
            color=(0, 0, 0, 1),
            font_size=dp(12),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(40))
            )
        status_color = (0, 0.7, 0, 1) if status == "Hadir" else (0.8, 0, 0, 1)
        self.history_layout.add_widget(Label(
            text=status, 
            color=status_color, 
            bold=True,
            font_size=dp(12),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(40))
            )
        # Clear inputs
        self.guru_spinner.text = "Pilih Guru"
        self.mapel_spinner.text = "Pilih Mapel"
        self.jam_spinner.text = "Pilih Jam"
        
        self.show_popup("Sukses", f"Absensi {nama} untuk {mapel} {jam} berhasil dicatat!")
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(
            text=message, 
            halign='center',
            color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(16))
        )
        btn = Button(
            text="OK", 
            size_hint_y=None, 
            height=dp(40),
            color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(16))
        popup = Popup(
            title=title, 
            content=content, 
            size_hint=(0.8, 0.4),
            title_color=(0, 0, 0, 1),
            title_size=dp(18))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.open()

if __name__ == "__main__":
    AttendanceApp().run()