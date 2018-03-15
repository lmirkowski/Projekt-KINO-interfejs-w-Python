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
                        
    def login(self):
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

    def connString(self):
        self.conn = pymysql.connect('localhost','project','project','kinokopia')
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
            
    def chooseShowing(self):
        print('--------------------------------------------')
        idseans = input('Wybierz seans ')
        print('')
        print('Cennik biletów: Noramlny 25 zł, Ulgowy 20 zł')
        print('')
        input('Liczba biletów normalnych:  ')
        input('Liczba biletów ulgowych::  ')
        
        
    def select(self):
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
            print('%2i.| Tytuł: %-35s \n Rok produkcji: %-4i | Kraj: %-15s | Reżyser: %-25s \n Czas trwania: %-10s | Ograniczenie wiekowe %-3s | Gatunek: %-30s | Obsada: %-120s | Opis: %-500s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9    ])) 
            
    def selectShowing(self): # Wyświetla listę tytułów dostępnych seansów (dla admina)
        self.c.execute('SELECT * FROM seans;')
        for row in self.c.fetchall():
            print('%2i %-10s %-5s %-2i %-1i' % (row[0], row[1], row[2], row[3], row[4]))
            
    def deleteMovie(self, id):
        try:    
            self.selectMovie()
            id = int(input('Podaj ID filmu do usunięcia: '))
            self.c.execute('DELETE FROM film WHERE idfilm=%s;', id)
            self.conn.commit()
            self.selectMovie()
        except:
            print('Podałeś błędny id!')
            
    def deleteShowing(self, id):
        try:    
            self.select()
            id = int(input('Podaj ID seansu do usunięcia: '))
            self.c.execute('DELETE FROM film WHERE idseans=%s;', id)
            self.conn.commit()
            self.select()
        except:
            print('Podałeś błędny id!')
            
    def delete(self):
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
            
    def insert(self):
        try:
            name = input('podaj imie: ')
            last = input('podaj nazwisko: ')
            type = input('podaj kategorie: ')
            exp = int(input('podaj doswiadczenie: '))
            lvl = int(input('podaj poziom: '))
            self.c.execute('insert into characters (name,last,type,experience,lvl) values (%s, %s, %s, %s, %s);', (name,last,type,exp,lvl))
            self.conn.commit()
            self.select()
        except:
            print('Podałeś niepoprawne dane! ')
            
    def connClose(self):
        self.conn.close()
    
    
db = DBConn()
