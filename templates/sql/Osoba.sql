
	create table if not exists Osoba(
		id integer PRIMARY KEY autoincrement,
		imie varchar(20) not null,
		nazwisko varchar(20)not null,
		adres int  not null,
		foreign key(adres) references Adres(id)

	)
