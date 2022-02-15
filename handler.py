from questions import questions, get_object_by_id
from random import choice
from education import uni, college
import copy

accept_words = ['Отлично!', 'Поняла.', 'Принято!', 'Следующие варианты']
NOTHING_WORDS = ['ничего', 'никакой']
STUDY_WORDS = ['только вузы', 'вузы', 'только колледжи', 'колледжи', 'оба варианта', 'оба']


def create_question(two_variants_id):
    # создает вопрос
    two_variants = get_object_by_id(two_variants_id, questions)
    question_choices = list(map(lambda choice: choice["text"], two_variants["choices"]))
    return question_choices[0] + ' ' + "или" + ' ' + question_choices[1].lower()


def add_count(choice_n, user_text, user_state): 
    two_variants = get_object_by_id(choice_n, questions)
    subject_choices = list(map(lambda choice: choice["subject"], two_variants["choices"]))
    # увеличивает баллы
    if user_text == "1":
        user_state[subject_choices[0]] += 10 
    else:
        user_state[subject_choices[1]] += 10
    return user_state


def evaluate_result(user_state):
    # рассчитывает результат пользователя
    user_state['repeat'] = 0 # обнуляю, чтобы затем узнать max значение для subject
    user_state['subject'] = 0
    subject = max(user_state, key = user_state.get) # находит max значение и возвращает ключ
    user_state['subject'] = subject

    if subject == 'nature':
        return "человек - природа. Несколько примеров профессий этого типа: эколог, биолог, ветеринар, врач, химик."
    elif subject == 'tech':
        return "человек - техника. Профессии этого типа, ориентированы на создание, применение и обслуживание технических механизмов и конструкций. Вам подходят специальности такие, как электрик, строитель, энергетик, специалист по автоматизации, робототехник, инженер, радиомеханик."
    elif subject == 'human':
        return "человек - человек. К этому типу относятся профессии, связанные с общением с людьми. Вам подходят специальности такие, как психолог, врач, преподаватель, менеджер, юрист, журналист, дипломат, политолог"
    elif subject == 'sign':
        return "человек - знаковая система. Этот тип объединяет профессии, связанные со знаковой информацией, т.е. (текстами, цифрами, звуковыми сигналами, схемами, чертежами). Вам подходят такие специальности, как программист, архитектор, проектный менеджер, переводчик, экономист"
    elif subject == 'creativity':
        return "человек - художественный образ. К этому типу относятся професии, связанные с созданием чего-то нового или творческим переосмыслением уже привычного. Вам подходят такие специальности, как визажист, дизайнер, урбанист, маркетолог, писатель, актер, режиссер"

    
def choose_education(subject, education_place, education_count):
    if education_place == 1:
        text = uni[subject][education_count]
    elif education_place == 2:
        text = college[subject][education_count]
    else:
        pass
    if education_count == 0:
        text = "Чтобы перейти к следующему варианту, скажите \"следующий\"\n" + text

    return text


template = {
        'nature': 0,
        'tech': 0,
        'human': 0,
        'sign': 0,
        'creativity': 0,
        'choice_number' : 1,
        'repeat' : "",
        'subject' : "",
        'education_place' : 0,
        'education_count' : 0
    }


def handler(event, context = {}):

    isEndSession = False

    intents = event['request'].get('nlu', {}).get('intents')
    user_text = event['request']['command'].lower()

    user_state = copy.deepcopy(template)
    user_state.update(event['state']['session'])

    choice_number = user_state['choice_number']
    repeat = user_state['repeat']

    # основной диалог
    if event['session']['new']:
        text = "Все профессии важны, все профессии нужны... Но какую выбрать? Я помогу вам определить свои сильные стороны и подскажу, куда можно пойти учиться. Вам нужно пройти тест. В нем 20 вопросов. Начинаем?"


    elif 'start_test' in intents:
        if choice_number != 1:
            text = "Вы уже начали тест.\n" + "Какой из двух \
                вариантов, первый или второй, вам больше нравится?\n" + create_question(choice_number)
        else:
            text = "Поехали! Я буду предлагать два варианта занятий, \
                а вам нужно будет выбрать тот, который больше нравится \
                и назвать номер. Итак, вы бы хотели...\n" + create_question(1)


    elif user_text in ['1', '2']:
        user_state = add_count(choice_number, user_text, user_state)
        choice_number += 1
        user_state['choice_number'] = choice_number 

        if choice_number <= 20:
            text = choice(accept_words) + '\n' + create_question(choice_number)
        else:
            result = evaluate_result(user_state)
            # результат теста
            text = "Тест завершен. Ваши результат: " + result  + "\n Теперь можно выбирать место учебы. Но перед этим скажите, вы рассматриваете ВУЗы, колледжи или оба варианта" 


    elif user_text in NOTHING_WORDS:
        text = "Нужно обязательно выбрать какой-то вариант"


    elif user_text in STUDY_WORDS:
        if user_text in ['вузы', 'только вузы']:
            user_state['education_place'] = 1
        elif user_text in ['колледжи', 'только колледжи']:
            user_state['education_place'] = 2
        else:
            user_state['education_place'] = 'both'     
        text = choose_education(user_state['subject'], user_state['education_place'], user_state['education_count'])
    

    elif user_text == 'следующий':
        if user_state['education_count'] <= 3:
            user_state['education_count'] += 1
            text = choose_education(user_state['subject'], user_state['education_place'], user_state['education_count'])
        else:
            text = "На этом у меня все! Помните, что в современном быстро меняющемся мире невозможно выбрать профессию один раз и на всю жизнь, скорее всего вы будете менять её в течение жизни, поэтому не бойтесь ошибиться. Что бы вы не выбрали, залог успеха - настойчивость и трудолюбие"


    elif 'repeat' in intents:
        text = repeat


    elif user_text == 'завершить':
        # завершить сессию
        text = "До новых встреч!"
        isEndSession = True

    else:
        text = "Я не понимаю вас.\n Чтобы выйти, скажите \"завершить\".\nЧтобы повторить фразу, скажите \"повторить\"" 
    
    if text[:13] != 'Я не понимаю' or text != 'Нужно обязательно выбрать какой-то вариант':
        user_state['repeat'] = text


    return {
        'version' : event['version'],
        'session' : event['session'],
        'response' : {
            'text' : text,
            'end_session' : isEndSession,

        },
        'session_state' : user_state
    }
