# sodo

<i>Do zrobienia</i>
Powrót do carta jeżeli się wyjdzie - zapisywać stan carta (najlepiej w modelu)

USER_APP:
- lista wniosków oczekujących - wypisanie obiektów (model str)
- wizard
	- wyszukiwanie jednostki
	- walidacja
	- aktualne uprawnienia wybranych pracowników do wybranych obiektów
	- podsumowanie wniosku - ostylować ładnie
- Dostępne obiekty - wyszukiwanie
- Twój panel - poprawić 
- autoryzacja
- pdfy poprawić 
- podgląd wniosku poprawić
- messeges poprawić

- dodać menu administratora systemu - wyświetlać się tam będą wnioski do ostatecznego zatwierdzenia


ADMIN_APP:
- strona początkowa zatwierdzanie szybkie wniosków
- zakładka wnioski, lista wniosków złożonych dla labiego (paginacja, wyszukiwanie)
- Pracownicy - paginacja, wyszukiwanie, więcej informacji na stronie + podgląd
- obiekty - paginacja, wyszukiwanie, więcej informacji na stronie + podgląd
- typy obiektów - paginacja, wyszukiwanie, więcej informacji na stronie + podgląd
- jednostki org - paginacja, wyszukiwanie, więcej informacji na stronie + podgląd
- wyszukiwanie usunąć
- dodawanie obiektów, typów, jednostek, rodzaj pracownika i pracownika
- dodać wizard wniosku

Rozbudować historie:
Składamy wniosek (status: złożony)
Labi zatwierdza (zatwierdzone przez labiego)
ABI zatwierdza (zatwierdzone przez ABI) - na tym poziomie już pokazujemy pracownikowi
AS zatwierdza (zatwierdzone przez AS) - tutaj dajemy informacje że zostało wprowadzone

Statusy: odrzucony, złożony, LABI, ABI, AS

+ dodać pole pracownika do historii żeby było wiadomo kto ostatni coś robił



Do testów:
Hasło do admina - 'blacktron'
Zwykły uzytkownik - 'michal', 'kamil'
LABI - 'admin_wmi', 'admin_fizyka'

Potrzebne do działania:
- weasyprint - generowanie pdfów z wzorca w html, https://weasyprint.readthedocs.io/en/stable/install.html
- multiselectfield - instalowanie: pip3 install django-multiselectfield


<b>Ustalenia:</b>

Przy dodawaniu wniosku sprawdzamy 4 rzeczy
- pracownika
- obiekt 
- upraweninia
- typ wniosku

czy się nie powtarzają, jeśli tak to przekierowanie do wniosku z opcją 'wyslij ponownie' jeśli został odrzucony, natomiast jeśli został przyjęty to mamy wgląd do wniosku wraz z opcją zniesienia uprawnienia (do przemyślenia). Jesli nie to stworzenie nowego. 

Jeżeli LABI zatwierdzi wniosek to trafia on do potrójnej tabeli. Jeżeli zostanie zatwierdzony wniosek o usuniecie uprawnienia to usuwamy z tabeli. Odrzucone wnioski nie trafiają do tabeli.
Pracownik + obiekt + uprawnienie.

Jeśli wniosek jest przetwarzany to nie możemy dodać takiego samego wniosku jeszcze raz. 
