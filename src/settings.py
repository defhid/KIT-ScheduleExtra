class Mapping:
    SUBJECTS = {
        'технология разработки и защиты баз данных'.lower(): "ТРиЗБД",
        'инфокоммуникационные системы и сети'.lower(): "ИСиС",
        'инструментальные средства разработки программного обеспечения'.lower(): "ИСРПО",
        'технические средства информатизации'.lower(): "ТСИ",
        'микропроцессорные системы'.lower(): "МС",
        'компьютерные сети'.lower(): "КС",
        'наладчик технологического оборудования'.lower(): "НТО",
        'правовое обеспечение профессиональной деятельности'.lower(): "ПОПД",
        'физическая культура'.lower(): "Физ-ра",
        'иностранный язык'.lower(): "Ин. язык",
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

SHEET_NAME = "Лист1"

EVEN = "чет".lower()
ODD = "неч".lower()
