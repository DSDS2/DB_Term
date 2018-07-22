'''
Created on 2018. 7. 19.https://lh3.googleusercontent.com/a/default-user=s128

@author: 6조, 박중규, 민경학 , 박용훈


'''
import pymysql


IS_DEBUG=False
def print_debug_msg(*msg):
    if IS_DEBUG: print('[DEBUG] ',msg)

class ConcertManagement:
    def __init__(self):
        self.menu_func=[]
        
    import pymysql.cursors

# Connect to the database

    def send_query(self, query, values=None, is_commit=False):
        print_debug_msg("SEND QUERY:", query)
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
    
    '''
    @function : formatted_print 함수는 Query 결과 딕셔너리를 파라미터로 받아 그 결과를 포맷팅한 문자열로 변환하여 리턴한다.
    @example
                result = self.send_query("SELECT * FROM audience;")        
                print(self.formatted_print(result))
                위 코드와 같이 실행 시 아래와 같은 결과가 출력 됨을 확인 할 수 있음.
                ------------------------------------------------
                a_gender         a_name    a_id    a_age    
                ------------------------------------------------
                       M     Choi minho       1       27    
                       F    park minwoo       2       17    
                ------------------------------------------------
    '''    
    def formatted_print(self, records, col_names=[]):
#         col_names=['id', 'name', ...]
#         records=[{'id':'12', 'name':'aaaa bbb', ...}, ...]
        print_debug_msg(records)
        if len(col_names)>0 and len(col_names)!=len(records) : 
            self.print_msg("ERROR", "formatted print error: length missmatch between column and records")
            return None
        keys = records[0].keys()
        key_dict={}        
        for r in records:
            for key in keys:
                if key_dict.__contains__(key)==False:                     
                    key_dict[key]=len(key)
                if key_dict[key] < len(str(r[key])): key_dict[key]=len(r[key])
        dividebar=""
        table_head = ""  
        formatted_str=""  
        if len(col_names) > 0 :
            pass 
