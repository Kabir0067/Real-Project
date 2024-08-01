from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import ReplyKeyboardRemove
from datetime import datetime,date,time
from telebot import TeleBot, types
from requests.utils import quote
from secret import *
import psycopg2
import logging
import requests


TEACHER_CHAT_ID = TEACHER_CHAT_ID_SC
TEACHER_BOT_TOKEN = TEACHER_BOT_TOKEN_SC

bot = TeleBot(bot_sc)

#Comandaho
commands = [
    types.BotCommand('/start', 'Барои оғоз кардани кор бо бот'),
    types.BotCommand('/help', 'Кумакрасони ва тарзи истифодаи бот'),
    types.BotCommand('/buttons', 'Тугмаҳои асосӣ'),
    types.BotCommand('/switch_to_a_new_group', 'Гузаштан ба гурӯҳи нав')
]
try:
    bot.set_my_commands(commands)
    print("Commands set successfully.")
except Exception as e:
    print(f"An error occurred: {e}")


#Payvast shudan ba database va close
def connection_database():
    connection = psycopg2.connect(
        database=database_sc,
        user=user_sc,
        host=host_sc,
        password=password_sc,
        port=port_sc
    )
    return connection

def close_connection(conn, cur):
    cur.close()
    conn.close()
##########################----------------------------------------------------------------------------------------------##########################


#Soakhtani Tablitsa
# def create_table_users():
#     conn = connection_database()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS USERS(
#                 USER_ID VARCHAR(150) PRIMARY KEY,
#                 FIRST_NAME VARCHAR(50),
#                 LAST_NAME VARCHAR(50),
#                 USERNAME VARCHAR(100),
#                 GROUP_NAME VARCHAR(50),
#                 ADDRESS VARCHAR(150) NULL,
#                 PHONE_NUMBER VARCHAR(13) NULL,
#                 EMAIL VARCHAR(100) NULL,
#                 DATE_OF_BIRTH DATE NULL,
#                 IS_ACTIVE BOOLEAN DEFAULT TRUE,
#                 REGISTRATION_DATE TIMESTAMP NULL
#             )
#         """)
#         conn.commit()
#         print("USERS table created successfully")
#     except Exception as e:
#         print(f'Error: {str(e)}')
#     finally:
#         close_connection(conn, cur)

# def create_table_came_and_went():
#     conn = connection_database()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS my_app_comeandwent(
#                 CW_ID SERIAL PRIMARY KEY,
#                 USER_ID VARCHAR(150),
#                 TIME_TO_COME TIMESTAMP null,
#                 TIME_TO_GO TIMESTAMP NULL,
#                 ABSENT_REASON TEXT NULL,
#                 LATE_REASON TEXT NULL,
#                 DATE DATE DEFAULT CURRENT_DATE,
#                 FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID)
#             )
#         """)
#         conn.commit()
#         print("my_app_comeandwent table created successfully")
#     except Exception as e:
#         print(f'Error: {str(e)}')
#     finally:
#         close_connection(conn, cur)

# def create_table_feedbacks():
#     conn = connection_database()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS FEEDBACK(
#                 FDB_ID SERIAL PRIMARY KEY,
#                 FEEDBACK_TEXT TEXT NULL,
#                 SUBMISSION_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
#                 USER_ID VARCHAR(150) NOT NULL,
#                 FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID)
#             )
#         """)
#         conn.commit()
#     except Exception as e:
#         print(f'Error {e}')
#     finally:
#         close_connection(conn, cur)
##########################----------------------------------------------------------------------------------------------##########################


