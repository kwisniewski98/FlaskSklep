	create table if not exists Adres(
		id integer PRIMARY KEY autoincrement,
		nr_lokalu integer check (nr_lokalu > 0),
		nr_budynku integer check(nr_budynku > 0) not null,
		ulica varchar(40) not null,
		miasto varchar(40) not null,
		wojewodztwo varchar(40) not null

	)