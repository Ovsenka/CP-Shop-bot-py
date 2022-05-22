import sqlite3
import catalog
import functions
import datetime



class Database():
    def __init__(self, path_to_db):
        try:
            print("Подключение к базе данных...")
            self.connection = sqlite3.connect(path_to_db)
            self.cursor = self.connection.cursor()
            print("База данных успешно подключена!")
        except Exception as err:
            print("Ошибка при подключении! \n", err)
    def promo_apply(self, user_id, promo, discount):
        with self.connection:
            self.cursor.execute("UPDATE users SET promo = ?, discount = ? WHERE user_id = ?", (promo, discount, user_id,))
            return 0
    def get_user(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT promo, discount FROM users WHERE user_id = ?", (user_id,))
            user = self.cursor.fetchone()
            print(user)
            return user
            
    def user_register(self, user_id):
        with self.connection:
            with self.connection:
                self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
                print("Register user ", user_id)
    
    def get_all_parts(self):
        with self.connection:
            try:
                print("Извлечение каталога из базы данных...")
                self.cursor.execute("SELECT * FROM catalog")
                parts = self.cursor.fetchall()
                print("*"*45)
                print(f"Всего комплектующих:  {len(parts)}")
                return parts
            except Exception as err:
                print("Ошибка при извлечении! \n", err)
    def get_sum_order_from_cart(self, user_id):
        with self.connection:
            print("GET SUM ID = ", user_id)
            self.cursor.execute("SELECT part_id, count FROM cart WHERE user_id = ?", (user_id,))
            cart = self.cursor.fetchall()
            price = functions.get_all_cost(cart)
            if self.promo_is_active(user_id):
                percent = self.get_discount_promo(user_id)
                price_a = price * (100 - percent) / 100
            return price_a
    def promo_is_active(self, user_id) -> bool:
        with self.connection:
            self.cursor.execute("SELECT discount FROM users WHERE user_id = ?", (user_id,))
            if self.cursor.fetchone()[0] != 0:
                return True
            return False
    def get_discount_promo(self, user_id) -> int:
        with self.connection:
            self.cursor.execute("SELECT discount FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()[0]
            return result
    def get_promo_user(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT promo FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()[0]
            return result    
    def get_text_user_cart(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT part_id, count FROM cart WHERE user_id = ?", (user_id,))
            cart = self.cursor.fetchall()
            price = functions.get_all_cost(cart)
            text = "Позиция" + "       |       " + "Количество" + "\n"
            for item in cart:
                p_id = item[0]
                c = item[1]
                if p_id in catalog.CPUs:
                    name = catalog.CPUs[p_id][0]
                if p_id in catalog.MBs:
                    name = catalog.MBs[p_id][0]
                if p_id in catalog.VCs:
                    name = catalog.VCs[p_id][0]
                if p_id in catalog.RAMs:
                    name = catalog.RAMs[p_id][0]
                if p_id in catalog.PSs:
                    name = catalog.PSs[p_id][0]
                
                text += f"{name} - {c} шт.\n"
            
            text += "-"*20 + f" Итого: {price} ₽\n"
            print("ACTIVE PROMO: ", self.promo_is_active(user_id))
            if self.promo_is_active(user_id):
                print("GET DISCOUNT ACTIVE: ", self.get_discount_promo(user_id))
                percent = self.get_discount_promo(user_id)
                price_a = price * (100 - percent) / 100
                text += "-"*20 + f" Итого со скидкой: {price_a} ₽ (скидка {percent}%)"
            return text
    def get_count_of_part_from_cart(self, user_id, p_id):
        with self.connection:
            self.cursor.execute("SELECT count FROM cart WHERE user_id = ? AND part_id = ?", (user_id, p_id,))
            c = self.cursor.fetchall()
            print(c)
            if len(c) == 0:
                return 0
            else:
                return c[0][0]
    def add_to_cart(self, user_id, part_id, cat_id, count):
        with self.connection:
            try:
                user_have_count = self.get_count_of_part_from_cart(user_id, part_id)
                if user_have_count == 0:
                    self.cursor.execute("INSERT INTO cart VALUES (?, ?, ?, ?)", (user_id, part_id, cat_id, count,))
                elif user_have_count >= 1:
                    self.cursor.execute("UPDATE cart SET count = count + 1 WHERE user_id = ? AND part_id = ?", (user_id, part_id,))
                    
                print(f"{user_id} добавил в корзину {part_id} - {count} шт.")
                return 0
            except Exception as err:
                print("Ошибка добавления в корзину!", err)
                return -1
    def del_from_cart(self, user_id, part_id, count):
        with self.connection:
            try:
                self.cursor.execute("UPDATE cart SET count = count - 1 WHERE user_id = ? AND part_id = ?", (user_id, part_id,)) 
                if self.get_count_of_part_from_cart(user_id, part_id) <= 0:
                    self.cursor.execute("DELETE FROM cart WHERE user_id = ? AND part_id = ?",(user_id, part_id,))
                return 0
            except Exception as err:
                print("Ошибка удаления из корзины!", err)
                return -1
    def clear_cart(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
            return 0

    def clear_fav(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM favourite WHERE user_id = ?", (user_id,))
            return 0
    def add_to_fav(self, user_id, cat_id, part_id):
        with self.connection:
            self.cursor.execute("INSERT INTO favourite VALUES (?, ?, ?)", (user_id, part_id, cat_id,))
            return 0
    def get_user_fav(self, user_id) -> list:
        with self.connection:
            self.cursor.execute("SELECT part_id FROM favourite WHERE user_id = ?", (user_id,))
            fav = self.cursor.fetchall()
            return fav
    def get_text_user_fav(self, user_id):
        fav = self.get_user_fav(user_id)
        text = ""
        for item in fav:
            if item[0] in catalog.CPUs:
                text += catalog.CPUs[item[0]][0] + "\n"
            if item[0] in catalog.MBs:
                text += catalog.MBs[item[0]][0] + "\n"
            if item[0] in catalog.VCs:
                text += catalog.VCs[item[0]][0] + "\n"
            if item[0] in catalog.RAMs:
                text += catalog.RAMs[item[0]][0] + "\n"
            if item[0] in catalog.PSs:
                text += catalog.PSs[item[0]][0] + "\n"
        return text
        
    def to_cart(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT part_id, cat_id FROM favourite WHERE user_id = ?", (user_id,))
            parts = self.cursor.fetchall()
            for part in parts:
                print(part)
                self.add_to_cart(user_id, part[0], part[1], 1)
    
    def is_parts_in_fav(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT part_id FROM favourite WHERE user_id = ?", (user_id,))
            parts = self.cursor.fetchall()
            print(parts)
            if len(parts) == 0:
                return False
            return True
    def get_all_promo(self):
        with self.connection:
            self.cursor.execute("SELECT name, discount FROM promo")
            result = self.cursor.fetchall()
            return result
    def add_order(self, order_id, user_id):
        with self.connection:
            date = datetime.datetime.now().strftime('%H:%M:%S')
            promo = ""
            self.cursor.execute("SELECT part_id, count, cat_id FROM cart WHERE user_id = ?", (user_id,))
            cart = self.cursor.fetchall()
            price = functions.get_all_cost(cart)
            if self.promo_is_active(user_id):
                percent = self.get_discount_promo(user_id)
                price_a = price * (100 - percent) / 100
                promo = db.get_promo_user(user_id)
            else:
                promo = "NONE"
            for item in cart:
                p_id = item[0]
                c = item[1]
                cat = item[2]
                self.cursor.execute("INSERT INTO orders (order_id, client_id, part_id, category_id, count_part, price_order, status, datetime, promo) VALUES (?,?,?,?,?,?,?,?,?)",(order_id,user_id,p_id,cat,c,price_a,"success",date,promo))
    

db = Database("/home/dovsenka/Python Projects/CP Shop/db_cpshop/cpshop.db")