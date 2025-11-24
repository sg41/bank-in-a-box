import argparse
from pathlib import Path
import re

def create_text_dump(source_dir: str, output_file: str, extension: str = None, regex: str = None):
    """
    Создаёт текстовый дамп файлов из проекта.

    - Если указан regex — используется регулярное выражение по имени файла.
    - Иначе, если указано extension — фильтрует по точному расширению (автоматически добавляет $ в конец и экранирует точку).
    - Если ничего не указано — используется .dart по умолчанию.

    :param source_dir: Корневая директория проекта.
    :param output_file: Выходной файл.
    :param extension: Простое расширение, например ".yaml"
    :param regex: Регулярное выражение, например r"\\.ya?ml$"
    """
    source_path = Path(source_dir).resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"Исходная директория не найдена: {source_path}")

    # Определяем паттерн
    if regex is not None:
        # Используем регулярное выражение "как есть"
        try:
            pattern = re.compile(regex)
        except re.error as e:
            raise ValueError(f"Некорректное регулярное выражение: {e}")
    else:
        # Используем простое расширение
        if extension is None:
            extension = ".dart"
        # Экранируем точку и добавляем привязку к концу строки
        escaped_ext = re.escape(extension)
        pattern = re.compile(escaped_ext + r"$")

    # Собираем и фильтруем файлы
    all_files = source_path.rglob("*")
    filtered_files = [
        f for f in all_files
        if f.is_file() and pattern.search(f.name)
    ]
    filtered_files = sorted(filtered_files)

    # Запись дампа
    with open(output_file, "w", encoding="utf-8") as out_f:
        for source_file in filtered_files:
            rel_path = source_file.relative_to(source_path)
            out_f.write(f"=== {rel_path} ===\n")
            try:
                with open(source_file, "r", encoding="utf-8") as src_f:
                    content = src_f.read()
            except (UnicodeDecodeError, OSError):
                content = "// [Файл не может быть прочитан как текст]\n"
            out_f.write(content)
            if not content.endswith("\n"):
                out_f.write("\n")
            out_f.write("\n")

    print(f"✅ Текстовый дамп создан: {Path(output_file).resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Создаёт текстовый дамп всех исходных файлов проекта в один файл."
    )
    parser.add_argument(
        "source",
        help="Путь к корневой папке проекта"
    )
    parser.add_argument(
        "-o", "--output",
        default="project_dump.txt",
        help="Имя выходного текстового файла (по умолчанию: project_dump.txt)"
    )
    parser.add_argument(
        "-e", "--extension",
        default=None,
        help="Простое расширение файлов, например '.yaml' или '.js' (по умолчанию: '.dart')"
    )
    parser.add_argument(
        "-r", "--regex",
        default=None,
        metavar="PATTERN",
        help="Регулярное выражение для имени файла (например: '\\.ya?ml$'). "
             "Имеет приоритет над --extension."
    )

    args = parser.parse_args()

    try:
        create_text_dump(
            source_dir=args.source,
            output_file=args.output,
            extension=args.extension,
            regex=args.regex
        )
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()