#             formatted_str+=table_head%(*col_names) +"\n"
        else: 
            i=0
            for i in range(0,len(keys)): 
                value=''
                if bool(key_dict[list(keys)[i]]) :  value=key_dict[list(keys)[i]]
                table_head+="{"+str(i)+":<"+str(value)+"}     "                 
            table_head=table_head.format(*list(keys))    +"\n"
            
        format_str = ""
        for key in keys:
            format_str+="{"+str(key)+":<"+str(key_dict[key])+"}     "
            dividebar+='-'*(key_dict[key]+5)            
          
        for r in records:
            formatted_str+=format_str.format(**r)    +"\n"
        
        formatted_str=dividebar+"\n"+table_head+dividebar+"\n"+formatted_str+dividebar+"\n"
                
        return formatted_str    
    
        
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
    
    def print_all_buildings(self):
      #1 모든 공연장 정보 출력
        result = self.send_query('select building.b_id, building.b_name, building.b_loc, building.b_cap, count(perf_build.b_id) as b_ass'
                                  ' from building left outer join perf_build on building.b_id=perf_build.b_id '
                                  'group by building.b_id, building.b_name, building.b_loc, building.b_cap order by building.b_id;')
        print(self.formatted_print(result))    
        input("Press any key to continue...")    
    def print_all_performances(self):
      #2 모든 공연 정보 출력
        result = self.send_query('select performance.p_id, performance.p_name, performance.p_type, performance.p_price, count(distinct a_id) as booked'
                                 ' from performance left outer join perf_audi on performance.p_id=perf_audi.p_id'
                                 ' group by performance.p_id, performance.p_name, performance.p_type, performance.p_price order by performance.p_id;')
        print(self.formatted_print(result))
        input("Press any key to continue...")    
    def print_all_audiences(self):
        #3 모든 관객 정보 출력
        result = self.send_query('select a_id, a_name, a_gender, a_age from audience order by a_id;')
        print(self.formatted_print(result))
        input("Press any key to continue...")  
    def insert_a_new_building(self):
      #4 공연장 insert
        name = str(input('Building name : '))
        loc= str(input('Building location : '))
        cap = int(input('Building capacity : '))
        self.send_query("insert into building (b_name, b_loc, b_cap) values (%s,%s,%s);",(name,loc,cap),True)
        print("A building is successfully inserted")
        input("Press any key to continue...")
    def remove_a_new_building(self):
      #5 공연장 delete
        b_id = int(input('Building ID : '))
        result =self.send_query("select b_id from building where b_id=%s;",b_id)
        #각 Table에 공연장과 관련된 공연 및 예매 내역 삭제
        if bool(result):
            self.send_query("delete from book where p_id in (select p_id from perf_build where b_id=%s);",b_id,True)
            self.send_query("delete from perf_build where b_id=%s;",b_id,True)
            self.send_query("delete from building where b_id = %s;",b_id,True)
            print("A building is successfully deleted")
        else:
          self.print_msg("ERROR", 'Building id : %s is not exist' % (b_id))
        input("Press any key to continue...")
        
    def insert_a_new_performance(self):
      #6 공연 추가
        name = str(input('Performance name : '))
        type= str(input('Performance type : '))
        price = int(input('Performance price : '))
        self.send_query("insert into performance (p_name, p_type, p_price) values (%s,%s,%s);",(name,type,price),True)
        print("A performance is successfully inserted")
        pass
    def remove_a_performance(self):
      #7 공연 delete
        p_id = int(input('Performance ID : '))
        result =self.send_query("select p_id from performance where p_id=%s;",p_id)
        #각 Table에 공연과 관련된 예매 정보 삭제
        
        if bool(result):
            self.send_query("delete from book where p_id = %s;",p_id,True)
            self.send_query("delete from performance where p_id = %s;",p_id,True)
            print("A performance is successfully deleted")
        else:
          self.print_msg("ERROR", 'Performance id : %s is not exist' % (p_id))
        input("Press any key to continue...")
    def insert_a_new_audience(self):
        # 8 관객 추가
        name = str(input('Audience name : '))
        gender= str(input('Audience gender : '))
        age = int(input('Audience age : '))
        result = self.send_query("insert into audience (a_name, a_gender, a_age) values (%s,%s,%s);",(name,gender,age),True)        
        print("An audience is successfully inserted")
        input("Press any key to continue...")
    def remove_an_audience(self):
      # 9 관객 삭제
        p_id = int(input('Audience ID : '))
        result =self.send_query("select a_id from audience where a_id=%s;",p_id)
        #각 Table에 공연과 관련된 예매 정보 삭제
        if bool(result):
            self.send_query("delete from book where a_id = %s;",a_id,True)
            self.send_query("delete from audience where a_id = %s;",a_id,True)
            print("A performance is successfully deleted")
        else:
          self.print_msg("ERROR", 'Audience id : %s is not exist' % (a_id))
        input("Press any key to continue...")       
    def assign_a_performance_to_a_building(self):
      #10 공연 배정
        b_id = int(input('Building ID : '))
        check_b = self.send_query("select distinct b_id from building where b_id=%s;",b_id)
        if bool(check_b) == False:
            print("There is no %s building" %(b_id))
        else:
            p_id = int(input('Performance ID : '))
            # 이미 다른 공연장에 배치되었는지 확인
            check_p = self.send_query("select distinct p_id from perf_build where p_id=%s;",p_id)
            if bool(check_p)==False:
                self.send_query('insert into perf_build values'
                                ' (%s, (select p_name from performance where p_id=%s), %s, (select b_name from building where b_id=%s))',(p_id,p_id,b_id,b_id),True)
                print("A performance %s is successfully arranged to %s building" %(p_id,b_id))
            else:
                self.print_msg("ERROR", 'Performance id : %s is already arranged' % (p_id))
        input("Press any key to continue...")
    def book_a_performance(self):
        #11 공연예매
        # 입력: 공연ID, 관객ID, 좌석번호 리스트(int list) 
        # 한 관객은 여러개의 공연을 예매할 수 있음 / 여러 좌석을 예매할 수 있음
        # 공연의 좌석번호는 정수(int)이며, 1에서 부터 해당 공연이 배정 된 공연장의 정원 값까지 가질 수 있음
        #    *좌석 번호 리스트의 좌석번호 값들 중 하나라도 범위를 벗어난다면 에러 메시지 출력
        #    *좌석 번호 리스트에서 각 좌석 번호는 콤마로 구분
        #    *좌석 번호 리스트의 좌석 번호 중 하나라도 이미 예매되어 있다면 예매 실패
        #    *예매 성공 시 총 티켓가격 출력
        #        -총 티겟 가격은 티켓 수X티켓 하나당 가격으로 계산 됨
        #        -티켓 하나당 가격은 나이에 따라 달라짐
        #            +1~7:무료 / 8~12:50%할인 / 13~18: 20%할인 / 19이상 : 정가
        #        -계산 된 총 티켓 가격은 소수점 첫째자리에서 반올림
        #    *공연이 공연장에 배정되지 않았다면 에러 메시지 출력
        ''' WORK FLOW
             a. 메뉴선택(#11-예매)
             b. 예매정보 입력 및 검증
                 b-1. 공연 ID 입력 :공연ID 존재 확인, 공연장 배정 확인.
                 b-2. 관객 ID 입력 :관객ID 존재 확인                 
                 b-3. 좌석 리스트 입력: 중복여부 확인
             c. b완료 후 이상이 없으면 예매 확정 후 티켓가격 출력
                 c-1. 할인정보 적용
        '''
        #전체 관객정보 출력        
