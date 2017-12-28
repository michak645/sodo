# sodo

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


<i>Do zrobienia w wizardzie</i>
<ul>
	<li>Step 1 - uwzględnić wybór</li>
	<li>Step 2 - Czyszczenie wyborów</li>
	<li>Step 3 - typ wniosku</li>
	<li>Step 4 - podsumowanie i złożenie</li>
	<li>Ogólne anulowanie wizarda koło progresu</li>
</ul>
Zmienić tabele wniosku aby móc tworzyć dla wielu użytkowników i obiektów 
Powrót do carta jeżeli się wyjdzie - zapisywać stan carta (najlepiej w modelu)
Key - dodać do carta