
create table if not exists Uzytkownik(
                           id    integer primary key autoincrement,
                           login varchar(30)                                                                 not null,
                           haslo varchar(30)                                                                 not null,
                           typ   varchar(15) check (typ = 'Manager' or typ = 'Klient' or typ = 'Sprzedawca') not null,
                           osoba integer ,
                           foreign key(osoba) references Osoba (id)
)