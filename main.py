"""
GTFSPy - Application de routage de transport en commun
Application mobile pour calculer l'itinéraire optimal entre deux points
en utilisant les données GTFS
"""

import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapView, MapMarker
from gtfs_manager import GTFSManager
from routing_engine import RoutingEngine
from storage_manager import StorageManager


class MainScreen(Screen):
    """Écran principal de l'application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Titre
        title = Label(
            text='GTFSPy - Routage Transport',
            size_hint=(1, 0.1),
            font_size='20sp'
        )
        layout.add_widget(title)
        
        # Carte
        self.mapview = MapView(
            zoom=11,
            lat=48.8566,
            lon=2.3522,
            size_hint=(1, 0.6)
        )
        layout.add_widget(self.mapview)
        
        # Champs de saisie
        input_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=5)
        
        self.origin_input = TextInput(
            hint_text='Point de départ (lat, lon)',
            multiline=False
        )
        input_layout.add_widget(self.origin_input)
        
        self.destination_input = TextInput(
            hint_text='Point d\'arrivée (lat, lon)',
            multiline=False
        )
        input_layout.add_widget(self.destination_input)
        
        layout.add_widget(input_layout)
        
        # Boutons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=5)
        
        calculate_btn = Button(text='Calculer itinéraire')
        calculate_btn.bind(on_press=self.calculate_route)
        button_layout.add_widget(calculate_btn)
        
        import_btn = Button(text='Importer GTFS')
        import_btn.bind(on_press=self.import_gtfs)
        button_layout.add_widget(import_btn)
        
        download_map_btn = Button(text='Télécharger carte')
        download_map_btn.bind(on_press=self.download_map)
        button_layout.add_widget(download_map_btn)
        
        layout.add_widget(button_layout)
        
        self.add_widget(layout)
    
    def calculate_route(self, instance):
        """Calcule l'itinéraire entre deux points"""
        try:
            origin = self.parse_coordinates(self.origin_input.text)
            destination = self.parse_coordinates(self.destination_input.text)
            
            app = App.get_running_app()
            route = app.routing_engine.find_route(origin, destination)
            
            if route:
                self.display_route(route)
                self.show_popup('Succès', 'Itinéraire calculé!')
            else:
                self.show_popup('Erreur', 'Aucun itinéraire trouvé')
        except Exception as e:
            self.show_popup('Erreur', f'Erreur: {str(e)}')
    
    def parse_coordinates(self, text):
        """Parse les coordonnées depuis le texte"""
        parts = text.strip().replace(' ', '').split(',')
        if len(parts) == 2:
            return float(parts[0]), float(parts[1])
        raise ValueError("Format invalide. Utilisez: lat, lon")
    
    def display_route(self, route):
        """Affiche l'itinéraire sur la carte"""
        # Nettoyer les marqueurs existants
        self.mapview.clear_widgets()
        
        # Ajouter les marqueurs pour le début et la fin
        if route and len(route) > 0:
            start = route[0]
            end = route[-1]
            
            start_marker = MapMarker(lat=start['lat'], lon=start['lon'])
            end_marker = MapMarker(lat=end['lat'], lon=end['lon'])
            
            self.mapview.add_widget(start_marker)
            self.mapview.add_widget(end_marker)
            
            # Centrer la carte
            self.mapview.center_on(start['lat'], start['lon'])
    
    def import_gtfs(self, instance):
        """Ouvre le sélecteur de fichiers pour importer un GTFS"""
        content = BoxLayout(orientation='vertical')
        
        filechooser = FileChooserListView(
            filters=['*.zip'],
            path=os.path.expanduser('~')
        )
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        
        select_btn = Button(text='Sélectionner')
        cancel_btn = Button(text='Annuler')
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Sélectionner un fichier GTFS',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def on_select(instance):
            if filechooser.selection:
                app = App.get_running_app()
                success = app.gtfs_manager.import_gtfs(filechooser.selection[0])
                if success:
                    self.show_popup('Succès', 'GTFS importé avec succès!')
                else:
                    self.show_popup('Erreur', 'Échec de l\'importation')
                popup.dismiss()
        
        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def download_map(self, instance):
        """Télécharge les données de carte pour utilisation hors ligne"""
        app = App.get_running_app()
        success = app.storage_manager.download_map_data(
            self.mapview.lat,
            self.mapview.lon,
            self.mapview.zoom
        )
        if success:
            self.show_popup('Succès', 'Carte téléchargée!')
        else:
            self.show_popup('Erreur', 'Échec du téléchargement')
    
    def show_popup(self, title, message):
        """Affiche un popup avec un message"""
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        
        close_btn = Button(text='Fermer', size_hint=(1, 0.3))
        content.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


class GTFSPyApp(App):
    """Application principale GTFSPy"""
    
    def build(self):
        """Construit l'interface de l'application"""
        self.title = 'GTFSPy - Routage Transport'
        
        # Initialiser les gestionnaires
        self.storage_manager = StorageManager()
        self.gtfs_manager = GTFSManager(self.storage_manager)
        self.routing_engine = RoutingEngine(self.gtfs_manager)
        
        # Créer le gestionnaire d'écrans
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        
        return sm


if __name__ == '__main__':
    GTFSPyApp().run()
