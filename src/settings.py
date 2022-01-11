class Mapping:
    SUBJECTS = {
        'технология разработки и защиты баз данных'.lower(): "ТРиЗБД",
        'инфокоммуникационные системы и сети'.lower(): "ИСиС",
        'инструментальные средства разработки программного обеспечения'.lower(): "ИСРПО",
        'компьютерные сети'.lower(): "КС",
        'наладчик технологического оборудования'.lower(): "НТО",
        'физическая культура'.lower(): "Физ-ра",
        'иностранный язык'.lower(): "Ин. язык",
        'информационная безопасность'.lower(): "ИБ",
        'Управление проектами'.lower(): "УП",
    }
    EXERCISES = {
        'лаб. раб.'.lower(): "ЛР  ",
        'практика'.lower(): "ПР  ",
        'лекция'.lower(): "Лек "
    }
    CLASSROOMS = {
        'спортзал'.lower(): 'с/з',
    }


class ColumnIndex:
    WEEKDAY = 1
    GROUP = 0
    TIME = 2
    EVEN_ODD = 3
    SUBJECT = 4
    EXERCISE = 5
    CLASSROOM = 6
    BUILDING = 7
    FIO = 8


WEEKDAYS = {
    'пн'.lower(): 1,
    'вт'.lower(): 2,
    'ср'.lower(): 3,
    'чт'.lower(): 4,
    'пт'.lower(): 5,
    'сб'.lower(): 6,
    'вс'.lower(): 7,
}

OUTPUT_COLORS = [
    "#34a434",  # green
    "#a4a41f",  # yellow
    "#e09a1a",  # orange
    "#19b3b3",  # blue
    "#c117c1",  # purple
    "#dc2e2e",  # red
]

OUTPUT_FILE = 'output.html'

SHEET_NAME = "Лист2"

EVEN = "чет".lower()
ODD = "неч".lower()
