'''
Created on 2018. 7. 19.

@author: 6조, 박중규, 민경학 , 박용훈
'''
class ConcertManagement:
    
    def show_menu(self):
        print('''
    ============================================================
     1. print all buildings
     2. print all performances
     3. print all audiences
     4. insert a new building
     5. remove a new building
     6. insert a new performance
     7. remove a performance
     8. insert a new audience
     9. remove an audience 
    10. assign a performance to a building
    11. book a performance
    12. print all performances which assigned at a building
    13. print all audiences who booked for a performance
    14. print ticket booking status of a performance
    15. exit
    16. reset database
    ============================================================
    ''')
     
    def print_msg(self, type, msg):
        msg = msg_format = "[{TYPE}] {MSG}".format(TYPE=type,MSG=msg)
        print(msg)

if __name__ == '__main__':
    isRun = True
    while isRun:
        cm = ConcertManagement()
        cm.show_menu()
        sel=-1
        try:
            sel = int(input("Select Menu#: ")) 
        except ValueError as e:
            cm.print_msg("ERROR", "숫자만 입력해주세요")
            input("Press any key to restart...")
        if sel == 15: isRun=False    
            
            