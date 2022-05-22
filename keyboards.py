from gettext import Catalog
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from functions import get_next_part_id, get_last_id_for_categ, get_prev_part_id
from catalog import CPUs, MBs, VCs, RAMs, PSs
import catalog

class Buttons():
    def __init__(self):
        # Main menu 
        self.btn_catalog = KeyboardButton("💰 Каталог")
        self.btn_favourite = KeyboardButton("⭐️ Избранное")
        self.btn_cart = KeyboardButton("🛒 Корзина")
        self.btn_settings = KeyboardButton("⚙️ Настройки")
        #
        # Settings
        self.btn_edit_addr = KeyboardButton("Изменить данные доставки")
        self.btn_history = KeyboardButton("История заказов")
        self.btn_help = KeyboardButton("Обратная связь")
        self.btn_backmenu = KeyboardButton("Главное меню")
        # Categories Inline
        self.p1 = InlineKeyboardButton("Процессоры", callback_data='c1')
        self.p2 = InlineKeyboardButton("Материнские платы", callback_data='c2')
        self.p3 = InlineKeyboardButton("Видеокарты", callback_data='c3')
        self.p4 = InlineKeyboardButton("Оперативная память", callback_data='c4')
        self.p5 = InlineKeyboardButton("Блоки питания", callback_data='c5')
        self.p6 = InlineKeyboardButton("Корпуса", callback_data='c6')
        self.p7 = InlineKeyboardButton("Охлаждение", callback_data='c7')
        self.p8 = InlineKeyboardButton("SSD накопители", callback_data='c8')
        self.p9 = InlineKeyboardButton("Жесткие диски", callback_data='c9')
        #
        # Item Inline
        self.add_to_cart = InlineKeyboardButton("🛒 Добавить в корзину", callback_data="add_")
        self.next = InlineKeyboardButton("Далее ➡️", callback_data="next_")
        self.prev = InlineKeyboardButton("⬅️ Назад", callback_data="prev_")
        self.del_from_cart = InlineKeyboardButton("Убрать из корзины", callback_data="del_")
        self.add_fav = InlineKeyboardButton("В избранное ⭐️", callback_data="fav_")
        # 
        
        self.clear_cart = InlineKeyboardButton("❌ Очистить", callback_data="clr_cart")
        self.clear_fav = InlineKeyboardButton("❌ Очистить", callback_data="clr_fav")
        self.add_cart_from_fav = InlineKeyboardButton("В корзину 🛒", callback_data="tocartfromfav_")
        self.buy = InlineKeyboardButton("💳 Оформить заказ", callback_data="buy_")
        self.promo = InlineKeyboardButton("⚡️ Промокод", callback_data="enter_promo")
        self.cancel_action = InlineKeyboardButton("Отменить", callback_data="cancel_act")
        self.check_order = InlineKeyboardButton("Проверить оплату", callback_data="check_order_")
        self.order_buy = InlineKeyboardButton("💳 Оплатить", url="yoomoney.ru")
        

class Keyboard_():
    def __init__(self):
        self.BTNS = Buttons()
        self.empty_ = ReplyKeyboardRemove()
        self.mainmenu = ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
        self.settings = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
        self.categories = InlineKeyboardMarkup(row_width=1, inline_keyboard=True)
        self.item = InlineKeyboardMarkup(row_width=3, inline_keyboard=True)
        self.cart = InlineKeyboardMarkup(row_width=2, inline_keyboard=True)
        self.fav = InlineKeyboardMarkup(inline_keyboard=True)
        self.enter_prom = InlineKeyboardMarkup(inline_keyboard=True)
        self.check_ord = InlineKeyboardMarkup(inline_keyboard=True)
        
        self.fav.add(self.BTNS.add_cart_from_fav, self.BTNS.clear_fav)
        self.categories.add(self.BTNS.p1, self.BTNS.p2,self.BTNS.p3,self.BTNS.p4,self.BTNS.p5)
        self.mainmenu.row(self.BTNS.btn_catalog, self.BTNS.btn_cart, self.BTNS.btn_favourite).add(self.BTNS.btn_settings)
        self.cart.row(self.BTNS.buy, self.BTNS.promo).row(self.BTNS.clear_cart)
        self.settings.add(self.BTNS.btn_edit_addr, self.BTNS.btn_history, self.BTNS.btn_help, self.BTNS.btn_backmenu)
        self.enter_prom.add(self.BTNS.cancel_action)
    
    def generate_cart_callback(self, user_id):
        self.BTNS.add_cart_from_fav = InlineKeyboardButton("В корзину 🛒", callback_data=f"tocartfromfav_{user_id}")
    def generate_order(self, key, url):
        self.BTNS.check_order = InlineKeyboardButton("Проверить оплату", callback_data=f"check_order_{key}")
        self.BTNS.order_buy = InlineKeyboardButton(text = f"💳 Оплатить", url=f"{url}")
        self.check_ord.add(self.BTNS.order_buy, self.BTNS.check_order)    
    
    def generate_item(self, cat_id, part_id):
        if cat_id == 1:
            parts_dict = CPUs
        if cat_id == 2:
            parts_dict = MBs
        if cat_id == 3:
            parts_dict = VCs
        if cat_id == 4:
            parts_dict = RAMs
        if cat_id == 5:
            parts_dict = PSs
            
        catg_ = catalog.categ_names[cat_id]
          
        if part_id == get_last_id_for_categ(parts_dict):
            next_part_id = 0
        else:
            next_part_id = get_next_part_id(part_id, parts_dict)
        if part_id == catalog.id_first_cpu:
            prev_part_id = 0
        else:
            prev_part_id = get_prev_part_id(part_id, parts_dict)
            
            
        self.item = InlineKeyboardMarkup(row_width=3, inline_keyboard=True)
        self.BTNS.add_to_cart = InlineKeyboardButton("➕ Добавить в корзину", callback_data=f"add_{catg_}_{part_id}")
        self.BTNS.next = InlineKeyboardButton("Далее ➡️", callback_data=f"next_{catg_}_{next_part_id}")
        self.BTNS.prev = InlineKeyboardButton("⬅️ Назад", callback_data=f"prev_{catg_}_{prev_part_id}")
        self.BTNS.del_from_cart = InlineKeyboardButton("➖ Убрать из корзины", callback_data=f"del_{catg_}_{part_id}")
        self.BTNS.add_fav = InlineKeyboardButton("В избранное ⭐️", callback_data=f"fav_{cat_id}_{part_id}")
        self.item.row(self.BTNS.add_to_cart).row(self.BTNS.add_fav).row(self.BTNS.del_from_cart).add(self.BTNS.prev, self.BTNS.next)
            
        
    
nav = Keyboard_()  
