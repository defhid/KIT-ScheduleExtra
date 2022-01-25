from src.settings import (
    Mapping,
    ColumnIndex,
    COLUMNS_ORDER,
    SHEET_NAME,
    WEEKDAYS,
    OUTPUT_COLORS,
    EVEN,
    ODD,
)
from math import isnan
import pandas as pd
import os


def load() -> (str, list, str):
    filepath = input("Input path to schedule file (.xlsx):\n").strip("'\"")
    while not os.path.exists(filepath):
        filepath = input("Filepath is incorrect! Please, try again:\n").strip("'\"")

    try:
        df = pd.read_excel(filepath, sheet_name=SHEET_NAME, engine="openpyxl")
    except Exception:
        print("Error occurred while opening schedule file!")
        raise

    group = input("Input your group name:\n").strip()
    while not group or not group.isdigit():
        group = input("Incorrect group name! Please, try again:\n").strip()

    return os.path.dirname(filepath), df.values.tolist(), group


def filter_by_group(rows: list, group: str) -> list:
    def _check_group_name(r):
        return "".join(filter(lambda ch: ch.isdigit(), str(r[ColumnIndex.GROUP]))) == group

    return list(filter(_check_group_name, rows))


def cast_and_sort(rows: list):
    add = []

    for row in rows:
        for i in range(len(row)):
            row[i] = "-" \
                if type(row[i]) is float and isnan(row[i]) \
                else str(row[i]).strip()
        if '/' in row[ColumnIndex.EVEN_ODD]:
            row[ColumnIndex.EVEN_ODD] = EVEN
            add.append(row.copy())
            add[-1][ColumnIndex.EVEN_ODD] = ODD
    
    rows += add
    rows.sort(key=lambda r: (WEEKDAYS.get(r[ColumnIndex.WEEKDAY].lower(), -1), r[ColumnIndex.TIME], r[ColumnIndex.EVEN_ODD]))


def apply_mapping(rows: list):
    def _map(_index: int, mapping: dict):
        row[_index] = mapping.get(row[_index].lower(), row[_index])

    for row in rows:
        _map(ColumnIndex.SUBJECT, Mapping.SUBJECTS)
        _map(ColumnIndex.EXERCISE, Mapping.EXERCISES)
        _map(ColumnIndex.CLASSROOM, Mapping.CLASSROOMS)
    
    for row in rows:
        row[ColumnIndex.WEEKDAY] = row[ColumnIndex.WEEKDAY].lower().capitalize()
        row[ColumnIndex.TIME] = ":".join(str(row[ColumnIndex.TIME]).split(":")[:2])
        row[ColumnIndex.FIO] = " ".join(x.lower().capitalize() for x in row[ColumnIndex.FIO].split())


def make_schedule(rows: list) -> list[str]:
    lengths = [max(map(lambda r: len(r[i]), rows)) for i in range(len(rows[0]))]

    last_wd = None
    colors = OUTPUT_COLORS if OUTPUT_COLORS else [""]
    color_index = 0

    content = []
    grouped = []
    for row in rows:
        if last_wd != row[ColumnIndex.WEEKDAY]:
            last_wd = row[ColumnIndex.WEEKDAY]
            if grouped:
                content.append(f"<code style=\"color: {colors[color_index]}\">\n" + "\n".join(grouped) + "\n</code>")
                color_index = (color_index + 1) % len(OUTPUT_COLORS)
            grouped.clear()

        for i in range(len(lengths)):
            row[i] += " " * (lengths[i] - len(row[i]))

        grouped.append("<span>" + "  ".join(map(lambda j: row[j], COLUMNS_ORDER)) + "</span>")

    if grouped:
        content.append(f"<code style=\"color: {colors[color_index]}\">\n" + "\n".join(grouped) + "\n</code>")

    return content


def make_output_filename(directory) -> str:
    out_path = os.path.join(directory, 'output.html')
    i = 0
    while os.path.exists(out_path):
        i += 1
        out_path = os.path.join(directory, 'output' + str(i) + '.html')
    return out_path


def main():
    directory, rows, group = load()
    rows = filter_by_group(rows, group)

    if not rows:
        print(f"Group '{group}' not found!")
        return

    cast_and_sort(rows)

    apply_mapping(rows)

    with open("src/template.html", 'rb') as f:
        template = f.read().decode('utf-8')

    general = make_schedule(rows)
    even = make_schedule(list(filter(lambda r: r[ColumnIndex.EVEN_ODD].lower() != ODD, rows)))
    odd = make_schedule(list(filter(lambda r: r[ColumnIndex.EVEN_ODD].lower() != EVEN, rows)))

    out_path = make_output_filename(directory)

    with open(out_path, 'wb') as output:
        font_path = os.path.abspath(os.path.join("src", "font.otf"))
        if os.sep == "\\":
            font_path = font_path.replace("\\", "\\\\")

        output.write(template.format(general="\n".join(general),
                                     even="\n".join(even), odd="\n".join(odd), font=font_path).encode('utf-8'))

    print(f"Result: {out_path}")


if __name__ == '__main__':
    main()
