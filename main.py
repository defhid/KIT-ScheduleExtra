from src.settings import (
    Mapping,
    ColumnIndex,
    SHEET_NAME,
    WEEKDAYS,
    OUTPUT_COLORS,
    OUTPUT_FILE,
    EVEN,
    ODD,
)
from math import isnan
import pandas as pd
import os


def load() -> (list, str):
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

    return df.values.tolist(), group


def filter_by_group(rows: list, group: str) -> list:
    def _check_group_name(r):
        return "".join(filter(lambda ch: ch.isdigit(), str(r[ColumnIndex.GROUP]))) == group

    return list(filter(_check_group_name, rows))


def cast_and_sort(rows: list):
    for row in rows:
        for i in range(len(row)):
            row[i] = "-" \
                if type(row[i]) is float and isnan(row[i]) \
                else str(row[i]).strip()

    rows.sort(key=lambda r: (WEEKDAYS.get(r[ColumnIndex.WEEKDAY].lower(), -1), r[ColumnIndex.TIME]))


def apply_mapping(rows: list):
    def _map(_index: int, mapping: dict):
        row[_index] = mapping.get(row[_index].lower(), row[_index])

    for row in rows:
        _map(ColumnIndex.SUBJECT, Mapping.SUBJECTS)
        _map(ColumnIndex.EXERCISE, Mapping.EXERCISES)
        _map(ColumnIndex.CLASSROOM, Mapping.CLASSROOMS)


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

        grouped.append("<span>" + "  ".join(row[:ColumnIndex.GROUP] + row[ColumnIndex.GROUP + 1:]) + "</span>")

    if grouped:
        content.append(f"<code style=\"color: {colors[color_index]}\">\n" + "\n".join(grouped) + "\n</code>")

    return content


def main():
    rows, group = load()
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

    with open(os.path.abspath(OUTPUT_FILE), 'wb') as output:
        font_path = os.path.abspath(os.path.join("src", "font.otf"))
        if os.sep == "\\":
            font_path = font_path.replace("\\", "\\\\")

        output.write(template.format(general="\n".join(general),
                                     even="\n".join(even), odd="\n".join(odd), font=font_path).encode('utf-8'))

    print(f"Result: {os.path.abspath(OUTPUT_FILE)}")


if __name__ == '__main__':
    main()
