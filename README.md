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
	- komentarz do wniosku
- Twój panel - poprawić 
- autoryzacja
- podgląd wniosku poprawić (zobaczyc czy uprawnienia sa)
- messeges poprawić


LBI_APP:
- strona początkowa zatwierdzanie szybkie wniosków
- zakładka wnioski, lista wniosków złożonych dla labiego (paginacja, wyszukiwanie)
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
- bootstrap-pagination - instalowanie: pip3 install django-bootstrap-pagination


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