#Ilovakunii user ba jadval
def add_user_in_table(user_id, first_name, last_name, username, group_name='', address='', phone_number='', email='', date_of_birth=None, is_active=True, registration_date=None):
    if registration_date is None:
        registration_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO api_customeruser(
                user_id, first_name, last_name, username, group_name, address, phone_number, email, date_of_birth, is_active, registration_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING
        """, (user_id, first_name, last_name, username, group_name, address, phone_number, email, date_of_birth, is_active, registration_date))
        conn.commit()
        print(f"User {user_id} added successfully.")
    except Exception as e:
        print(f'Error occurred while adding user {user_id}: {str(e)}')
        conn.rollback()  
    finally:
        close_connection(conn, cur)

def update_user_data(user_id, column, value):
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute(f"UPDATE api_customeruser SET {column} = %s WHERE user_id = %s", (value, str(user_id)))
        conn.commit()
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        close_connection(conn, cur)

def check_user_data(user_id):
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM api_customeruser WHERE user_id = %s", (str(user_id),))
        user_data = cur.fetchone()
        return user_data
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    finally:
        close_connection(conn, cur)
##########################----------------------------------------------------------------------------------------------##########################


#Giriftani nom nasab va username az chat
def update_first_name(message):
    if message.text=='/start' or message.text=='/help':
        bot.send_message(message.chat.id,'Ин команда аст!',)
        start(message)
    else:
        first_name = message.text
        user_id = message.chat.id
        logging.info(f'Updating first name for user {user_id}')
        update_user_data(user_id, 'first_name', first_name)
        check_user_data_and_ask_for_missing(user_id, message)

def update_last_name(message):
    if message.text=='/start' or message.text=='/help':
        bot.send_message(message.chat.id,'Ин команда аст!',)
        start(message)
    else: 
        last_name = message.text
        user_id = message.chat.id
        logging.info(f'Updating last name for user {user_id}')
        update_user_data(user_id, 'last_name', last_name)
        check_user_data_and_ask_for_missing(user_id, message)

def update_username(message):
    if message.text=='/start' or message.text=='/help':
        bot.send_message(message.chat.id,'Ин команда аст!',)
        start(message)
    else:
        username = message.text
        user_id = message.chat.id
        logging.info(f'Updating username for user {user_id}')
        update_user_data(user_id, 'username', username)
        check_user_data_and_ask_for_missing(user_id, message)
##########################----------------------------------------------------------------------------------------------##########################


#Giriftani Soli tavalud az chat      
def get_date_of_birth(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, 'Санаи тавалудатонро дохил кунед бо чунин формат: (YYYY-MM-DD) 😊')
    bot.register_next_step_handler(msg, update_date_of_birth)   
   
def update_date_of_birth(message):
    if message.text=='/start' or message.text=='/help':
        bot.send_message(message.chat.id,'Ин команда аст!',)
        start(message)
    else:
        date_of_birth = message.text
        user_id = message.chat.id
        update_user_data(user_id, 'date_of_birth', date_of_birth)
        check_user_data_and_ask_for_missing(user_id, message)
##########################----------------------------------------------------------------------------------------------##########################


#Giriftani suroga az chat
def get_address(message):
    msg = bot.send_message(message.chat.id, 'Суроғаатонро ворид кунед 😊')
    bot.register_next_step_handler(msg, process_address)

def process_address(message):
    address = message.text
    user_id = message.chat.id
    if address.startswith('/') or address.strip() == "":
        bot.send_message(user_id, 'Ин команда  дуруст нест. Лутфан, суроғаатонро ворид кунед 😊')
        get_address(message)
    else:
        logging.info(f'Updating address for user {user_id}')
        update_user_data(user_id, 'address', address)
        check_user_data_and_ask_for_missing(user_id, message)

def update_address(message):
    if message.text in ['/start', '/help']:
        bot.send_message(message.chat.id, 'Ин команда аст!')
        start(message)
    else:
        process_address(message)
##########################----------------------------------------------------------------------------------------------##########################

 
#Girihtani raqami telefon az chat
def get_phone_number(message):
    msg = bot.send_message(message.chat.id, 'Рақами телефонатонро ворид кунед 😊')
    bot.register_next_step_handler(msg, process_phone_number)

def process_phone_number(message):
    phone_number = message.text
    user_id = message.chat.id

    if phone_number.startswith('/') or phone_number.strip() == "":
        bot.send_message(user_id, 'Ин команда ё рақами телефон дуруст нест. Лутфан, рақами телефонатонро ворид кунед 😊')
        get_phone_number(message)  
    else:
        logging.info(f'Updating phone number for user {user_id}')
        update_user_data(user_id, 'phone_number', phone_number)
        check_user_data_and_ask_for_missing(user_id, message)

def update_phone_number(message):
    if message.text in ['/start', '/help']:
        bot.send_message(message.chat.id, 'Ин команда аст!')
        start(message)
    else:
        process_phone_number(message)
##########################----------------------------------------------------------------------------------------------##########################
    
        
#Giriftani Email az chat
def get_email(message):
    msg = bot.send_message(message.chat.id, 'Почтаи электронӣ ворид кунед 😊')
    bot.register_next_step_handler(msg, process_email)

def process_email(message):
    email = message.text
    user_id = message.chat.id

    if email.startswith('/') or email.lower() in ['/start', '/help']:
        bot.send_message(user_id, 'Ин команда аст!')
        start(message)
    else:
        logging.info(f'Updating email for user {user_id}')
        update_user_data(user_id, 'email', email)
        check_user_data_and_ask_for_missing(user_id, message)

def update_email(message):
    if message.text in ['/start', '/help']:
        bot.send_message(message.chat.id, 'Ин команда аст!')
        start(message)
    else:
        process_email(message)
##########################----------------------------------------------------------------------------------------------##########################
 
def check_user_data_and_ask_for_missing(user_id, message):
    user_data = check_user_data(user_id)
    
    if not user_data[1]:
        msg = bot.send_message(user_id, 'Наматонро дохил кунед 😊')
        bot.register_next_step_handler(msg, update_first_name)
    elif not user_data[2]:
        msg = bot.send_message(user_id, 'Насабатонро дохил кунед 😊')
        bot.register_next_step_handler(msg, update_last_name)
    elif not user_data[3]:
        msg = bot.send_message(user_id, 'Telegram акаунти худро дохил кунед 😊')
        bot.register_next_step_handler(msg, update_username)
    elif not user_data[4]:
        get_group_name(message)
    elif not user_data[5]:
        msg = bot.send_message(user_id, 'Суроғаатонро ворид кунед 😊')
        bot.register_next_step_handler(msg, update_address)
    elif not user_data[6]:
        msg = bot.send_message(user_id, 'Рақами телефонро дохил кунед 😊')
        bot.register_next_step_handler(msg, update_phone_number)  
    elif not user_data[7]:
        msg = bot.send_message(user_id, 'Почтаи электронӣ худро дохил кунед (***@gmail.com) агар надошта бошед надорам нависед 😊')
        bot.register_next_step_handler(msg, update_email)
    elif not user_data[8]:
        msg = bot.send_message(user_id, 'Санаи тавалудатонро дохил кунед бо ин тарз: (YYYY-MM-DD) 😊')
        bot.register_next_step_handler(msg, update_date_of_birth)
    else:
        bot.send_message(message.chat.id, 'Шумо бо мувафақият ба қайд гирифта шудед.')
        send_message_bot(user_id)


#Giriftani vaqti omadan
def check_time_to_come(user_id):
    conn = connection_database()
    cur = conn.cursor()
    try:
        today = date.today()
        cur.execute("""
            SELECT time_to_come, time_to_go FROM api_comeandwent
            WHERE user_id = %s AND date = %s
        """, (str(user_id), today))
        result = cur.fetchone()
        return result
    except Exception as e: 
        print(f'Error: {str(e)}')
        return None
    finally:
        close_connection(conn, cur)

def add_time_to_come(user_id):
    conn = connection_database()
    cur = conn.cursor()
    try:
        existing_times = check_time_to_come(user_id)
        if existing_times:
            time_to_come, time_to_go = existing_times
            if time_to_go:
                bot.send_message(user_id, 'Ту алакай рафтаии!')
            else:
                bot.send_message(user_id, f'Вақти омадани шумо илова карда шуда буд:  Мехоҳед таъғир диҳед?')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                btn_ha = types.KeyboardButton('Ҳа')
                btn_ne = types.KeyboardButton('Не')
                markup.add(btn_ha, btn_ne)
                bot.send_message(user_id, 'Тасдиқ кунед Ҳа ё Не:', reply_markup=markup)
                bot.register_next_step_handler_by_chat_id(user_id, update_arrival)
        else:
            now = datetime.now()
            time_to_come = now.strftime('%Y-%m-%d %H:%M')
            cur.execute("""
                INSERT INTO api_comeandwent(user_id, time_to_come, date) VALUES
                (%s, %s, %s)""", (str(user_id), time_to_come, now.date())) 
            conn.commit()
            bot.send_message(user_id, f'Вақти омадан шумо илова карда шуд: {time_to_come}') 
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        close_connection(conn, cur)

def update_arrival(message): 
    user_id = message.chat.id
    if message.text == 'Ҳа':
        time_to_come = datetime.now().strftime('%Y-%m-%d %H:%M')
        conn = connection_database()
        cur = conn.cursor()
        try:    
            cur.execute("""
                UPDATE api_comeandwent SET time_to_come = %s WHERE user_id = %s AND date = %s
            """, (time_to_come, str(user_id), date.today()))
            conn.commit()
            bot.send_message(user_id, f'Вақти омадани шумо иваз карда шуд: {time_to_come}') 
            send_message_bot(message.chat.id)
        except Exception as e:
            print(f'Error: {str(e)}')
        finally:
            close_connection(conn, cur)
    elif message.text == 'Не':
        bot.send_message(user_id, 'Ташаккур! Мо вақтатонро иваз намекунем.')
        send_message_bot(message.chat.id)


#Giriftani vaqti raftan
def check_time_to_go(user_id):
    conn = connection_database()
    cur = conn.cursor()
    try:
        today = date.today()
        cur.execute("""
            SELECT time_to_go FROM api_comeandwent
            WHERE user_id = %s AND date = %s
        """, (str(user_id), today))
        result = cur.fetchone()
        return result
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    finally:
        close_connection(conn, cur)

def add_time_to_go(user_id):
    existing_time = check_time_to_go(user_id)
    arrival_time = check_time_to_come(user_id)
    today = datetime.now().date()

    if not arrival_time or arrival_time[0] is None:
        bot.send_message(user_id, 'Шумо ҳоло омадаги нестед куҷо меравед')
        return

    if existing_time:
        if existing_time[0] is not None and existing_time[0].date() == today:
            bot.send_message(user_id, 'Шумо метавонед вақти рафтанро танҳо як маротиба дар як рӯз ворид кунед.')
        else:
            try:
                conn = connection_database()
                cur = conn.cursor()
                time_to_go = datetime.now().strftime('%Y-%m-%d %H:%M')
                cur.execute("""
                   UPDATE api_comeandwent
                   SET time_to_go = %s
                   WHERE user_id = %s AND date = %s
                  """, (time_to_go, str(user_id), today))
                conn.commit()
                bot.send_message(user_id, f'Вақти рафтани шумо сабт шуд: {time_to_go}')
            except Exception as e:
                print(f'Error updating departure time: {str(e)}')
            finally:
                close_connection(conn, cur)
    else:
        try:
            conn = connection_database()
            cur = conn.cursor()
            time_to_go = datetime.now().strftime('%Y-%m-%d %H:%M')
            cur.execute("""
               INSERT INTO api_comeandwent (user_id, time_to_go, date)
               VALUES (%s, %s, %s)
              """, (str(user_id), time_to_go, today))
            conn.commit()
            bot.send_message(user_id, f'Вақти рафтани шумо сабт шуд: {time_to_go}')
        except Exception as e:
            print(f'Error adding departure time: {str(e)}')
        finally:
            close_connection(conn, cur)
##########################----------------------------------------------------------------------------------------------##########################


#Giriftani Feedback
def add_feedback(user_id, feedback_text):
    conn = connection_database()
    if conn:
        cur = conn.cursor()
        try:
            date = datetime.now().strftime('%Y-%m-%d %H:%M')
            cur.execute("""
                INSERT INTO api_feedback (user_id, submission_time, feedback_text) VALUES (%s, %s, %s)
            """, (str(user_id), date, feedback_text))
            conn.commit()
        except Exception as e:
            print(f'Error: {str(e)}')
        finally:
            close_connection(conn, cur)
            
def ask_for_feedback(user_id):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Ба қафо')
    markup.add(back_button)
    
    msg = bot.send_message(user_id, "Лутфан, Фикру андешаатонро нисбат ба барнома нависед 😊:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_feedback)

def process_feedback(message):
    user_id = message.chat.id
    feedback_text = message.text

    if feedback_text.lower() == 'ба қафо':  
        bot.send_message(user_id, "Шумо ба менюи асосӣ баргаштед.", reply_markup=types.ReplyKeyboardRemove())
        send_message_bot(user_id) 
        return

    add_feedback(user_id, feedback_text)
    bot.send_message(user_id, "Ташаккур барои Фикру андешаҳо нисбат ба барнома 🙏!")
    send_message_bot(user_id) 
##########################----------------------------------------------------------------------------------------------##########################


#giriftani sababi der kardan ba dars 
def ask_the_reason_for_the_delay(user_id):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Ба қафо') 
    markup.add(back_button)
    bot.send_message(user_id, 'Сабаби деркарданатонро мегуфтед? 🤨', reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(user_id, the_reason_for_being_late)

def the_reason_for_being_late(message):
    user_id = message.chat.id
    reason = message.text
    
    if reason.lower() == 'ба қафо': 
        bot.send_message(user_id, "Шумо ба менюи асосӣ баргаштед.", reply_markup=types.ReplyKeyboardRemove())
        send_message_bot(user_id) 
        return
    
    if check_time_to_come_empty(user_id):
        bot.send_message(user_id, "Ман сабаби дер карданатонро ба муаллиматон фиристодам. Онкас камтар пас ба шумо ҷавоб хоҳанд дод!")
        reason_to_teachers(user_id, reason)
        record_late_reason(user_id, reason)
        send_message_bot(message.chat.id)
    else:
        bot.send_message(user_id, "Шумо имрӯз омадаед, чихел дер мекунед.")
        send_message_bot(user_id)

def check_time_to_come_empty(user_id):
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute("SELECT time_to_come FROM api_comeandwent WHERE user_id = %s AND date = CURRENT_DATE", (str(user_id),))
        time_to_come = cur.fetchone()
        if time_to_come and time_to_come[0] is not None:
            return False
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        close_connection(conn, cur)

def reason_to_teachers(user_id, reason):
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute("SELECT first_name, last_name, username, group_name FROM api_customeruser WHERE user_id = %s", (str(user_id),))
        user_info = cur.fetchone()
        if user_info:
            first_name, last_name, username, group_name = user_info
            message_to_teachers = f"""
Донишҷӯ --> {first_name.upper()} {last_name.upper()}
Аз гурӯҳи --> {group_name.upper()}
Телеграм акаунт --> @{username}

Сабаби дер карданаш:
{reason}
"""
            escaped_message = message_to_teachers.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")
            response = requests.post(
                f"https://api.telegram.org/bot{TEACHER_BOT_TOKEN}/sendMessage",
                params={
                    'chat_id': TEACHER_CHAT_ID,
                    'text': escaped_message,
                    'parse_mode': 'HTML'  
                }
            )
            if response.status_code == 200:
                print("Message sent successfully")
            else:
                print(f"Failed to send message. Status code: {response.status_code}")
                print(response.text)
        else:
            print(f"User information not found for user_id: {user_id}")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        close_connection(conn, cur)

def record_late_reason(user_id, reason):
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM api_comeandwent WHERE user_id = %s AND date = CURRENT_DATE", (str(user_id),))
        cw_id = cur.fetchone()

        if cw_id:
            cur.execute("UPDATE api_comeandwent SET late_reason = %s WHERE id = %s", (reason, cw_id[0]))
        else:
            cur.execute("INSERT INTO api_comeandwent (user_id, late_reason, date) VALUES (%s, %s, CURRENT_DATE)", (str(user_id), reason))
        
        conn.commit()
        print("Late reason recorded successfully")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        close_connection(conn, cur)
##########################----------------------------------------------------------------------------------------------##########################


#Giriftani sababi naomadan
def ask_for_absence_reason(user_id):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Ба қафо')
    markup.add(back_button)
    bot.send_message(user_id, "Ба дарс наомадан оқибатҳои нохуб дорад. Лутфан, сабаби наомаданатонро гӯед.", reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(user_id, process_absence_reason)

def process_absence_reason(message):
    user_id = message.chat.id
    reason = message.text
    if reason.lower() == 'ба қафо':  
        bot.send_message(user_id, "Шумо ба менюи асосӣ баргаштед.", reply_markup=types.ReplyKeyboardRemove())
        send_message_bot(user_id) 
        return

    if check_time_to_come_empty(user_id):
        bot.send_message(user_id, "Ман сабаби наомаданатонро ба муаллиматон фиристодам. Онкас каме дертар ба шумо ҷавоб хоҳанд дод.")
        send_reason_to_teachers(user_id, reason)
        record_absence_reason(user_id, reason)
        send_message_bot(message.chat.id)

    else:
        bot.send_message(user_id, "Шумо имрӯз омадаед, чихел омада наметавонед.")
        send_message_bot(user_id) 

def send_reason_to_teachers(user_id, reason):
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute("SELECT first_name, last_name, username, group_name FROM api_customeruser WHERE user_id = %s", (str(user_id),))
        user_info = cur.fetchone()
        if user_info:
            first_name, last_name, username, group_name = user_info
            message_to_teachers = f"""
Донишҷӯ --> {first_name} {last_name}
Аз гурӯҳи --> {group_name}
Телеграм акаунт --> @{username}

Сабаби наомаданаш:
{reason}
"""
            escaped_message = message_to_teachers.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")
            response = requests.post(
                f"https://api.telegram.org/bot{TEACHER_BOT_TOKEN}/sendMessage",
                params={
                    'chat_id': TEACHER_CHAT_ID,
                    'text': escaped_message,
                    'parse_mode': 'HTML'
                }
            )
            if response.status_code == 200:
                print("Message sent successfully")
            else:
                print(f"Failed to send message. Status code: {response.status_code}")
                print(response.text)
        else:
            print(f"User information not found for user_id: {user_id}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        close_connection(conn, cur)

def record_absence_reason(user_id, reason):
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM api_comeandwent WHERE user_id = %s AND date = CURRENT_DATE", (str(user_id),))
        cw_id = cur.fetchone()

        if cw_id:
            cur.execute("UPDATE api_comeandwent SET absent_reason = %s WHERE id = %s", (reason, cw_id[0]))
        else:
            cur.execute("INSERT INTO api_comeandwent (user_id, absent_reason, date) VALUES (%s, %s, CURRENT_DATE)", (str(user_id), reason))
        
        conn.commit()
        print("Absence reason recorded successfully")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        close_connection(conn, cur)
##########################----------------------------------------------------------------------------------------------##########################


#Comandai Start
@bot.message_handler(commands=['start'])
def start(message):
   
    user_id = message.chat.id
    user_data = check_user_data(user_id)
    if user_data:
        if not user_data[1]:
            msg = bot.send_message(user_id, 'Наматонро дохил кунед 😊')
            bot.register_next_step_handler(msg, update_first_name)
        elif not user_data[2]:
            msg = bot.send_message(user_id, 'Насабатонро дохил кунед 😊')
            bot.register_next_step_handler(msg, update_last_name)
        elif not user_data[3]:
            msg = bot.send_message(user_id, 'Telegram акаунти худро дохил кунед 😊')
            bot.register_next_step_handler(msg, update_username)
        elif not user_data[4]:
            get_group_name(message)
        elif not user_data[5]:
            get_address(message)
        elif not user_data[6]:
            get_phone_number(message)
        elif not user_data[7]:
            get_email(message)
        elif not user_data[8]:
            get_date_of_birth(message)
        else:
            send_message_bot(user_id)
    else:
        first_name = message.chat.first_name or ''
        last_name = message.chat.last_name or ''
        username = message.chat.username or ''
        registration_date = datetime.now().strftime('%Y-%m-%d %H:%M')
                
        add_user_in_table(user_id, first_name, last_name, username,registration_date)

        if not first_name:
            msg = bot.send_message(user_id, 'Наматонро дохил кунед 😊')
            bot.register_next_step_handler(msg, update_first_name)
        elif not last_name:
            msg = bot.send_message(user_id, 'Насабатонро дохил кунед 😊')
            bot.register_next_step_handler(msg, update_last_name)
        elif not username:
            msg = bot.send_message(user_id, 'Telegram акаунти худро дохил кунед 😊')
            bot.register_next_step_handler(msg, update_username)
        else:
            get_group_name(message)
##########################----------------------------------------------------------------------------------------------##########################


#Comandai help
@bot.message_handler(commands=['help'])
def helping(message):
    bot.send_message(message.chat.id, f"""
    Ин бот барои ҳасту нест кардани студентоҳои SoftClub мебошад.
    
    1.Барои истифjда бурдани бот аз қисмати меню /start -
    ро пахш намоед то ки ботро истифода бурда тавонед.
    Пас аз пахш кардани /start агар ном ё насаб ё ин ки 
    номи корбаратон холи бошад пас аз шумо ҳамон набудаашро
    мепурсад шумо бошад онро дар чат нависед. Пасон дар поён 
    тугмаҳо пайдо мешаванд тугмаҳо инҳоянд "(Ман омадам, 
    Ман рафтам, Ҷавоб мегирам ва баҳо додан)".
    2.Бо пахш кардани тугмаи "Ман омадам" шуморо дар журнал
    қайд мекунад ки ба дарс омадед инчунини соати омадаатонро
    низ қайд мекунад.Агар шумо дар тули руз ин корро чанд бор
    такрор кунед ҳар бор аз шумо мепурсад вақти омадаатонро 
    иваз кардан мехоҳед ТУгмаи ҲА ва НЕ мебарояд ва яке аз 
    инро пахш кунед.
    3.Бо пахш кардани тугмаи "Ман рафтам" вақти рафтаи шумо
    сабт карда мешавад ва дуюм маротиба шумо ин корро анҷом
    дода наметавонед чун вақти рафтан як бор сабт мешавад.
    4.Бо пахши тугмаи "Ҷавоб мегирам" Аз шумо сабаби ҷавоб 
    пурсиданатонро мепурсад ва ҷавоби навистаатонро ба 
    устодатон равон мекунад ва устодатон ба шумо занг мезанад.
    5.Бо пахши тугмаи "Баҳо додан" ягон арзу шикоят бошад ё ин
    ки ягон чи гуфтани бтошед нависед!""")
##########################----------------------------------------------------------------------------------------------##########################


#Comandai nishon dodani tugmaho
@bot.message_handler(commands=['buttons']) 
def buttons(message):
    send_message_bot(message.chat.id)
##########################----------------------------------------------------------------------------------------------##########################


#Giriftani nomi guruh
def get_group_name(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btns = ['Cpp', 'HTML & CSS', 'Dart', 'Python', 'C Sharp', ' Dot NET', 'J.Script', 'J.Script 2', 'React', 'React 2', 'UХ/UI', 'Cpp Olimpiad', 'Django', 'Graphic design', 'Дигар']
    buttons = [KeyboardButton(btn) for btn in btns]
    markup.add(*buttons)
    msg = bot.send_message(message.chat.id, 'Номи гурӯҳатонро аз инҷо интихоб кунед ё ки ворид кунед 😊', reply_markup=markup)
    bot.register_next_step_handler(msg, process_group_choice)

def process_group_choice(message):
    group_name = message.text
    if group_name == 'Дигар':
        msg = bot.send_message(message.chat.id, 'Номи гурӯҳатонро дохил кунед 😊')
        bot.register_next_step_handler(msg, process_custom_group_name)
    else:
        user_id = message.chat.id
        logging.info(f'Updating group name for user {user_id} to {group_name}')
        update_user_data(user_id, 'group_name', group_name)
        check_user_data_and_ask_for_missing(user_id, message)

def process_custom_group_name(message):
    group_name = message.text
    user_id = message.chat.id
    logging.info(f'Updating custom group name for user {user_id} to {group_name}')
    update_user_data(user_id, 'group_name', group_name)
    check_user_data_and_ask_for_missing(user_id, message)
##########################----------------------------------------------------------------------------------------------##########################


#Ivaz kardani nomi guruh
def update_user_group(user_id, new_group_name):
    conn = connection_database()
    cur = conn.cursor()
    try:
        user_id_str = str(user_id)

        cur.execute("""
            SELECT first_name, last_name, username, phone_number, email, date_of_birth, address, group_name
            FROM api_customeruser
            WHERE user_id = %s
        """, (user_id_str,))
        existing_user = cur.fetchone()

        if not existing_user:
            print(f"No existing user found with user_id: {user_id_str}")
            return

        first_name, last_name, username, phone_number, email, date_of_birth, address, last_group_name = existing_user

        cur.execute("""
            SELECT COUNT(*)
            FROM api_customeruser
            WHERE user_id LIKE %s
        """, (f"{user_id_str}_%",))
        count = cur.fetchone()[0]

        previous_user_id = f"{user_id_str}_{count + 2}"

        cur.execute("""
            UPDATE api_customeruser
            SET is_active = FALSE,
                user_id = %s,
                group_name = %s
            WHERE user_id = %s
        """, (previous_user_id, last_group_name, user_id_str))
        
        
        cur.execute("""
            UPDATE api_comeandwent
            SET user_id = %s
            WHERE user_id = %s
        """, (previous_user_id, user_id_str))
        
       
        cur.execute("""
            UPDATE api_feedback
            SET user_id = %s
            WHERE user_id = %s
        """, (previous_user_id, user_id_str))
        

        cur.execute("""
            INSERT INTO api_customeruser (
                user_id, group_name, registration_date, is_active, first_name, last_name, username, phone_number, email, date_of_birth, address
            )
            VALUES (%s, %s, %s, TRUE, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id_str, new_group_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
            first_name, last_name, username, phone_number, email, date_of_birth, address
        ))
        conn.commit()
        print(f"Group name for user {user_id_str} updated to {new_group_name}")
        bot.send_message(user_id, f"Your previous group was '{last_group_name}'. We have moved you to group '{new_group_name}'.")
        
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        close_connection(conn, cur)

