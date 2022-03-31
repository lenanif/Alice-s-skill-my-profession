from questions import *
from education import *
from random import choice
import copy

accept_words = ['Отлично!\n', 'Поняла.\n', 'Принято!\n', 'Следующие варианты\n', '']
NOTHING_WORDS = ['ничего', 'никакой', 'не знаю']
STUDY_WORDS = ['вузы', 'колледжи']


def create_question(two_variants_id:int):
    # создает вопрос, который выводится на экран
    two_variants = get_object_by_id(two_variants_id, questions)
    question_choices = list(map(lambda choice: choice["text"], two_variants["choices"]))
    return question_choices[0] + " или " + question_choices[1].lower()


def create_speach(two_variants_id:int):
    # создает вопрос, который озвучивает
    two_variants = get_object_by_id(two_variants_id, questions)
    question_choices = list(map(lambda choice: choice["speak"], two_variants["choices"]))
    return question_choices[0] + ' sil <[120]> ' + " или " + question_choices[1].lower()


def add_count(choice_n:int, user_text:str, user_state:dict): 
    two_variants = get_object_by_id(choice_n, questions)
    subject_choices = list(map(lambda choice: choice["subject"], two_variants["choices"]))
    # увеличивает баллы
    if user_text == "1":
        user_state[subject_choices[0]] += 10 
    else:
        user_state[subject_choices[1]] += 10
    return user_state


def evaluate_result(user_state:dict):
    # рассчитывает результат пользователя
    user_state['repeat'] = 0 # обнуляю, чтобы затем узнать max значение для subject
    user_state['subject'] = 0
    user_state['current_user_status'] = 0
    user_state['choice_number'] = 0
    user_state['repeat_speach'] = 0

    subject = max(user_state, key = user_state.get) # находит max значение и возвращает ключ
    user_state['subject'] = subject

    if subject == 'nature':
        return "человек - природа. Несколько примеров профессий этого типа: эколог, биолог, ветеринар, врач, химик."
    elif subject == 'tech':
        return "человек - техника. Профессии этого типа ориентированы на создание, применение и обслуживание технических механизмов и конструкций. Вам подходят такие специальности, как электрик, строитель, энергетик, специалист по автоматизации, робототехник, инженер, радиомеханик."
    elif subject == 'human':
        return "человек - человек. К этому типу относятся профессии, связанные с общением с людьми. Вам подходят специальности такие, как психолог, врач, преподаватель, менеджер, юрист, журналист, дипломат, политолог."
    elif subject == 'sign':
        return "человек - знаковая система. Этот тип объединяет профессии, связанные со знаковой информацией, т.е. (текстами, цифрами, звуковыми сигналами, чертежами). Вам подходят такие специальности, как программист, архитектор, проектный менеджер, переводчик, экономист."
    elif subject == 'creativity':
        return "человек - художественный образ. К этому типу относятся профессии, связанные с созданием чего-то нового или творческим переосмыслением уже привычного. Вам подходят такие специальности, как визажист, дизайнер, урбанист, маркетолог, писатель, актер, режиссер."

    
def choose_education(subject:str, education_place:int, education_count:int):
    if education_place == 1:
        text = uni[subject][education_count]
    elif education_place == 2:
        text = college[subject][education_count]
    if education_count == 0:
        text +=  "\nЧтобы перейти к следующему варианту, скажите \"следующий\""
    return text


template = {
        'nature': 0,
        'tech': 0,
        'human': 0,
        'sign': 0,
        'creativity': 0,
        'choice_number': 1,
        'repeat': "",
        'repeat_speach': "",
        'subject': "",
        'education_place': 0,
        'education_count': 0,
        'current_user_status': 0
    }


