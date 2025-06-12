import tkinter as tk
from tkinter import messagebox, filedialog
import os
import random
from PIL import Image, ImageTk, ImageOps
import glob

class OutfitGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Zufälliger Outfit-Generator")
        self.root.geometry("600x900")  # Höher für mehr Kategorien
        self.root.configure(bg='black')  # Schwarzer Hintergrund
        
        # Ordner-Pfade (werden automatisch gesucht)
        self.top_folder = None
        self.layer_folder = None
        self.bottom_folder = None
        self.shoes_folder = None
        self.short_top_folder = None
        self.short_bottom_folder = None
        self.button_up_folder = None
        
        # Kategorie-Status (nur eine der drei speziellen Kategorien kann aktiv sein)
        self.layer_enabled = tk.BooleanVar(value=True)
        self.short_top_enabled = tk.BooleanVar(value=False)
        self.short_bottom_enabled = tk.BooleanVar(value=False)
        self.button_up_enabled = tk.BooleanVar(value=False)
        
        # Unterstützte Bildformate
        self.image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
        
        # Automatisch nach Ordnern suchen
        self.auto_find_folders()
        
        # GUI erstellen
        self.create_widgets()
        
        # Automatisch ein Outfit beim Start generieren
        self.root.after(500, self.auto_generate_on_startup)
        
    def auto_find_folders(self):
        """Intelligente Suche nach allen Ordnern"""
        search_paths = [
            os.path.expanduser("~"),  # Home-Verzeichnis
            os.path.expanduser("~/Desktop"),  # Desktop
            os.path.expanduser("~/Documents"),  # Dokumente
            os.path.expanduser("~/Pictures"),  # Bilder
            "C:\\",  # C-Laufwerk (Windows)
            "D:\\",  # D-Laufwerk (Windows)
        ]
        
        folder_names = {
            'top': ['Top', 'top', 'Tops', 'tops', 'Oberteile', 'oberteile'],
            'layer': ['Layer', 'layer', 'Layers', 'layers', 'Jacken', 'jacken', 'Hoodies', 'hoodies'],
            'bottom': ['Bottom', 'bottom', 'Bottoms', 'bottoms', 'Hosen', 'hosen', 'Unten', 'unten'],
            'shoes': ['Shoes', 'shoes', 'Schuhe', 'schuhe', 'Footwear', 'footwear'],
            'short_top': ['Short Top', 'short_top', 'Short_Top', 'ShortTop', 'Kurze Oberteile', 'kurze_oberteile', 'T-Shirts', 'tshirts'],
            'short_bottom': ['Short Bottom', 'short_bottom', 'Short_Bottom', 'ShortBottom', 'Kurze Hosen', 'kurze_hosen', 'Shorts', 'shorts'],
            'button_up': ['Button Up', 'button_up', 'Button_Up', 'ButtonUp', 'Hemden', 'hemden', 'Shirts', 'shirts', 'Blusen', 'blusen']
        }
        
        found_folders = {
            'top': None, 'layer': None, 'bottom': None, 'shoes': None,
            'short_top': None, 'short_bottom': None, 'button_up': None
        }
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            try:
                # Durchsuche Unterordner bis zu 3 Ebenen tief
                for root, dirs, files in os.walk(search_path):
                    # Begrenze die Suchtiefe
                    level = root.replace(search_path, '').count(os.sep)
                    if level >= 3:
                        dirs[:] = []  # Nicht tiefer gehen
                        continue
                    
                    for folder_type, names in folder_names.items():
                        if found_folders[folder_type] is None:
                            for name in names:
                                if name in dirs:
                                    folder_path = os.path.join(root, name)
                                    # Prüfe ob Ordner Bilder enthält
                                    if self.folder_contains_images(folder_path):
                                        found_folders[folder_type] = folder_path
                                        print(f"Gefunden: {folder_type} -> {folder_path}")
                                        break
                    
                    # Wenn alle gefunden, Suche beenden
                    if all(found_folders.values()):
                        break
                        
            except (PermissionError, OSError):
                continue  # Ordner ohne Berechtigung überspringen
                
            if all(found_folders.values()):
                break
        
        self.top_folder = found_folders['top']
        self.layer_folder = found_folders['layer']
        self.bottom_folder = found_folders['bottom']
        self.shoes_folder = found_folders['shoes']
        self.short_top_folder = found_folders['short_top']
        self.short_bottom_folder = found_folders['short_bottom']
        self.button_up_folder = found_folders['button_up']
        
    def folder_contains_images(self, folder_path):
        """Prüft ob ein Ordner Bilder enthält"""
        try:
            for extension in self.image_extensions:
                if glob.glob(os.path.join(folder_path, extension)):
                    return True
            return False
        except:
            return False
        
    def create_widgets(self):
        # Header Frame für Titel und Instagram
        header_frame = tk.Frame(self.root, bg='black')
        header_frame.pack(fill='x', pady=10)
        
        # Titel (links)
        title_label = tk.Label(header_frame, text="Outfit Generator by Henry's & Kim's®", 
                              font=("Arial", 16, "bold"),
                              bg='black', fg='white')
        title_label.pack(side='left', padx=20)
        
        # Instagram Handle (rechts)
        instagram_label = tk.Label(header_frame, text="Instagram/henryzdumpster", 
                                 font=("Arial", 10, "italic"),
                                 bg='black', fg='#E4405F')  # Instagram-Farbe
        instagram_label.pack(side='right', padx=20)
        
        # Status der gefundenen Ordner anzeigen
        status_text = self.get_folder_status()
        self.status_label = tk.Label(self.root, text=status_text,
                                    font=("Arial", 9),
                                    bg='black', fg='lightgray',
                                    justify=tk.LEFT)
        self.status_label.pack(pady=5)
        
        # Button zum Ordner manuell auswählen (abgerundet)
        folder_button = tk.Button(self.root, text="Ordner manuell auswählen", 
                                 command=self.select_folders,
                                 bg="#4CAF50", fg='white',
                                 font=("Arial", 10, "bold"),
                                 relief='flat',
                                 bd=0,
                                 padx=20, pady=8,
                                 cursor='hand2')
        folder_button.configure(highlightbackground='black')
        folder_button.pack(pady=5)
        
        # Kategorie-Schalter
        self.create_category_switches()
        
        # Button zum Outfit generieren (abgerundet)
        self.generate_button = tk.Button(self.root, text="🎲 Zufälliges Outfit generieren!", 
                                        command=self.generate_outfit,
                                        bg="#FF6B35", fg='white',
                                        font=("Arial", 12, "bold"),
                                        relief='flat',
                                        bd=0,
                                        height=2,
                                        padx=20,
                                        cursor='hand2')
        self.generate_button.configure(highlightbackground='black')
        self.generate_button.pack(pady=15)
        
        # Scrollbares Frame für die Bilder
        self.create_scrollable_frame()
        
    def create_category_switches(self):
        """Erstellt die Schalter für alle Kategorien"""
        switches_frame = tk.Frame(self.root, bg='black')
        switches_frame.pack(pady=10)
        
        # Layer Schalter
        self.layer_checkbox = tk.Checkbutton(switches_frame, 
                                           text="🧥 Layer einblenden",
                                           variable=self.layer_enabled,
                                           command=lambda: self.toggle_category('layer'),
                                           bg='black', fg='white',
                                           selectcolor='#333333',
                                           activebackground='#444444',
                                           activeforeground='white',
                                           font=("Arial", 10),
                                           relief='flat',
                                           bd=0,
                                           cursor='hand2')
        self.layer_checkbox.pack(pady=2)
        
        # Short Top Schalter
        self.short_top_checkbox = tk.Checkbutton(switches_frame, 
                                                text="👕 Short Top einblenden",
                                                variable=self.short_top_enabled,
                                                command=lambda: self.toggle_category('short_top'),
                                                bg='black', fg='white',
                                                selectcolor='#333333',
                                                activebackground='#444444',
                                                activeforeground='white',
                                                font=("Arial", 10),
                                                relief='flat',
                                                bd=0,
                                                cursor='hand2')
        self.short_top_checkbox.pack(pady=2)
        
        # Short Bottom Schalter
        self.short_bottom_checkbox = tk.Checkbutton(switches_frame, 
                                                   text="🩳 Short Bottom einblenden",
                                                   variable=self.short_bottom_enabled,
                                                   command=lambda: self.toggle_category('short_bottom'),
                                                   bg='black', fg='white',
                                                   selectcolor='#333333',
                                                   activebackground='#444444',
                                                   activeforeground='white',
                                                   font=("Arial", 10),
                                                   relief='flat',
                                                   bd=0,
                                                   cursor='hand2')
        self.short_bottom_checkbox.pack(pady=2)
        
        # Button Up Schalter
        self.button_up_checkbox = tk.Checkbutton(switches_frame, 
                                                text="👔 Button Up einblenden",
                                                variable=self.button_up_enabled,
                                                command=lambda: self.toggle_category('button_up'),
                                                bg='black', fg='white',
                                                selectcolor='#333333',
                                                activebackground='#444444',
                                                activeforeground='white',
                                                font=("Arial", 10),
                                                relief='flat',
                                                bd=0,
                                                cursor='hand2')
        self.button_up_checkbox.pack(pady=2)
        
    def toggle_category(self, activated_category):
        """Behandelt die Kategorie-Umschaltung mit spezifischer Exklusivität"""
        # Layer bleibt unberührt von anderen Kategorien
        
        # Short Top und Top schließen sich gegenseitig aus
        if activated_category == 'short_top' and self.short_top_enabled.get():
            # Wenn Short Top aktiviert wird, deaktiviere Button Up
            self.button_up_enabled.set(False)
        elif activated_category == 'layer':
            # Layer beeinflusst keine anderen Kategorien
            pass
        elif activated_category == 'short_bottom' and self.short_bottom_enabled.get():
            # Short Bottom ist unabhängig, beeinflusst keine anderen
            pass
        elif activated_category == 'button_up' and self.button_up_enabled.get():
            # Button Up deaktiviert sowohl Top als auch Short Top
            self.short_top_enabled.set(False)
        
        # Outfit neu generieren
        if self.has_required_folders():
            self.generate_outfit()
        
    def create_scrollable_frame(self):
        """Erstellt ein scrollbares Frame für die Bilder"""
        # Canvas für Scrolling
        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview, bg='#333333')
        self.scrollable_frame = tk.Frame(self.canvas, bg='black')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack Canvas und Scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)
        
        # Mausrad-Scrolling aktivieren
        self.bind_mousewheel()
        
        # Frame für Top/Short Top/Button Up und Layer nebeneinander
        self.top_layer_frame = tk.Frame(self.scrollable_frame, bg='black')
        self.top_layer_frame.pack(pady=10, padx=20, fill='x')
        
        # Top/Short Top/Button Up Label (links)
        self.top_label = tk.Label(self.top_layer_frame, text="👔 Top", 
                                 font=("Arial", 12), 
                                 bg='#333333', fg='white',
                                 relief='flat', bd=2,
                                 pady=10)
        self.top_label.pack(side='left', padx=(0, 10), fill='both', expand=True)
        
        # Layer Label (rechts)
        self.layer_label = tk.Label(self.top_layer_frame, text="🧥 Layer", 
                                   font=("Arial", 12), 
                                   bg='#333333', fg='white',
                                   relief='flat', bd=2,
                                   pady=10)
        self.layer_label.pack(side='right', padx=(10, 0), fill='both', expand=True)
        
        # Bottom/Short Bottom Label (volle Breite)
        self.bottom_label = tk.Label(self.scrollable_frame, text="👖 Bottom", 
                                    font=("Arial", 12),
                                    bg='#333333', fg='white',
                                    relief='flat', bd=2,
                                    pady=10)
        self.bottom_label.pack(pady=8, padx=20, fill='x')
        
        # Shoes Label (volle Breite)
        self.shoes_label = tk.Label(self.scrollable_frame, text="👟 Schuhe", 
                                   font=("Arial", 12),
                                   bg='#333333', fg='white',
                                   relief='flat', bd=2,
                                   pady=10)
        self.shoes_label.pack(pady=8, padx=20, fill='x')
        
    def bind_mousewheel(self):
        """Bindet Mausrad-Scrolling an Canvas"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        # Für Windows/Mac
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Für Linux
        def _on_mousewheel_linux(event):
            self.canvas.yview_scroll(-1, "units")
        def _on_mousewheel_linux_down(event):
            self.canvas.yview_scroll(1, "units")
            
        self.canvas.bind("<Button-4>", _on_mousewheel_linux)
        self.canvas.bind("<Button-5>", _on_mousewheel_linux_down)
        
    def auto_generate_on_startup(self):
        """Automatisch ein Outfit beim Programmstart generieren"""
        if self.has_required_folders():
            self.generate_outfit()
    
    def has_required_folders(self):
        """Prüft ob die Mindestordner vorhanden sind"""
        return all([self.top_folder, self.bottom_folder, self.shoes_folder])
        
    def get_folder_status(self):
        """Status der gefundenen Ordner als Text"""
        status = "Automatisch gefundene Ordner:\n"
        folders = [
            ("👔 Top:", self.top_folder),
            ("🧥 Layer:", self.layer_folder),
            ("👖 Bottom:", self.bottom_folder),
            ("👟 Schuhe:", self.shoes_folder),
            ("👕 Short Top:", self.short_top_folder),
            ("🩳 Short Bottom:", self.short_bottom_folder),
            ("👔 Button Up:", self.button_up_folder)
        ]
        
        for name, folder in folders:
            if folder:
                folder_name = os.path.basename(folder)
                status += f"{name} ✓ {folder_name}\n"
            else:
                status += f"{name} ✗ Nicht gefunden\n"
                
        return status
        
    def select_folders(self):
        """Ordner für alle Kategorien manuell auswählen"""
        self.top_folder = filedialog.askdirectory(title="Top-Ordner auswählen")
        if self.top_folder:
            self.layer_folder = filedialog.askdirectory(title="Layer-Ordner auswählen")
        if self.layer_folder:
            self.bottom_folder = filedialog.askdirectory(title="Bottom-Ordner auswählen")
        if self.bottom_folder:
            self.shoes_folder = filedialog.askdirectory(title="Schuhe-Ordner auswählen")
        if self.shoes_folder:
            self.short_top_folder = filedialog.askdirectory(title="Short Top-Ordner auswählen")
        if self.short_top_folder:
            self.short_bottom_folder = filedialog.askdirectory(title="Short Bottom-Ordner auswählen")
        if self.short_bottom_folder:
            self.button_up_folder = filedialog.askdirectory(title="Button Up-Ordner auswählen")
            
        if self.has_required_folders():
            messagebox.showinfo("Erfolg", "Mindestens die erforderlichen Ordner wurden ausgewählt!")
            # Status aktualisieren
            self.status_label.configure(text=self.get_folder_status())
        
    def get_random_image(self, folder_path):
        """Zufälliges Bild aus einem Ordner auswählen"""
        if not folder_path or not os.path.exists(folder_path):
            return None
            
        all_images = []
        for extension in self.image_extensions:
            all_images.extend(glob.glob(os.path.join(folder_path, extension)))
            
        if not all_images:
            return None
            
        return random.choice(all_images)
    
    def remove_white_background(self, image):
        """Entfernt weißen Hintergrund und macht ihn schwarz/transparent"""
        try:
            # Konvertiere zu RGBA wenn nötig
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Erstelle eine Kopie für die Bearbeitung
            img_array = image.load()
            width, height = image.size
            
            # Definiere Schwellenwerte für "weiß" (toleranter)
            white_threshold = 240  # Werte über 240 gelten als "weiß"
            
            for x in range(width):
                for y in range(height):
                    r, g, b, a = img_array[x, y]
                    
                    # Prüfe ob Pixel "weiß" ist (alle RGB-Werte hoch)
                    if r > white_threshold and g > white_threshold and b > white_threshold:
                        # Mache weißen Hintergrund schwarz
                        img_array[x, y] = (0, 0, 0, a)  # Schwarz mit ursprünglicher Alpha
            
            return image
            
        except Exception as e:
            print(f"Fehler beim Entfernen des weißen Hintergrunds: {e}")
            return image
    
    def resize_image(self, image_path, max_width=250, max_height=180):
        """Bild auf gewünschte Größe anpassen und weißen Hintergrund entfernen"""
        try:
            image = Image.open(image_path)
            
            # Entferne weißen Hintergrund
            image = self.remove_white_background(image)
            
            # Größe anpassen
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Fehler beim Laden des Bildes {image_path}: {e}")
            return None
    
    def get_active_top_category(self):
        """Gibt die aktive Top-Kategorie zurück"""
        if self.button_up_enabled.get():
            return ('button_up', self.button_up_folder, "👔 Button Up")
        elif self.short_top_enabled.get():
            return ('short_top', self.short_top_folder, "👕 Short Top")
        else:
            return ('top', self.top_folder, "👔 Top")
    
    def get_active_bottom_category(self):
        """Gibt die aktive Bottom-Kategorie zurück"""
        if self.short_bottom_enabled.get():
            return ('short_bottom', self.short_bottom_folder, "🩳 Short Bottom")
        else:
            return ('bottom', self.bottom_folder, "👖 Bottom")
    
    def generate_outfit(self):
        """Zufälliges Outfit aus den Ordnern generieren"""
        # Prüfen ob Mindestordner existieren (Top, Bottom, Schuhe)
        required_folders = [
            (self.top_folder, "Top"),
            (self.bottom_folder, "Bottom"), 
            (self.shoes_folder, "Schuhe")
        ]
        
        missing_folders = []
        for folder, name in required_folders:
            if not folder or not os.path.exists(folder):
                missing_folders.append(name)
                
        if missing_folders:
            messagebox.showerror("Fehler", 
                               f"Folgende Ordner fehlen oder sind ungültig:\n" + 
                               "\n".join(missing_folders) + 
                               "\n\nBitte 'Ordner manuell auswählen' verwenden oder\n" +
                               "entsprechende Ordner erstellen.")
            return
        
        # Aktive Top-Kategorie ermitteln
        top_category, top_folder, top_text = self.get_active_top_category()
        top_image = self.get_random_image(top_folder)
        
        # Aktive Bottom-Kategorie ermitteln
        bottom_category, bottom_folder, bottom_text = self.get_active_bottom_category()
        bottom_image = self.get_random_image(bottom_folder)
        
        # Schuhe (immer angezeigt)
        shoes_image = self.get_random_image(self.shoes_folder)
        
        # Layer (unabhängig von anderen)
        layer_image = None
        if self.layer_enabled.get() and self.layer_folder and os.path.exists(self.layer_folder):
            layer_image = self.get_random_image(self.layer_folder)
        
        # Labels aktualisieren
        self.top_label.configure(text=top_text)
        self.bottom_label.configure(text=bottom_text)
        
        # Layer Label ein-/ausblenden
        if self.layer_enabled.get():
            self.layer_label.pack(side='right', padx=(10, 0), fill='both', expand=True)
        else:
            self.layer_label.pack_forget()
        
        # Bilder anzeigen
        self.display_images(top_image, layer_image, bottom_image, shoes_image, top_text, bottom_text)
    
    def display_images(self, top_path, layer_path, bottom_path, shoes_path, top_category_text, bottom_category_text):
        """Die Bilder in der GUI anzeigen"""
        images_data = [
            (top_path, self.top_label, top_category_text),
            (layer_path, self.layer_label, "🧥 Layer"),
            (bottom_path, self.bottom_label, bottom_category_text),
            (shoes_path, self.shoes_label, "👟 Schuhe")
        ]
        
        for image_path, label, category in images_data:
            # Layer überspringen wenn deaktiviert
            if category == "🧥 Layer" and not self.layer_enabled.get():
                continue
                
            if image_path and os.path.exists(image_path):
                photo = self.resize_image(image_path)
                if photo:
                    label.configure(image=photo, text="", compound='top')
                    label.image = photo  # Referenz behalten
                    # Hintergrund für Bild ändern
                    label.configure(bg='#000000')
                else:
                    label.configure(image="", text=f"Fehler beim Laden\n{category}", 
                                  bg='#333333', fg='lightcoral')
            else:
                # Für Layer: Nur Fehlermeldung wenn aktiviert
                if category == "🧥 Layer" and self.layer_enabled.get():
                    label.configure(image="", text=f"Kein Bild gefunden\n{category}",
                                  bg='#333333', fg='orange')
                elif category != "🧥 Layer":
                    label.configure(image="", text=f"Kein Bild gefunden\n{category}",
                                  bg='#333333', fg='orange')

def main():
    root = tk.Tk()
    app = OutfitGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