def is_user_registered(user_id):
    conn = connection_database()
    cur = conn.cursor()
    try:
        user_id_str = str(user_id)
        cur.execute("SELECT * FROM api_customeruser WHERE user_id = %s", (user_id_str,))
        user = cur.fetchone()
        return user is not None
    except Exception as e:
        print(f'Error: {str(e)}')
        return False
    finally:
        close_connection(conn, cur)

@bot.message_handler(commands=['switch_to_a_new_group'])
def switch_to_a_new_group(message):
    user_id = message.chat.id
    if not is_user_registered(user_id):
        bot.send_message(user_id, 'Шумо ҳоло ба қайд гирифта нашудаед. Лутфан фармони /start -ро истифода баред.')
        return

    markup = types.InlineKeyboardMarkup()
    ha_btn = types.InlineKeyboardButton('Ҳа', callback_data='switch_ha')
    ne_btn = types.InlineKeyboardButton('Не', callback_data='switch_ne')
    markup.add(ha_btn, ne_btn)
    confirmation_message = bot.send_message(user_id, "Ин фармон барои гузариш ба гуруҳи нав аст. Шумо мутмаин ҳастед, ки ба гуруҳи дигар мегузаред? Агар ҳа, пас тугмаи 'Ҳа' - ро пахш кунед, агар не, пас тугмаи 'Не' - ро пахш кунед.", reply_markup=markup)
    selection_message = bot.send_message(user_id, "Якеро интихоб кунед.", reply_markup=types.ReplyKeyboardRemove())

    user_states[user_id] = {
        'confirmation_message_id': confirmation_message.message_id,
        'selection_message_id': selection_message.message_id
    }

