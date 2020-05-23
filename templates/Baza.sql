if not exists ( SELECT *
                 FROM INFORMATION_SCHEMA.TABLES where  TABLE_NAME = 'Adres')
	create table Adres(
		id int PRIMARY KEY identity ,
		nr_lokalu int check (nr_lokalu > 0),
		nr_budynku int check(nr_budynku > 0) not null,
		ulica varchar(40) not null,
		miasto varchar(40) not null,
		wojewodztwo varchar(40) not null

	)
go

if not exists ( SELECT *
                 FROM INFORMATION_SCHEMA.TABLES where  TABLE_NAME = 'Osoba')
	create table Osoba(
		id int PRIMARY KEY identity,
		imie varchar(20) not null,
		nazwisko varchar(20)not null,
		adres int foreign key references Adres(id) not null,

	)
go
if not exists ( SELECT *
                 FROM INFORMATION_SCHEMA.TABLES where  TABLE_NAME = 'Produkt')
	create table Produkt(
		id int PRIMARY KEY identity ,
		Nazwa varchar(100) not null,
		cena_netto float check (cena_netto > 0) not null,
		vat float check (vat > 0) not null,
		)
go
if not exists ( SELECT *
                FROM INFORMATION_SCHEMA.TABLES where  TABLE_NAME = 'Uzytkownicy')
create table Uzytkownik(
                           id    int primary key identity,
                           login varchar(30)                                                                 not null,
                           haslo varchar(30)                                                                 not null,
                           typ   varchar(15) check (typ = 'Manager' or typ = 'Klient' or typ = 'Sprzedawca') not null,
                           osoba int foreign key references Osoba (id),
)
go
insert into Adres values(1, 1, 'Dluga', 'Gdansk', 'Pomorskie')
insert into Adres values(2, 2, 'Szeroka', 'Gdansk', 'Pomorskie')
insert into Adres values(3, 3, 'Wojska Polskiego', 'Gdansk', 'Pomorskie')
go

insert into Osoba values('Andrzej', 'Kowalski', 1)
insert into Osoba values('Ania', 'Kowalska', 1)
insert into Osoba values('Grzegorz', 'Nowak', 2)
go
insert into Produkt values('Intel core i7-9700K', 1600, 0.23, 1)
insert into Produkt values('Intel core i7-9900K', 2200, 0.23, 2)

go
insert into Uzytkownik values ('temp', 'temp123', 'Manager', 1)
insert into Uzytkownik values ('Klient', 'temp123', 'Klient', 1)
insert into Uzytkownik values ('S', 'temp123', 'Sprzedawca', 1)