def handler(event:dict, context = {}):

    isEndSession = False
    speach = ""
    intents = event['request'].get('nlu', {}).get('intents')
    # обновляем сохраненное состояние игрока 
    user_state = copy.deepcopy(template)
    user_state.update(event['state']['session'])

    if event['request']['type'] == 'ButtonPressed':
        user_text = event['request']['nlu']['tokens'][0].lower()
    else:
        user_text = event['request']['command'].lower()

    choice_number = user_state['choice_number']
    repeat_text = user_state['repeat']
    repeat_speach = user_state['repeat_speach']

    # основной диалог
    if event['session']['new']:
        text = "Все профессии важны, все профессии нужны... Но какую выбрать? Я помогу вам с этим и подскажу, куда можно пойти учиться. Для этого нужно пройти тест.\nЧтобы узнать подробности, спросите \"Что ты умеешь?\"\nЧтобы начать тест, скажите \"Начать\"." 
        user_state['current_user_status'] = 'start_skill'


    elif user_text in ["помощь", "что", "что ты умеешь"] and user_state['current_user_status'] == 'start_skill':
        text = "Тест составлен так, что в каждом вопросе вам нужно выбрать деятельность, которая вам больше по душе. Далее вы узнаете, к какой профессиональной сфере вы склонны. Затем я назову несколько примеров профессий и учебных заведений Москвы, где есть эти специальности. Теперь к тесту?"
        speach = "Тест составлен так, что в каждом вопросе вам нужно выбрать деятельность, которая вам больше по душе. Далее вы узнаете, к какой профессиональной сфере вы склонны. Затем я назову несколько примеров профессий и учебных заведений Москвы, где есть эти специальности.' sil <[100]> 'Теперь к тэсту?"

    elif 'start_test' in intents and user_state['current_user_status'] == 'start_skill':
        if choice_number > 1:
            text = "Вы уже начали тест.\n" + "Какой из двух вариантов, первый или второй, вам больше нравится?\n" + create_question(choice_number)
        elif choice_number == 0: # проверяем, тк пользователь может сказать "Да" в любой момент. После окончания теста choice_number обнуляется
            text = "Я не понимаю вас.\n Я могу повторить фразу или завершить навык."
        else:
            text = f"Поехали!\n{choice_number}/20\nВам нужно из двух вариантов выбрать тот, который больше нравится и назвать номер. Итак, вы бы хотели...\n" + create_question(choice_number)
            speach = "Поехали! Вам нужно из двух вариантов выбрать тот, который больше нравится и назвать номер. sil <[180]> Итак, вы бы хотели..." + create_speach(choice_number)
            user_state['current_user_status'] = 'test'


    elif user_text in ["1", "2"] and user_state['current_user_status'] == 'test':
        user_state = add_count(choice_number, user_text, user_state)
        choice_number += 1
        user_state['choice_number'] = choice_number 

        if choice_number <= 20:
            accept_w = choice(accept_words)
            text = f"{choice_number}/20\n" + accept_w + create_question(choice_number)
            speach = accept_w + create_speach(choice_number)
        else:
            result = evaluate_result(user_state)
            # результат теста
            user_state['current_user_status'] = 'choose_education_place'
            text = "Тест завершен. Ваши результат: " + result  + "\nТеперь я предложу несколько вариантов учебных заведений, где вы можете получить необходимые знания. Но перед этим скажите, вы рассматриваете ВУЗы или колледжи?" 
            speach = "Тест завершен. Ваши результат: " + result  + "sil <[180]>\nТеперь я предложу несколько вариантов учебных заведений, где вы можете получить необходимые знания. Но перед этим скажите, вы рассматриваете ВУЗы или колледжи?"


    elif user_text in NOTHING_WORDS:
        text = "Нужно обязательно выбрать какой-то вариант"


    elif user_text in STUDY_WORDS:
        if user_text == 'вузы':
            user_state['education_place'] = 1
        elif user_text == 'колледжи':
            user_state['education_place'] = 2    
        text = choose_education(user_state['subject'], user_state['education_place'], user_state['education_count'],)
        user_state['current_user_status'] = 'next'


    elif user_text == 'следующий' and user_state['current_user_status'] == 'next':
        if user_state['education_count'] <= 3:
            user_state['education_count'] += 1
            text = choose_education(user_state['subject'], user_state['education_place'], user_state['education_count'])
        else:
            text = "На этом у меня все!"
            speach = "На этом у меня все! Помните, что в современном быстро меняющемся мире невозможно выбрать профессию только один раз, скорее всего вы будете менять её в течение жизни, поэтому не бойтесь ошибиться. Что бы вы не выбрали, залог успеха - настойчивость и трудолюбие"
            user_state['current_user_status'] = 0


    elif 'repeat' in intents:
        if repeat_speach != "":
            speach = repeat_speach
        else: 
            speach = repeat_text
        text = repeat_text


    elif 'finish_test' in intents:
        # завершить сессию
        text = "Пока-пока!"
        isEndSession = True


    else:
        text = "Я не понимаю вас.\nЯ могу повторить фразу или завершить навык." 
    

    if text != 'Я не понимаю вас.\nЯ могу повторить фразу или завершить навык.' and text != 'Нужно обязательно выбрать какой-то вариант':
        user_state['repeat_speach'] = speach
        user_state['repeat'] = text


    # response template
    response = {
        'version' : event['version'],
        'session' : event['session'],
        'response' : {
            'text' : text,
            'end_session' : isEndSession,
            'buttons' : []
        },
        'session_state' : user_state
    }


    if speach != "":

        response = {
            'version' : event['version'],
            'session' : event['session'],
            'response' : {
                'text' : text,
                'tts' : speach,
                'end_session' : isEndSession,
                'buttons' : []
            },
            'session_state' : user_state
        }

    # buttons
    if user_state['current_user_status'] == 'start_skill':
        response['response']['buttons'] = [
            {
                'title': "Начать",
                'hide': True
            },
            {
                'title': "Помощь",
                'hide': True
            },
            {
                'title': "Что ты умеешь?",
                'hide': True
            }
        ]

    elif user_state['current_user_status'] == 'test':
        response['response']['buttons'] = [
            {
                'title': "1",
                'hide': True
            },
            {
                'title': "2",
                'hide': True
            }
        ]
    elif user_state['current_user_status'] == 'next':
        response['response']['buttons'] = [
            {
                'title': "Следующий",
                'hide': True
            }
        ]
    elif user_state['current_user_status'] == 'choose_education_place':
        response['response']['buttons'] = [
            {
                'title': "ВУЗы",
                'hide': True
            },
            {
                'title': "Колледжи",
                'hide': True
            }
        ]

    return response
