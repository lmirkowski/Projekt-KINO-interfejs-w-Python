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
                while(True):
                    dec = input('1.Select, 2.Delete, 3.Insert, 4.Logout')
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
                        print('Zły wybór')
            elif(perm.upper() == 'U'):
                while(True):
                    dec = input('1.Select, 2.Logout')
                    if(dec == '1'):
                        self.select()
                    elif(dec == '2'):
                        self.connClose()
                        break
                    else:
                        print('Zły wybór')               
            else:
                print('błąd logowania!')
        
    def login(self):
        mail = input('podaj maila: ')
        passwd = input('podaj hasło: ')
        self.c.execute('SELECT perm FROM login WHERE mail=%s AND pass=%s', (mail, passwd))
        try:
            perm = self.c.fetchall()[0][0]
        except:
            perm = '0'
        return perm
    def connString(self):
        self.conn = pymysql.connect('localhost','puser','abc123','warrior')
        self.c = self.conn.cursor()
    def select(self):
        self.c.execute('SELECT * FROM characters;')
        for row in self.c.fetchall():
            print('%3i %15s %15s %15s %5i %5i' % (row[0], row[1], row[2], row[3], row[4], row[5]))
    def delete(self):
        try:    
            self.select()
            id = int(input('ID do usunięcia: '))
            self.c.execute('DELETE FROM characters WHERE id=%s;', id)
            self.conn.commit()
            self.select()
        except:
            print('Podałeś błędny id!')
            
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
            print('podałeś niepoprawne dane!')
    def connClose(self):
        self.conn.close()
db = DBConn()
'''
class User:
    def __init__(self):
       
'''