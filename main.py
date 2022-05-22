from bot import CPBot
from aiogram import types
from handlers import *
from keyboards import nav
import catalog
import functions
from db import db
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from StatesGrp import Form
from aiogram.dispatcher import FSMContext
from payments import YooPayment
from datetime import datetime
from config import TOKEN_API, ACCESS_TOKEN


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()    
    bot = CPBot(TOKEN_API, storage)
    client = YooPayment(ACCESS_TOKEN)
    
@bot.dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Рады видеть вас!", reply_markup=nav.mainmenu)
    print(message.chat.username, message['from'].first_name,  message['text'])
    if not db.get_user(message.chat.id):
        db.user_register(message.chat.id)

@bot.dp.message_handler()
async def msg(message: types.Message):
    if message.text == "💰 Каталог":
        await message.answer("Каталог", reply_markup=nav.categories)
    if message.text == "Главное меню":
        await message.answer("Главное меню", reply_markup=nav.mainmenu)
    if message.text == "⭐️ Избранное":
        if not db.is_parts_in_fav(message.chat.id):
            await message.answer("Ваше избранное пусто.")
        else:
            nav.generate_cart_callback(message.chat.id)
            await message.answer("Избранное: \n" + db.get_text_user_fav(message.chat.id), reply_markup=nav.fav)
    if message.text == "🛒 Корзина":
        parts_ = db.get_text_user_cart(message.from_user.id)
        await message.answer("Ваша корзина:\n" + parts_, reply_markup=nav.cart)
    if message.text == "⚙️ Настройки":
        await message.answer("Настройки\n", reply_markup=nav.settings)  
    print(message.chat.username, message['from'].first_name,  message['text'])
    
@bot.dp.message_handler(state=Form.promo)
async def process_name(message: types.Message, state: FSMContext):
    for promo in db.get_all_promo():
        if promo[0] == message.text:
            await state.finish()
            discount = promo[1]
            if db.promo_apply(message.chat.id, promo[0], discount) == 0:
                await message.answer("Промокод активирован!")   

@bot.dp.callback_query_handler(lambda c: c.data == "buy_")
async def order(callback_query: types.CallbackQuery):
    await bot.CPbot.answer_callback_query(callback_query.id, text="Оплата заказа..", show_alert=False)
    user_id = callback_query.message.chat.id
    key = functions.generate_key_string(20)
    key_str = str(datetime.now().time()) + "." + key
    sum = db.get_sum_order_from_cart(user_id)
    order_id = key
    url = client.get_payment_url(order_id, sum, key_str)
    print("ЗАКАЗ {}\n{}\n{}\n{}".format(order_id, key_str, url, sum))
    nav.generate_order(key_str, url)
    await callback_query.message.answer("Чтобы заказать товар, следуйте шагам: \n1) Оплатите покупку на Yoomoney по кнопке\n2) Проверьте оплату по кнопке после оплаты", reply_markup=nav.check_ord)

@bot.dp.callback_query_handler(lambda c: c.data.startswith("check_order_"))
async def check_pay(callback_query: types.CallbackQuery):
    await bot.CPbot.answer_callback_query(callback_query.id)
    key_str = callback_query.data.split("_")[2]
    order_id = key_str.split(".")[2]

    #client.get_all_client_history()
    print(f"Оплата {key_str}: ", client.is_success_payment(key_str))
    if client.is_success_payment(key_str):
        await bot.CPbot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text="✅ Оплата прошла успешно\n🎉 Поздравляем с покупкой")
        db.add_order(order_id, callback_query.message.chat.id)
        db.clear_cart(callback_query.message.chat.id)
    else:
        await bot.CPbot.edit_message_text(message_id=callback_query.message.message_id, 
                                          chat_id=callback_query.message.chat.id, 
                                          text="Чтобы заказать товар, следуйте шагам: \n1) Оплатите покупку на Yoomoney по кнопке\n2) Проверьте оплату по кнопке после оплаты\n❌ Заказ не оплачен", reply_markup=nav.check_ord)
        return

@bot.dp.callback_query_handler(lambda c: c.data == "cancel_act", state=Form.promo)
async def promo_cancel(callback_query: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await bot.CPbot.answer_callback_query(callback_query.id, text="Отменено", show_alert=False)
    await bot.CPbot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text="Ввод промокода отменен.")
        
@bot.dp.callback_query_handler(lambda c: c.data == "enter_promo")
async def enter_prom(callback_query: types.CallbackQuery, state=FSMContext):
    await Form.promo.set()
    await callback_query.message.answer("Введите промокод: ", reply_markup=nav.enter_prom) 
    
@bot.dp.callback_query_handler(lambda c: c.data == "clr_cart")
async def clear_cart(callback_query: types.CallbackQuery):
    if db.clear_cart(callback_query.message.chat.id) == 0:
        await bot.CPbot.answer_callback_query(callback_query.id, text="Корзина очищена!", show_alert=True)
        await bot.CPbot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text="Ваша корзина пуста.")
    else:
        await bot.CPbot.answer_callback_query(callback_query.id, text="Ошибка при очистке корзины! Попробуйте снова.", show_alert=True)

@bot.dp.callback_query_handler(lambda c: c.data == "clr_fav")
async def clear_favourite(callback_query: types.CallbackQuery):
    if db.clear_fav(callback_query.message.chat.id) == 0:
        await bot.CPbot.answer_callback_query(callback_query.id, text="Избранное очищено!", show_alert=True)
        await bot.CPbot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text="Ваше избранное пусто.")
    else:
        await bot.CPbot.answer_callback_query(callback_query.id, text="Ошибка при очистке избранного! Попробуйте снова.", show_alert=True)

