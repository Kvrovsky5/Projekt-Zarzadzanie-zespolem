
# Aplikacja do Zarządzania Zadaniami w Zespole

## Spis treści
1. [Opis](#opis)
2. [Funkcjonalności](#funkcjonalności)
3. [Instrukcje obsługi](#instrukcje-obsługi)
   - [Wymagania](#wymagania)
   - [Instalacja](#instalacja)
   - [Uruchomienie](#uruchomienie)

## Opis
Aplikacja do zarządzania zadaniami w zespole napisana w Pythonie. Umożliwia tworzenie zadań, przypisywanie ich do użytkowników, śledzenie statusu zadań oraz generowanie raportów.

## Funkcjonalności
- **Dodawanie użytkowników**: Możliwość dodawania nowych członków zespołu.
- **Tworzenie zadań**: Tworzenie nowych zadań z przypisaniem do wybranego użytkownika.
- **Śledzenie statusu zadań**: Zadania są wyświetlane w trzech kolumnach odpowiadających ich statusom: To Do, In Progress, Done.
- **Edycja zadań**: Możliwość edytowania nazwy, opisu i przypisanego użytkownika dla każdego zadania.
- **Zmiana statusu zadań**: Zmiana statusu zadania przez kliknięcie na kartę zadania.
- **Generowanie raportów**: Generowanie raportów dotyczących liczby zadań przypisanych do użytkowników oraz czasu spędzonego nad zadaniami.
- **Przypisywanie zadań po usunięciu użytkownika**: Możliwość ponownego przypisania zadań do innych użytkowników po usunięciu użytkownika.
- **Przewijanie listy zadań**: Obsługa przewijania listy zadań w każdej sekcji (To Do, In Progress, Done).
- **Zawijanie tekstu opisu zadań**: Opisy zadań zawijają się automatycznie, jeśli są zbyt długie.

## Instrukcje obsługi

### Wymagania
- Python 3.6+
- Tkinter (wbudowany w Pythonie)
- `ttk` (wbudowany w Pythonie)

### Instalacja
1. Sklonuj repozytorium:
    ```bash
    git clone https://github.com/Kvrovsky5/Projekt-Zarzadzanie-zespolem.git
    ```
2. Przejdź do katalogu z projektem:
    ```bash
    cd Task_manager
    ```

### Uruchomienie
1. Uruchom aplikację za pomocą poniższego polecenia:
    ```bash
    python Task_manager.py
    ```

## Użycie
- Aby dodać użytkownika, kliknij przycisk "Add User" i wprowadź nazwę użytkownika.
- Aby dodać zadanie, kliknij przycisk "Add Task", wprowadź nazwę zadania, opis, oraz wybierz przypisanego użytkownika.
- Zadania są wyświetlane w trzech kolumnach odpowiadających ich statusom: To Do, In Progress, Done.
- Kliknij na zadanie prawym przyciskiem myszy, aby zmienić jego status lub edytować zadanie.
- Kliknij przycisk "Generate Report", aby wygenerować raport dotyczący liczby zadań przypisanych do użytkowników oraz czasu spędzonego nad zadaniami.
- Lista użytkowników jest wyświetlana w prawym dolnym rogu aplikacji.
- Po usunięciu użytkownika, pojawi się możliwość przypisania zadań usuniętego użytkownika do innych członków zespołu.

## Struktura Plików
```plaintext
Task_manager/
│
├── tasks.json          # Plik do przechowywania zadań i użytkowników
├── Task_manager.py     # Główny plik aplikacji
└── README.md           # Dokumentacja projektu
```


