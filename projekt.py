# -*- coding: utf-8 -*-
import pymysql

class DBConn:
    def __init__(self):
        
        while(True):
            quit = input('1.Logowanie, 2.Wyjście  ')
            if(quit == '2'):
                break
            self.connString()
            perm = self.login()
            if(perm.upper() == 'A'):
                print('---------------------------------------------------------------')
                print('            ZALOGOWANO JAKO ADMINISTRATOR SYSTEMU              ')
                print('---------------------------------------------------------------')                
                self.uprAdmin()
                
            elif(perm.upper() == 'U'):
                print('---------------------------------------------------------------')
                print('             WITAMY W SYSTEMIE REZERWACJI BILETÓW              ')
                print('---------------------------------------------------------------')                
                self.uprUser()
                            
            else:
                print('Błąd logowania!')
                        
    def login(self): # logowanie - pobiera maila i hasło z mysql i sprawdza przypisane uprawnienia
        email = input('Podaj swój email: ')
        password = input('Podaj swoje hasło: ')
        self.c.execute('SELECT perm FROM logowanie WHERE email=%s AND password=%s;', (email, password))
        try:
            perm = self.c.fetchall()[0][0]
        except:
            perm = '0'
        return perm
    
    def uprAdmin(self): #wyświetla uprawnienia administratora
        while(True):
            dec = input('1.Select, 2.Delete, 3.Insert, 4.Wyloguj ')
            if(dec == '1'):
                self.select()
            elif(dec == '2'):
                self.delete()
            elif(dec == '3'):
                self.insert()
            elif(dec == '4'):
                self.connClose()
                break
            else:
                print('Zły wybór ')
                
    def uprUser(self): #wyświetla uprawnienia usera - dalej wybór filmu i rezerwacja
        while(True):
            print('')
            dec = input('1.Wyświetl listę filmów,    2.Wyloguj ')
            if(dec == '1'):
                self.selectMovie()
                self.showChosenMowie(id)
                self.chooseShowing()
            elif(dec == '2'):
                self.connClose()
                break
            else:
                print('Zły wybór')

    def connString(self): # Ustanowienie połączenia z bazą mysql
        self.conn = pymysql.connect(host='localhost', user='project', password='project', db='kinokopia', charset='utf8', use_unicode=True)
        self.c = self.conn.cursor()
        
    def selectMovie(self): # Wyświetla listę tytułów dostępnych filmów 
        self.c.execute('SELECT idfilm, title FROM film;')
        for row in self.c.fetchall():
            print('%2i %-50s' % (row[0], row[1]))
            
    def showChosenMowie(self, id):   # Wyświetla opis filmu wybranego przez użytkownika oraz dostępne seanse
        print('--------------------------------------------')
        idfilm = input('Podaj numer filmu ')
        print('--------------------------------------------')
        id = idfilm 
        self.c.execute('SELECT idfilm, title, rok_prod, kraj, rezyser, czas_trwania, ogr_wiek, gatunek, obsada, opis FROM film where idfilm=%s;', id)
        for row in self.c.fetchall():
            print('%2i.| Tytuł: %-35s \n Rok produkcji: %-4i | Kraj: %-15s | Reżyser: %-25s \n Czas trwania: %-10s | Ograniczenie wiekowe %-3s | Gatunek: %-30s | Obsada: %-120s | Opis: %-500s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9    ])) 
        self.c.execute('SELECT * FROM seans WHERE film_idfilm=(SELECT idfilm from film where idfilm=%s);', id)
        for row in self.c.fetchall():
            print('--------------------------------------------')
            print('Dostępne seanse')
            print('--------------------------------------------')
            print('%2i %-15s %-15s' % (row[0], row[1], row[2]))   
            
    def chooseShowing(self): # Wybór seansu i biletów //nie oprogramowane zliczanie wybranych opcji przez użytkownika aby wyświetlało się podsumowanie rezerwacji
        print('--------------------------------------------')
        idseans = input('Wybierz seans ')
        print('')
        print('Cennik biletów: Noramlny 25 zł, Ulgowy 20 zł')
        print('')
        input('Liczba biletów normalnych:  ')
        input('Liczba biletów ulgowych::  ')
        
        
    def select(self): # Wyświetla wybór: lista filmów lub lista seansów
        dec = input('1.Lista filmów, 2.Lista seansów, 3.Wyloguj ')
        if(dec == '1'):
            self.selectMovie()
            self.showChosenMowieAdm(id)
        elif(dec == '2'):
            self.selectShowing()
        elif(dec == '3'):
            self.connClose()
        else:
            print('Zły wybór')
            
    def showChosenMowieAdm(self, id):   # Wyświetla opis filmu wybranego przez administratora
        print('--------------------------------------------')
        idfilm = input('Podaj numer filmu ')
        print('--------------------------------------------')
        id = idfilm 
        self.c.execute('SELECT idfilm, title, rok_prod, kraj, rezyser, czas_trwania, ogr_wiek, gatunek, obsada, opis FROM film where idfilm=%s;', id)
        for row in self.c.fetchall():
            print('%2i. Tytuł: %-35s \n Rok produkcji: %-4i | Kraj: %-15s | Reżyser: %-25s \n Czas trwania: %-10s | Ograniczenie wiekowe %-3s | Gatunek: %-30s \n| Obsada: %-120s \n| Opis: %-500s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])) 
            
    def selectShowing(self): # Wyświetla listę tytułów dostępnych seansów (dla admina)
        self.c.execute('SELECT * FROM seans;')
        for row in self.c.fetchall():
            print('%2i %-10s %-5s %-2i %-1i' % (row[0], row[1], row[2], row[3], row[4]))
            
    def deleteMovie(self, id): # Usuwanie rekordu o podanym ID z tabeli film 
        try:    
            self.selectMovie()
            id = int(input('Podaj ID filmu do usunięcia: '))
            self.c.execute('DELETE FROM film WHERE idfilm=%s;', id)
            self.conn.commit()
            self.selectMovie()
            print('\n********** Usunięto film o ID=%s **********'  % (id))
        except:
            print('Podałeś błędny id!')
            
    def deleteShowing(self, id): # Usuwanie rekordu o podanym ID z tabeli seans 
        try:    
            self.selectShowing()
            id = int(input('Podaj ID seansu do usunięcia: '))
            self.c.execute('DELETE FROM seans WHERE idseans=%s;', id)
            self.conn.commit()
            self.selectShowing()
            print('\n********** Usunięto seans o ID=%s **********'  % (id))
        except:
            print('Podałeś błędny id!')
            
    def delete(self): #Wybór: usunięcie rekordu z tabeli film lub seans
        print('--------------------------------------------------------------')
        dec = input('1.Usuń film z listy, 2.Usuń seans z listy, 3.Wyloguj ')
        print('--------------------------------------------------------------')
        if(dec == '1'):
            self.deleteMovie(id)
        elif(dec == '2'):
            self.deleteShowing(id)
        elif(dec == '3'):
            self.connClose()
        else:
            print('Zły wybór')
            
    def insert(self): # Wybór: dodanie rekordu do tabeli film lub seans
        print('--------------------------------------------------------------')
        dec = input('1.Dodaj film, 2.Dodaj seans, 3.Wyloguj ')
        print('--------------------------------------------------------------')
        if(dec == '1'):
            self.insertMovie()
        elif(dec == '2'):
            self.insertShowing()
        elif(dec == '3'):
            self.connClose()
        else:
            print('Zły wybór')
            
    def insertMovie(self): # Dodanie rekordu to tabeli film
        try:
            title = input('Tytuł filmu: ')
            rezyser = input('Reżyser: ')
            rokprod = int(input('Rok produkcji: '))
            czas = input('Czas trwania: ')
            kraj = input('Kraj: ')
            obsada = input('Obsada: ')
            ogrwiek = input('Ogr. wiekowe: ')
            gatunek = input('Gatunek: ')
            opis = input('Opis: ')
            self.c.execute('insert into film (title,rezyser,rok_prod,czas_trwania,kraj,obsada,ogr_wiek,gatunek,opis) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);', (title,rezyser,rokprod,czas,kraj,obsada,ogrwiek,gatunek,opis))
            self.conn.commit()
            self.select()
        except:
            print('Podałeś niepoprawne dane! ')
            
    def insertShowing(self): # Dodanie rekordu do tabeli seans
        try:
            data = input('Data seansu: ')
            godzina = input('Godzina seansu: ')
            filmidfilm = int(input('ID filmu: '))
            salaidsala = int(input('ID sali: '))
            self.c.execute('insert into seans (data,godzina,film_idfilm,sala_idsala) values (%s, %s, %s, %s);', (data,godzina,filmidfilm,salaidsala))
            self.conn.commit()
            self.select()
        except:
            print('Podałeś niepoprawne dane! ')
            
    def connClose(self):   # Zamknięcie połączenia z bazą mysql
        self.conn.close()
        print('\n\n\t\t***** ZOSTAŁEŚ WYLOGOWANY Z SYSTEMU *****\n\n\t\tProjekt i wykonanie: Łukasz Mirkowski 2018')
        while(True):
            dec = input('\nAby ponownie zalogować wybierz 1\n')
            if(dec == '1'):
                self.__init__()        
    
    
db = DBConn()