user_states = {}

@bot.callback_query_handler(func=lambda call: call.data in ['switch_ha', 'switch_ne'])
def handle_switch_response(call):
    user_id = call.from_user.id
    state = user_states.get(user_id, {})
    confirmation_message_id = state.get('confirmation_message_id')
    selection_message_id = state.get('selection_message_id')

    if confirmation_message_id:
        try:
            bot.delete_message(call.message.chat.id, confirmation_message_id)
        except Exception as e:
            print(f"Failed to delete confirmation message: {e}")

    if selection_message_id:
        try:
            bot.delete_message(call.message.chat.id, selection_message_id)
        except Exception as e:
            print(f"Failed to delete selection message: {e}")

    if call.data == 'switch_ha':
        if not is_user_registered(user_id):
            bot.send_message(user_id, 'Шумо ҳоло ба қайд гирифта нашудаед. Лутфан фармони /start -ро истифода баред.')
            return
        get_group_name(call.message)
        bot.register_next_step_handler(call.message, process_new_group_name)
    elif call.data == 'switch_ne':
        bot.send_message(user_id, "Гузариш ба гуруҳи нав бекор карда шуд.")
        send_message_bot(user_id)

    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    except Exception as e:
        print(f"Failed to remove inline keyboard: {e}")

def process_new_group_name(message):
    user_id = message.from_user.id
    new_group_name = message.text
    if not new_group_name:
        bot.send_message(user_id, "Гурӯҳи нав наомад. Лутфан дубора кӯшиш кунед.")
        return
    update_user_group(user_id, new_group_name)
    bot.send_message(user_id, f"Шуморо ба гурӯҳи\n'{new_group_name}' гузаронидем.")
##########################----------------------------------------------------------------------------------------------##########################


#Tugmaho
def send_message_bot(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton('Ман омадам ')
    btn2 = types.KeyboardButton('Ман рафтам')
    btn3 = types.KeyboardButton('Дер мекунам')
    btn4 = types.KeyboardButton('Ҷавоб мегирам')
    btn5 = types.KeyboardButton('Фикру андешаҳо нисбат ба барнома')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(user_id, 'Якеро интихоб кунед.', reply_markup=markup)
##########################----------------------------------------------------------------------------------------------##########################


@bot.message_handler()
def handler(message):
    if message.text == 'Ман омадам':
        add_time_to_come(message.chat.id)
    elif message.text == 'Ман рафтам':
        add_time_to_go(message.chat.id)
    elif message.text == 'Дер мекунам':
        ask_the_reason_for_the_delay(message.chat.id)
    elif message.text == 'Ҷавоб мегирам':
        ask_for_absence_reason(message.chat.id)
    elif message.text == 'Фикру андешаҳо нисбат ба барнома':
        ask_for_feedback(message.chat.id) 


if __name__ == "__main__":
    bot.polling(none_stop=True)

