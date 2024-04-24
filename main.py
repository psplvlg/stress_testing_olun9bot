import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaDocument
import os

from Array import Array
from Variable import Variable
from config import BOT_TOKEN
from find_test import find_test
from generate_test import generate_test

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

type_parametr = [None, 4, 6]  # 4 - variable, 6 - array
id_functions = {"ask_variable": 4, "ask_array": 6}


def get_ans(text):
    print(text)
    return text.lower() == '+'


async def start(update, context):
    os.makedirs(f'user_files/{update.message.chat.id}', exist_ok=True)

    await update.message.reply_text(
        "Привет, я бот-тестировщик. Я могу помочь найти не работающий тест к твоему решению!\n"
        "Для начала нужно сгенерировать тесты, для этого введи команду /gen_test"
    )


async def help(update, context):
    await update.message.reply_text(
        "Тут пока ничего (")


async def gen_test(update, context):
    context.user_data['test_format'] = [[]]
    await update.message.reply_text(
        "Пора вводить параметры!\n"
        'Хотите ли добавить первый? Напишите, пожалуйста, "+" или "-"')
    return 1


async def ask_type_parametr(update, context):
    add = get_ans(update.message.text)
    if not add:
        await update.message.reply_text(
            "Я начал генерировать тесты к твоей задаче")
        in_file = generate_test(update.message.chat_id, context.user_data['test_format'])
        path = f"user_files/{update.message.chat.id}/in.txt"
        print(path)
        await context.bot.send_document(update.message.chat.id, open(path, 'rb'),
                                        "Все готово! Проверь, такой ли тест ты хотел получить?\n"
                                        "Если все хорошо, то введи комаду /add_solution, иначе введи /gen_test\n")
        return ConversationHandler.END
    await update.message.reply_text(
        'Тип параметра:\n'
        '1 - для переменной;\n'
        '2 - для массива;\n')
    return 2


async def get_type_parametr(update, context):
    t = int(update.message.text)
    if type_parametr[t] == id_functions["ask_variable"]:
        await update.message.reply_text(
            'Введите характеристику переменной:\n'
            'название;\n'
            'минимальное значение;\n'
            'максимальное значение;\n'
            '"-" или "+" (если переменную нужно вводить на текущей строке, напишите "-", иначе - "+");\n'
            'Образец: "n 1 100 +"')
        return 3
    elif type_parametr[t] == id_functions["ask_array"]:
        await update.message.reply_text(
            'Введите характеристику массива:\n'
            'название;\n'
            'количество элементов (имя переменной количества);'
            'минимальное значение элемента;\n'
            'максимальное значение элемента;\n'
            '"-" или "+" (если массив нужно вводить на текущей строке, напишите "-", иначе - "+")\n'
            'Образец: "a n 1 100 +"')
        return 4
    await update.message.reply_text(
        'Вы ввели что-то не то, попробуйте еще раз!\n')
    return 2


async def get_variable(update, context):
    inp = list(update.message.text.split())
    var = Variable(*inp[:-1])
    if get_ans(inp[-1]):
        context.user_data['test_format'].append([])
    context.user_data['test_format'][-1].append(var)
    await update.message.reply_text(
        'Хотите ли добавить еще один? Напишите, пожалуйста, "+" или "-"')
    return 1


async def get_array(update, context):
    inp = list(update.message.text.split())
    ar = Array(*inp[:-1])
    if get_ans(inp[-1]):
        context.user_data['test_format'].append([])
    context.user_data['test_format'][-1].append(ar)
    await update.message.reply_text(
        'Хотите ли добавить еще один? Напишите, пожалуйста, "+" или "-"')
    return 1


async def add_solution(update, context):
    await update.message.reply_text(
        "Отправь мне, верное, но, возможно, не оптимальное решение")
    return 1


async def get_correct_solution(update, context):
    fileName = f"user_files/{update.message.chat.id}/{update.message.document.file_id}.py"
    context.user_data['correct_id'] = f"{update.message.document.file_id}.py"
    new_file = await update.message.effective_attachment.get_file()
    await new_file.download_to_drive(fileName)

    await update.message.reply_text(
        "Получил! Теперь мне нужно твое неправильное решение)")
    return 2


async def get_bad_solution(update, context):
    fileName = f"user_files/{update.message.chat.id}/{update.message.document.file_id}.py"
    context.user_data['bad_id'] = f"{update.message.document.file_id}.py"
    new_file = await update.message.effective_attachment.get_file()
    await new_file.download_to_drive(fileName)

    await update.message.reply_text(
        "Получил! Чтобы я начал стрессить твой код, напиши мне /start_stress")
    return ConversationHandler.END


async def start_stress(update, context):
    await update.message.reply_text(
        "Я уже начал поиск теста...")

    if find_test(update.message.chat.id, context.user_data['test_format'],
                 context.user_data['correct_id'], context.user_data['bad_id']):
        await update.message.reply_text(
            "Ура! Кажется, я его нашел!")

        path = f"user_files/{update.message.chat.id}/"
        print(path)

        in_txt = open(path + 'in.txt', 'rb')
        await context.bot.send_document(update.message.chat.id, in_txt)
        in_txt.close()
        cor_txt = open(path + 'correct_out.txt', 'rb')
        await context.bot.send_document(update.message.chat.id, cor_txt)
        cor_txt.close()
        bad_txt = open(path + 'bad_out.txt', 'rb')
        await context.bot.send_document(update.message.chat.id, bad_txt)
        bad_txt.close()

        await update.message.reply_text("Все готово! Проверь, такой ли тест не работает?\n"
                                        "Если нет, то введи /start_stress и я пойду искать дальше...\n")
    else:
        await update.message.reply_text(
            "Извини, у меня не получилось :( Попробуй изменить параметры теста... /gen_test")

async def get_status(update, context):
    await update.message.reply_text(
        "Тестирую...")


async def stop(update, context):
    await update.message.reply_text(
        "Ой! что-то пошло не так :(")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    conv_handler_set_test_format = ConversationHandler(
        entry_points=[CommandHandler('gen_test', gen_test)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_type_parametr)],  # ask type -> get type
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_type_parametr)],  # get type -> new var; -> new ar
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_variable)],  # get var -> add new param
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_array)],  # get ar -> add new param
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler_set_test_format)

    conv_handler_get_correct_solution = ConversationHandler(
        entry_points=[CommandHandler('add_solution', add_solution)],

        states={
            1: [MessageHandler(filters.Document.ALL & ~filters.COMMAND, get_correct_solution)],  # add correct
            2: [MessageHandler(filters.Document.ALL & ~filters.COMMAND, get_bad_solution)],  # add bad
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler_get_correct_solution)

    application.add_handler(CommandHandler("start_stress", start_stress))

    application.run_polling()


if __name__ == '__main__':
    main()