#         result = self.send_query("SELECT a_id as id, a_name as name, a_gender as gender, a_age as age FROM audience ORDER BY id ASC;")
#         print(self.formatted_print(result))
        
        IS_SUCCESS, RETURN_MSG=True, ''
        
        p_id=input('Performance ID: ')
        if not bool(p_id) : p_id='-1'
        a_id=input('Audience ID: ')
        if not bool(a_id) : a_id='-1'
        s_nums=input('Seat number: ')        
        if not bool(s_nums) : s_nums=[]
        else: s_nums= s_nums.split(sep=',')
        
        temp=[]
        for s in s_nums: 
            if bool(s) : temp.append(s)
        s_nums=temp
        
        print_debug_msg("[Performance ID]:%s, [Audience ID]:%s, [Seat number]:%s"%(p_id, a_id, str(s_nums)))
#         try:
        # Check Performance ID 
        per_result = self.send_query('SELECT p_id, p_name, building.b_id, building.b_name, b_loc, b_cap FROM perf_build, building '
                                     ' WHERE perf_build.b_id = building.b_id AND p_id=%s '%p_id)
        print_debug_msg('perf_build & building:', per_result)
        capa=0
        #print(len(per_result))
        if len(per_result)==1: capa=per_result[0]['b_cap']  
        RETURN_MSG=''      
        if len(per_result) == 0: IS_SUCCESS, RETURN_MSG=False, 'PERFORMANCE_ID_IS_NOT_EXIST'
#         print_debug_msg("Query Result Info.:",len(per_result), per_result)        
        
        # Check Audience ID 
        RETURN_MSG=''
        aud_result = self.send_query('SELECT * FROM audience WHERE a_id in (%s)'%a_id)
        aud_age=-1
        if len(aud_result) == 0: IS_SUCCESS, RETURN_MSG=False,'AUDIENCE_ID_IS_NOT_EXIST'
        else: aud_age= aud_result[0]['a_age']
        print_debug_msg("Query Result Info.:",len(aud_result), aud_result)
        
        # Check Seat numbers 
        RETURN_MSG=''
        seat_result = self.send_query('SELECT seat_num FROM book WHERE p_id=%s '%p_id)            
        print_debug_msg("Query Result Info.:",len(seat_result), seat_result) 
        booked_seats = []
        for r in seat_result: booked_seats.append(r['seat_num'])
        for seat in s_nums:
            seat=str(seat).strip()
            if not bool(seat): continue
            if int(seat) in booked_seats: 
                IS_SUCCESS,RETURN_MSG=False,"SEAT_IS_ALREADY_BOOKED"
                break
            try:
                if int(seat) > capa    :
                    IS_SUCCESS,RETURN_MSG=False,"SEAT_NUM_IS_OVER_CAPA."
                    break
            except Exception:
                IS_SUCCESS,RETURN_MSG=False,"INVALID_SEAT_NUMBER(%s)"%seat
        if not IS_SUCCESS: print_debug_msg(RETURN_MSG)
        else:
            values=''
            cnt=0
            for seat in s_nums:
                value='(%s, %s, %s)'%(a_id, p_id, seat)
                if cnt!=0 and (cnt)< len(s_nums):
                    values+=','
                values+=value
                cnt+=1

            self.send_query("INSERT INTO book (a_id, p_id, seat_num) VALUES %s"%values, is_commit=True)
            
            # Calculate booking charge    
            price =0
            perf_result = self.send_query('SELECT p_price FROM performance WHERE p_id=%s'%p_id)
            if len(perf_result)==1: price=perf_result[0]['p_price']
            print_debug_msg('PRICE:', price)
            discount_rate=0
            if 0< aud_age <= 7: discount_rate=1
            elif 7< aud_age <=12: discount_rate=0.5
            elif 12< aud_age <=18: discount_rate=0.2
            else : discount_rate=0
            price = round(price*(1-discount_rate)*len(s_nums))
            print('Total ticket price is',price)
        if IS_SUCCESS: print("Successfully book a performance")
        else: self.print_msg("ERROR", "Failed to make a booking for [Performance ID]:%s, [Audience ID]:%s, [Seat number]:%s"%(p_id, a_id, str(s_nums)))
        input("Press any key to continue...")