@bot.dp.callback_query_handler(lambda c: c.data.startswith("fav_"))
async def add_fav(callback_query: types.CallbackQuery):
    p_id = callback_query.data.split("_")[2]
    cat_id = callback_query.data.split("_")[1]
    if db.add_to_fav(callback_query.message.chat.id, cat_id, p_id) == 0:
        await bot.CPbot.answer_callback_query(callback_query.id, "Добавлено в избранное!")

@bot.dp.callback_query_handler(lambda c: c.data.startswith("tocartfromfav_"))
async def to_cart(callback_query: types.CallbackQuery):
    await bot.CPbot.answer_callback_query(callback_query.id, "Внимание! Товары в текущей корзине будут очищены!", show_alert=True)
    await bot.CPbot.answer_callback_query(callback_query.id, "Перемещено в корзину!")
    db.clear_cart(callback_query.message.chat.id)
    db.to_cart(callback_query.message.chat.id)
    db.clear_fav(callback_query.message.chat.id)
    await bot.CPbot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text="Ваше избранное пусто.")
    

@bot.dp.callback_query_handler(lambda c: c.data == 'c1')
async def process_c1(callback_query: types.CallbackQuery):
    await bot.CPbot.answer_callback_query(callback_query.id, text="Выбрана категория: процессоры", show_alert=False)
    nav.generate_item(1, catalog.id_first_cpu)
    text = functions.generate_msg(catalog.CPUs[catalog.id_first_cpu])
    await bot.CPbot.send_message(callback_query.from_user.id, text, reply_markup=nav.item)

@bot.dp.callback_query_handler(lambda c: c.data == 'c2')
async def process_c2(callback_query: types.CallbackQuery):
    await bot.CPbot.answer_callback_query(callback_query.id, text="Выбрана категория: материнские платы", show_alert=False)
    nav.generate_item(2, catalog.id_first_mb)
    text = functions.generate_msg(catalog.MBs[catalog.id_first_mb])
    await bot.CPbot.send_message(callback_query.from_user.id, text, reply_markup=nav.item)

@bot.dp.callback_query_handler(lambda c: c.data == 'c3')
async def process_c3(callback_query: types.CallbackQuery):
    await bot.CPbot.answer_callback_query(callback_query.id, text="Выбрана категория: материнские платы", show_alert=False)
    nav.generate_item(3, catalog.id_first_vc)
    text = functions.generate_msg(catalog.VCs[catalog.id_first_vc])
    await bot.CPbot.send_message(callback_query.from_user.id, text, reply_markup=nav.item)

@bot.dp.callback_query_handler(lambda c: c.data == 'c4')
async def process_c4(callback_query: types.CallbackQuery):
    await bot.CPbot.answer_callback_query(callback_query.id, text="Выбрана категория: оперативная память", show_alert=False)
    nav.generate_item(4, catalog.id_first_ram)
    text = functions.generate_msg(catalog.RAMs[catalog.id_first_ram])
    await bot.CPbot.send_message(callback_query.from_user.id, text, reply_markup=nav.item)

@bot.dp.callback_query_handler(lambda c: c.data == 'c5')
async def process_c5(callback_query: types.CallbackQuery):
    await bot.CPbot.answer_callback_query(callback_query.id, text="Выбрана категория: блоки питания", show_alert=False)
    nav.generate_item(5, catalog.id_first_ps)
    text = functions.generate_msg(catalog.PSs[catalog.id_first_ps])
    await bot.CPbot.send_message(callback_query.from_user.id, text, reply_markup=nav.item)

@bot.dp.callback_query_handler(lambda c: c.data.startswith("add_"))
async def add_cart(callback_query: types.CallbackQuery):
    p_id = callback_query.data.split("_")[2]
    c_id = catalog.categ_nums[callback_query.data.split("_")[1]]
    if db.add_to_cart(callback_query.message.chat.id, p_id, c_id, 1) == 0:
        await bot.CPbot.answer_callback_query(callback_query.id, text="Добавлено в корзину!", show_alert=False)
    else:
        await bot.CPbot.answer_callback_query(callback_query.id, text="Ошибка добавления! Попробуйте снова.", show_alert=False)

@bot.dp.callback_query_handler(lambda c: c.data.startswith("del_"))
async def del_(callback_query: types.CallbackQuery):
    p_id = callback_query.data.split("_")[2]
    if db.del_from_cart(callback_query.message.chat.id, p_id, 1) == 0:
        await bot.CPbot.answer_callback_query(callback_query.id, text="Успешно убрано из корзины!")
    else:
        await bot.CPbot.answer_callback_query(callback_query.id, text="Ошибка!")

@bot.dp.callback_query_handler(lambda c: c.data.startswith("next_") or c.data.startswith("prev_"))
async def process_paging(callback_query: types.CallbackQuery):
    await bot.CPbot.answer_callback_query(callback_query.id)
    part_id = int(callback_query.data.split("_")[2])
    if part_id == 0:
        await bot.CPbot.answer_callback_query(callback_query.id)
        return
    cat_id = catalog.categ_nums[callback_query.data.split("_")[1]]
    nav.generate_item(cat_id, part_id)
    text = functions.get_text(cat_id, part_id)
    await bot.CPbot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text=text)
    await bot.CPbot.edit_message_reply_markup(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, reply_markup=nav.item)



bot._start_()



    

