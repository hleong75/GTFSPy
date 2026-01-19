"""
Exemples d'utilisation de GTFSPy
"""

import os
import tempfile
import zipfile
import csv


def create_sample_gtfs():
    """
    Crée un fichier GTFS d'exemple pour tester l'application
    
    Returns:
        str: Chemin vers le fichier ZIP GTFS créé
    """
    # Créer un répertoire temporaire
    output_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    if not os.path.exists(output_dir):
        output_dir = tempfile.gettempdir()
    
    gtfs_zip_path = os.path.join(output_dir, 'sample_gtfs.zip')
    
    # Données d'exemple - Réseau de transport fictif à Paris
    stops_data = [
        ['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'stop_desc'],
        ['S1', 'Châtelet', '48.8584', '2.3470', 'Station centrale'],
        ['S2', 'Gare du Nord', '48.8809', '2.3553', 'Gare ferroviaire'],
        ['S3', 'République', '48.8676', '2.3633', 'Place République'],
        ['S4', 'Bastille', '48.8532', '2.3692', 'Place de la Bastille'],
        ['S5', 'Nation', '48.8484', '2.3960', 'Place de la Nation'],
        ['S6', 'Saint-Lazare', '48.8762', '2.3255', 'Gare Saint-Lazare'],
        ['S7', 'Opéra', '48.8716', '2.3314', 'Palais Garnier'],
        ['S8', 'Montparnasse', '48.8420', '2.3213', 'Gare Montparnasse'],
    ]
    
    routes_data = [
        ['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_type', 'route_color'],
        ['R1', 'AGENCY1', '1', 'Ligne 1 - Est-Ouest', '1', 'FFCD00'],
        ['R2', 'AGENCY1', '4', 'Ligne 4 - Nord-Sud', '1', '9F1B51'],
        ['R3', 'AGENCY1', '14', 'Ligne 14', '1', '62259D'],
    ]
    
    agency_data = [
        ['agency_id', 'agency_name', 'agency_url', 'agency_timezone', 'agency_lang'],
        ['AGENCY1', 'Transport Public Paris', 'http://example.com', 'Europe/Paris', 'fr'],
    ]
    
    trips_data = [
        ['route_id', 'service_id', 'trip_id', 'trip_headsign', 'direction_id'],
        ['R1', 'WD', 'T1_1', 'Direction Nation', '0'],
        ['R1', 'WD', 'T1_2', 'Direction Châtelet', '1'],
        ['R2', 'WD', 'T2_1', 'Direction Bastille', '0'],
        ['R3', 'WD', 'T3_1', 'Direction Opéra', '0'],
    ]
    
    stop_times_data = [
        ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence'],
        # Ligne 1 - Direction Nation
        ['T1_1', '08:00:00', '08:00:00', 'S1', '1'],
        ['T1_1', '08:05:00', '08:05:00', 'S3', '2'],
        ['T1_1', '08:10:00', '08:10:00', 'S4', '3'],
        ['T1_1', '08:15:00', '08:15:00', 'S5', '4'],
        # Ligne 1 - Direction Châtelet
        ['T1_2', '09:00:00', '09:00:00', 'S5', '1'],
        ['T1_2', '09:05:00', '09:05:00', 'S4', '2'],
        ['T1_2', '09:10:00', '09:10:00', 'S3', '3'],
        ['T1_2', '09:15:00', '09:15:00', 'S1', '4'],
        # Ligne 4
        ['T2_1', '08:30:00', '08:30:00', 'S2', '1'],
        ['T2_1', '08:35:00', '08:35:00', 'S3', '2'],
        ['T2_1', '08:40:00', '08:40:00', 'S4', '3'],
        # Ligne 14
        ['T3_1', '10:00:00', '10:00:00', 'S6', '1'],
        ['T3_1', '10:05:00', '10:05:00', 'S7', '2'],
        ['T3_1', '10:10:00', '10:10:00', 'S1', '3'],
    ]
    
    calendar_data = [
        ['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date'],
        ['WD', '1', '1', '1', '1', '1', '0', '0', '20240101', '20241231'],
        ['WE', '0', '0', '0', '0', '0', '1', '1', '20240101', '20241231'],
    ]
    
    # Créer le fichier ZIP
    with zipfile.ZipFile(gtfs_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename, data in [
            ('stops.txt', stops_data),
            ('routes.txt', routes_data),
            ('agency.txt', agency_data),
            ('trips.txt', trips_data),
            ('stop_times.txt', stop_times_data),
            ('calendar.txt', calendar_data)
        ]:
            # Convertir en CSV
            csv_content = '\n'.join([','.join(row) for row in data])
            zf.writestr(filename, csv_content)
    
    print(f"✓ Fichier GTFS créé: {gtfs_zip_path}")
    return gtfs_zip_path


def print_usage_examples():
    """Affiche des exemples d'utilisation"""
    print("\n" + "=" * 60)
    print("Exemples d'utilisation GTFSPy")
    print("=" * 60)
    
    print("\n1. Coordonnées des arrêts d'exemple:")
    print("   - Châtelet: 48.8584, 2.3470")
    print("   - Gare du Nord: 48.8809, 2.3553")
    print("   - République: 48.8676, 2.3633")
    print("   - Bastille: 48.8532, 2.3692")
    print("   - Nation: 48.8484, 2.3960")
    
    print("\n2. Comment utiliser dans l'application:")
    print("   a. Lancer l'application: python main.py")
    print("   b. Cliquer sur 'Importer GTFS'")
    print("   c. Sélectionner le fichier sample_gtfs.zip")
    print("   d. Entrer les coordonnées:")
    print("      - Départ: 48.8584, 2.3470 (Châtelet)")
    print("      - Arrivée: 48.8484, 2.3960 (Nation)")
    print("   e. Cliquer sur 'Calculer itinéraire'")
    
    print("\n3. Format des coordonnées:")
    print("   - Latitude, Longitude")
    print("   - Exemple: 48.8584, 2.3470")
    print("   - Pas d'espaces autour de la virgule")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    # Créer un fichier GTFS d'exemple
    gtfs_path = create_sample_gtfs()
    
    # Afficher les exemples d'utilisation
    print_usage_examples()
    
    print(f"\n✓ Fichier d'exemple prêt à être importé!")
    print(f"  Chemin: {gtfs_path}")
