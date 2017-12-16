# sodo

Do testów:
Hasło do admina - 'blacktron'
Zwykły uzytkownik - 'michal', 'kamil'
LABI - 'admin_wmi', 'admin_fizyka'

Potrzebne do działania:
- weasyprint - generowanie pdfów z wzorca w html, https://weasyprint.readthedocs.io/en/stable/install.html


<b>Ustalenia:</b>

Przy dodawaniu wniosku sprawdzamy 4 rzeczy
- pracownika
- obiekt 
- upraweninia
- typ wniosku
czy się nie powtarzają, jeśli tak to przekierowanie do wniosku z opcją 'wyslij ponownie' jeśli został odrzucony, natomiast jeśli został przyjęty to mamy wgląd do wniosku wraz z opcją zniesienia uprawnienia (do przemyślenia). Jesli nie to stworzenie nowego. 



Jeżeli LABI zatwierdzi wniosek to trafia on do potrójnej tabeli. Jeżeli zostanie zatwierdzony wniosek o usuniecie uprawnienia to usuwamy z tabeli. Odrzucone wnioski nie trafiają do tabeli.
Pracownik + obiekt + uprawnienie.

