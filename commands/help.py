from loader import bot


@bot.message_handler(commands=['help'])
def help_start(message):
    text_message = 'Бот chhotels — отличный помощник для поиска отелей в любом городе мира. Он находит варианты по ' \
                   'вашим критериям и предоставляет подробную информацию о каждом. Бот выдаст список отелей, ' \
                   'отсортированных по цене или расстоянию от центра города. Также вы можете просмотреть историю ' \
                   'последних запросов, чтобы не тратить время на поиск тех же отелей вновь и вновь.\n' \
                   'Введите команду и наслаждайтесь легким и быстрым поиском идеального места проживания:\n\n' \
                   '/lowprice — список отелей, отсортированных по цене от самой низкой к самой высокой ↗️\n\n' \
                   '/highprice — список отелей, отсортированных по цене от самой высокой к самой низкой ↘️\n\n' \
                   '/bestdeal — список отелей в пределах заданных цены и удаленности от центра 👌🏻\n\n' \
                   '/history — история последних 5 ваших запросов с найденными отелями.'

    bot.send_message(message.from_user.id, text=text_message, parse_mode='markdown')
