'''
Created on 2018. 7. 19.

@author: 6조, 박중규, 민경학 , 박용훈
'''
import pymysql
class ConcertManagement:
    def __init__(self):
        self.menu_func=[]
        
    import pymysql.cursors

# Connect to the database

    def send_query(self, query, values=None, is_commit=False):
        connection = pymysql.connect(
            host='147.46.215.246',
            port=33060,
            user='yh100788@naver.com',
            password='dbintro',
            db='ds2_db32',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
        result = None
        
        try:
            with connection.cursor() as cursor:
                if bool(values) : cursor.execute(query, values)
                else: cursor.execute(query)
                if is_commit:
                    connection.commit()
                else:
                    result = cursor.fetchall()
        finally:
            connection.close()
        return result  
    
    
        
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
    
    
    def run_menu(self, menu_num):
        if self.menu_func ==[]:
            self.menu_func=[
                self.print_all_buildings
                ,self.print_all_performances
                ,self.print_all_audiences
                ,self.insert_a_new_building
                ,self.remove_a_new_building
                ,self.insert_a_new_performance
                ,self.remove_a_performance
                ,self.insert_a_new_audience
                ,self.remove_an_audience
                ,self.assign_a_performance_to_a_building
                ,self.book_a_performance
                ,self.print_all_performances_which_assigned_at_a_building
                ,self.print_all_audiences_who_booked_for_a_performance
                ,self.print_ticket_booking_status_of_a_performance
                ,self.exit
                ,self.reset_database
                ]
        self.menu_func[sel-1]()
    def formatted_print(self, records, col_names=[]):
#         col_names=['id', 'name', ...]
#         records=[{'id':'12', 'name':'aaaa bbb', ...}, ...]
        if len(col_names)>0 and len(col_names)!=len(records) : 
            self.print_msg("ERROR", "formatted print error: length missmatch between column and records")
            return None
        keys = records[0].keys()
        key_dict={}        
        for r in records:
#             print(r)
            for key in keys:
                if key_dict.__contains__(key)==False:                     
                    key_dict[key]=len(key)
                if key_dict[key] < len(str(r[key])): key_dict[key]=len(r[key])
        dividebar=""
        format_str = ""  
#         print(key_dict)      
        for key in keys:            
            format_str+= "%"+str(key_dict[key])+"s\t"
            dividebar+='-'*(key_dict[key]+4) 
        formatted_str=""
        if len(col_names) > 0 : 
            formatted_str+=format_str%(col_names) +"\n"
        
        for r in records:
            print(format_str,"---------",r.values())
            vstr = ''
            print(list(r.values()))
            for i in range(0, len( list(r.values()))):    
                print(list(r.values())[i])            
                vstr+="'"+str(list(r.values())[i])+"'"
                if( i< len(r.values())-1 ): vstr+=','
            formatted_str+=format_str%(vstr) +"\n"    
                
        return formatted_str    
        
    def print_all_buildings(self):
        print("#1")
#         print(self.send_query("SELECT * FROM audience;"))
#         result = self.send_query("SELECT * FROM audience;")        
        result = self.send_query("SELECT * FROM audience WHERE a_id='%s';", 2)
        print(self.formatted_print(result))
#         print('--------------------------------------------')
#         format_str= "%2s\t%20s\t%10s"                
#         print(format_str%('id', 'name', 'age'))
#         for r in result:
#             print(format_str%(r['a_id'], r['a_name'],r['a_age'] ))
#         print('--------------------------------------------')    
        pass    
    def print_all_performances(self):
        print("#2")
        pass    
    def print_all_audiences(self):
        print("#3")
        pass
    def insert_a_new_building(self):
        print("#4")
        pass
    def remove_a_new_building(self):
        pass
    def insert_a_new_performance(self):
        pass
    def remove_a_performance(self):
        pass
    def insert_a_new_audience(self):
        pass
    def remove_an_audience(self):
        pass
    def assign_a_performance_to_a_building(self):
        pass
    def book_a_performance(self):
        pass
    def print_all_performances_which_assigned_at_a_building(self):
        pass
    def print_all_audiences_who_booked_for_a_performance(self):
        pass    
    def print_ticket_booking_status_of_a_performance(self):
        pass
    def exit(self):
        pass
    def reset_database(self):
        pass
    
if __name__ == '__main__':
    isRun = True
    while isRun:
        cm = ConcertManagement()
        cm.show_menu()
        sel=-1
        try:
            sel = int(input("Select Menu#(1-16): ")) 
            if sel <1 or sel>16:
              raise ValueError
        except ValueError as e:
            cm.print_msg("ERROR", "(1~16) 사이의 숫자만 입력해주세요")
            input("Press any key to continue...")
        except Exception as e:
            print(e)
        if sel == 15: isRun=False   
        cm.run_menu(sel)  
            