#         except Exception as e: 
        self.print_msg("ERROR", "Failed to make a booking for [Performance ID]:%s, [Audience ID]:%s, [Seat number]:%s"%(p_id, a_id, str(s_nums)))                    
        
    
    def print_all_performances_which_assigned_at_a_building(self):
        #12
        bid = int(input('Input building ID : '))
        result = self.send_query("SELECT pb.p_id, p.p_name, p.p_type,p.p_price, count(distinct b.seat_num) as seat"
                                 " FROM perf_build as pb left outer join performance as p on pb.p_id = p.p_id , book as b"
                                 " WHERE pb.b_id =%s and pb.p_id = b.p_id group by pb.p_id, p.p_name, p.p_type,p.p_price;" %(bid))       
        if bool(result):
            print(self.formatted_print(result))
        else:
            self.print_msg("ERROR", 'Building id : %s is not exist' % (bid))        
        input("Press any key to continue...")
    def print_all_audiences_who_booked_for_a_performance(self):
        #13
        pid = int(input('Input Performance ID : '))
        result = self.send_query("SELECT a.a_id, a.a_name, a.a_gender, a.a_age FROM book left outer join audience a on book.a_id = a.a_id where book.p_id = %s" % (pid))
        
        if bool(result):
            print(self.formatted_print(result))
        else:
            self.print_msg("ERROR", 'Performance id : %s is not exist' % (pid))     
        input("Press any key to continue...")
    def print_ticket_booking_status_of_a_performance(self):
        #14
        pid = int(input('Input Performance ID : '))
        #간소화필요
        result = self.send_query("SELECT book.seat_num, book.a_id, building.b_cap FROM book left outer join audience on book.a_id = audience.a_id, building, "
                                "perf_build where perf_build.b_id = building.b_id and book.p_id = perf_build.p_id and book.p_id = %s" % (pid))
        #가정 1. 좌석을 예약하지않은 경우 별도로 DB에 입력하지않음 : DB공간의 낭비 방지를 위한목적
        if bool(result):
            print(result)
            cnt = 0
            print('--------------------------------------------')  
            print('seat_number            audience_id')            
            print('--------------------------------------------')  
            #아래코드 너무 지저분해서... 리뷰좀해주세요
            for i  in range(1, result[0]['b_cap']+1): # 전체 seat number를 구하기위해 b_cap값을 for문돌린다
                if (cnt<len(result)) : #체크구문없으면 cnt의 마지막 index 에서 문제가 생김.. ㅡㅡ;
                    if( i == result[cnt]['seat_num'] ): #예약된자리면 예약된정보를 출력하고
                        print(result[cnt]['seat_num'],'','',result[cnt]['a_id'],sep='\t')
                        cnt += 1
                    else:
                        print(i) #예약된자리가아니면 seat_num만 찍어줌
                else: #요거도 seat_num만찍어주기위함.. 코드똥같음 ㅠㅠ
                    print(i)
            print('--------------------------------------------') 
        else:
            self.print_msg("ERROR", 'Performance id : %s is not exist' % (pid)) 
        input("Press any key to continue...")
    def exit(self):
        print('Bye!')
    def reset_database(self):
        r = input('Are you sure to delete all database?(N or Y) : ')
        if r.upper() == 'Y':
            #foreign key로 인해 table 생성과 삭제시 순서에 주의해야한다.                                                  
            #아래는 쿼리가 한방에 수행이안되서 어쩔수없이 리스트에서 포문을 돌림... 모아서 execute하면 에러남 ㅠㅠ
            query = []
            query.append('DROP TABLE IF EXISTS `perf_audi`')
            query.append('DROP TABLE IF EXISTS `perf_build`;')
            query.append('DROP TABLE IF EXISTS `book`;')
            query.append('DROP TABLE IF EXISTS `audience`;')
            query.append('DROP TABLE IF EXISTS `building`;')
            query.append('DROP TABLE IF EXISTS `performance`;')
            query.append('''CREATE TABLE IF NOT EXISTS `audience` (
  `a_id` int(11) NOT NULL AUTO_INCREMENT,
  `a_name` varchar(200) NOT NULL,
  `a_gender` varchar(1) NOT NULL,
  `a_age` int(11) NOT NULL,
  PRIMARY KEY (`a_id`),
  KEY `a_name` (`a_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;''')
            query.append('''CREATE TABLE IF NOT EXISTS `building` (
  `b_id` int(11) NOT NULL AUTO_INCREMENT,
  `b_name` varchar(200) NOT NULL,
  `b_loc` varchar(200) NOT NULL,
  `b_cap` int(11) NOT NULL,
  PRIMARY KEY (`b_id`),
  KEY `b_name` (`b_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;''')
            query.append('''CREATE TABLE IF NOT EXISTS `performance` (
  `p_id` int(11) NOT NULL AUTO_INCREMENT,
  `p_name` varchar(200) NOT NULL,
  `p_type` varchar(200) NOT NULL,
  `p_price` int(11) NOT NULL,
  PRIMARY KEY (`p_id`),
  KEY `p_name` (`p_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;''')
                        
            query.append('''CREATE TABLE IF NOT EXISTS `book` (
  `book_id` int(11) NOT NULL AUTO_INCREMENT,
  `a_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `seat_num` int(11) NOT NULL,
  PRIMARY KEY (`book_id`),
  KEY `a_id` (`a_id`),
  KEY `p_id` (`p_id`),
  CONSTRAINT `book_ibfk_1` FOREIGN KEY (`a_id`) REFERENCES `audience` (`a_id`),
  CONSTRAINT `book_ibfk_2` FOREIGN KEY (`p_id`) REFERENCES `performance` (`p_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;''')

            query.append('''CREATE TABLE IF NOT EXISTS `perf_audi` (
  `p_id` int(11) NOT NULL,
  `p_name` varchar(200) NOT NULL,
  `a_id` int(11) NOT NULL,
  `a_name` varchar(200) NOT NULL,
  PRIMARY KEY (`p_id`),
  KEY `p_name` (`p_name`),
  KEY `a_id` (`a_id`),
  KEY `a_name` (`a_name`),
  CONSTRAINT `perf_audi_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `performance` (`p_id`),
  CONSTRAINT `perf_audi_ibfk_2` FOREIGN KEY (`p_name`) REFERENCES `performance` (`p_name`),
  CONSTRAINT `perf_audi_ibfk_3` FOREIGN KEY (`a_id`) REFERENCES `audience` (`a_id`),
  CONSTRAINT `perf_audi_ibfk_4` FOREIGN KEY (`a_name`) REFERENCES `audience` (`a_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;''')
            query.append('''CREATE TABLE IF NOT EXISTS `perf_build` (
  `p_id` int(11) NOT NULL,
  `p_name` varchar(200) NOT NULL,
  `b_id` int(11) NOT NULL,
  `b_name` varchar(200) NOT NULL,
  PRIMARY KEY (`p_id`),
  KEY `p_name` (`p_name`),
  KEY `b_id` (`b_id`),
  KEY `b_name` (`b_name`),
  CONSTRAINT `perf_build_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `performance` (`p_id`),
  CONSTRAINT `perf_build_ibfk_2` FOREIGN KEY (`p_name`) REFERENCES `performance` (`p_name`),
  CONSTRAINT `perf_build_ibfk_3` FOREIGN KEY (`b_id`) REFERENCES `building` (`b_id`),
  CONSTRAINT `perf_build_ibfk_4` FOREIGN KEY (`b_name`) REFERENCES `building` (`b_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
            ''')            
            for i in query:
                result = self.send_query(i,None,True)
        else:
            print('Cancelled')
        input("Press any key to continue...")
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
            
          
          
      