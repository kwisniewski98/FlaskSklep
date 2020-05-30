	create table if not exists Produkt(
		id integer PRIMARY KEY autoincrement ,
		Nazwa varchar(100) not null,
		cena_netto float not null,
		vat float check (vat > 0) not null,
		opiekun integer,
        foreign key(opiekun) references Osoba(id)

		)
