# vba-ersatz
Dies ist eine Reimplementierung des VBA-Tools in vernünftig.

# Autor
Martin Haug <martin.haug@webpctech.de>

# TODO:
- Gruppen CRUD
    - Liste mit vorhandenen Gruppen anzeigen
    - Neue Gruppe anlegen 
    - Gruppe löschen
    - Gruppe aus Testplan importieren
        - Bestehende Testcases dürfen dabei nicht überschrieben werden, sollen aber ggf. aktualisiert werden
    - Testplan generieren
- Testcase CRUD
    - Testcase zu Gruppe hinzufügen
    - Testcase anlegen
    - Testcase bearbeiten
        - Parameter anpassen
- Jenkins
    - Job anlegen
    - Ergebnis eines Laufs anzeigen (optional)
        - Nur Anzahl der Fails und Passes
    - Job starten
- Coordinator
    - Vorhandene Templates erkennen
    - Ordnerstruktur beibehalten