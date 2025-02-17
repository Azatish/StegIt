import sys
import os
import requests
import random
import platform
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import piexif

CONFIG_FILE = "lang.conf"
TEST_TEXT = """muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe
muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe
muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe
muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe muhehehe"""

TEXTS = {
    "ru": {
        "logo": r"""        
        _________
       /         \
  ____|   ______  |____
 /  __|  |      |  |__  \
|  |__|  |StegIt|  |__|  | 
|_____   |______|   _____|   
      |___________|
      [   Hidden  ]
      [-----------]""",
        "author": "Автор: Azatish (Telegram: https://t.me/AzatKhairullin)",
        "description": "StegIt — генератор заданий по стеганографии для обучения методам сокрытия информации.",
        "help_prompt": "Введите 'help' для получения справки по командам.\n",
        "help_header": "Доступные команды:",
        "help_content": "  help        - вывод справочной информации о командах.\n  gen         - сгенерировать задание по стеганографии.\n  exit/quit/q - выход из программы",
        "prompt": "> ",
        "unknown": "Неизвестная команда: '{}'. Введите 'help' для получения справки.",
        "exit": "\nВыход из программы.",
        "language_prompt": "Выберите язык / Select language:\n1. Русский\n2. English\nВаш выбор: ",
        "gen_menu_header": "\nВыберите тип задания для генерации:",
        "gen_option_1": " 1. Аудио",
        "gen_option_2": " 2. Картинка",
        "gen_option_3": " 3. Видео",
        "gen_option_4": " 4. Текст",
        "gen_text_options": "\nВыберите задание по текстовой стеганографии:\n random - Случайное задание\n 1 - Использование двойных пробелов\n 2 - Скрытие данных в конечных пробелах\n 3 - Использование невидимых пробелов\n 4 - Замена повторяющихся символов",
        "gen_audio_in_dev": "Аудио-метод находится в разработке. Возврат в главное меню.\n",
        "gen_video_in_dev": "Видео-метод находится в разработке. Возврат в главное меню.\n",
        "gen_image_done": "Сгенерировано задание по стеганографии для изображения.\n",
        "gen_text_done": "Сгенерировано задание по стеганографии для текстовой информации.\n",
        "gen_invalid_choice": "Неверный выбор. Возврат в главное меню.\n",
        "gen_text_task_1": "Используйте двойные пробелы для кодирования скрытых данных (2 пробела = 1, 1 пробел = 0).",
        "gen_text_task_2": "Спрячьте бинарное сообщение в конечных пробелах строк текста.",
        "gen_text_task_3": "Используйте невидимые пробелы (Zero Width Space) для скрытого кодирования.",
        "ask_for_string": "Введите строку, которую вы хотите скрыть:",
        "ask_for_filename": "Введите имя файла, из которого следует записать данные:",
        "invalid_filename": "Неверное имя файла. Попробуйте снова.",
        "file_not_found": "Файл не найден. Будет использован текст по умолчанию.",
        "hiding_info": "Строка '{hidden_string}' будет скрыта в файле '{filename}'.",
        "message_hidden_successfully": "Сообщение успешно скрыто в файле.",
        "insufficient_capacity": "Недостаточная вместимость для скрытия сообщения.",
        "Error": "Ошибка",
        "Picture_saved": "Картинка сохранена как '{new_filename}'",
        "metadata_error": "Ой, формат '{format}' не поддерживает добавление метаданных."
    },
    "en": {
        "logo": r"""        
        _________
       /         \
  ____|   ______  |____
 /  __|  |      |  |__  \
|  |__|  |StegIt|  |__|  | 
|_____   |______|   _____|   
      |___________|
      [   Hidden  ]
      [-----------]""",
        "author": "Author: Azatish (Telegram: https://t.me/AzatKhairullin)",
        "description": "StegIt — a generator for steganography tasks to train methods of hiding information.",
        "help_prompt": "Type 'help' for a list of available commands.\n",
        "help_header": "Available commands:",
        "help_content": "  help        - display help information about commands.\n  gen         - generate a steganography task.\n  exit/quit/q - exit the program",
        "prompt": "> ",
        "unknown": "Unknown command: '{}'. Type 'help' for assistance.",
        "exit": "\nExiting the program.",
        "language_prompt": "Select language / Выберите язык:\n1. Русский\n2. English\nYour choice: ",
        "gen_menu_header": "\nSelect the type of task to generate:",
        "gen_option_1": " 1. Audio",
        "gen_option_2": " 2. Image",
        "gen_option_3": " 3. Video",
        "gen_option_4": " 4. Text",
        "gen_text_options": "\nSelect a text steganography task:\n random - Random task\n 1 - Using double spaces\n 2 - Hiding data in trailing spaces\n 3 - Using zero-width spaces\n 4 - Replacing repeating characters",
        "gen_audio_in_dev": "Audio method is under development. Returning to main menu.\n",
        "gen_video_in_dev": "Video method is under development. Returning to main menu.\n",
        "gen_image_done": "Image steganography task has been generated.\n",
        "gen_text_done": "Text steganography task has been generated.\n",
        "gen_invalid_choice": "Invalid choice. Returning to main menu.\n",
        "gen_text_task_1": "Use double spaces to encode hidden data (2 spaces = 1, 1 space = 0).",
        "gen_text_task_2": "Hide a binary message in trailing spaces of text lines.",
        "gen_text_task_3": "Use zero-width spaces (Zero Width Space) for hidden encoding.",
        "ask_for_string": "Enter the string you want to hide:",
        "ask_for_filename": "Enter the filename from which we are extracting data:",
        "invalid_filename": "Invalid filename. Please try again.",
        "file_not_found": "File not found. Using default texty text.",
        "hiding_info": "The string '{hidden_string}' will be hidden in file '{filename}'.",
        "message_hidden_successfully": "Message successfully hidden in file.",
        "insufficient_capacity": "Insufficient capacity to hide the message.",
        "Error": "Error",
        "Picture_saved": "Picture saved as '{new_filename}'",
        "metadata_error": "Oh, '{format}' format is not supported for metadata addition."
    }
}


def get_language():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            lang = f.read().strip()
            if lang in TEXTS:
                return lang

    choice = input(TEXTS["en"]["language_prompt"])
    if choice.strip() == "1":
        lang = "ru"
    else:
        lang = "en"
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(lang)
    return lang


def display_logo(texts):
    print(texts["logo"])


def display_intro(texts):
    display_logo(texts)
    print(texts["author"])
    print(texts["description"])
    print("\n" + texts["help_prompt"])


def display_help(texts):
    print(texts["help_header"])
    print(texts["help_content"])


def process_metadata_steganography(texts, hidden_string, filename):
    try:
        # Открываем изображение
        image = Image.open(filename)
        format = image.format.upper()

        if format == "PNG":
            metadata = PngInfo()
            metadata.add_text("flag", hidden_string)
            new_filename = f"{filename.split('.')[0]}_with_task.png"
            image.save(new_filename, pnginfo=metadata)
            image.close()
            print(texts["message_hidden_successfully"])
        elif format == "JPEG":
            exif_dict = piexif.load(image.info.get("exif", b""))
            user_comment = hidden_string.encode("utf-8")
            exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment
            exif_bytes = piexif.dump(exif_dict)
            new_filename = f"{filename.split('.')[0]}_with_task.jpg"
            image.save(new_filename, exif=exif_bytes)
            image.close()
            print(texts["message_hidden_successfully"])
        else:
            print(texts["metadata_error"].format(format=format))

    except FileNotFoundError:
        print(texts['file_not_found'])
    except Exception as e:
        print(f"{texts['Error']}: {str(e)}")




def process_image_lsb_steganography(texts, hidden_string, filename):
    try:
        image = Image.open(filename)
        pixels = image.load()

        binary_message = ''.join([format(ord(c), '08b') for c in hidden_string])
        binary_message += '00000000'  # $$$$$$

        if len(binary_message) > image.width * image.height:
            print(texts['insufficient_capacity'])
            return

        message_index = 0
        rand = random.randint(1, 3)
        for y in range(image.height):
            for x in range(image.width):
                if message_index < len(binary_message):
                    r, g, b = pixels[x, y]
                    if rand == 1:
                        r = (r & ~1) | int(binary_message[message_index])
                    elif rand == 2:
                        g = (g & ~1) | int(binary_message[message_index])
                    else:
                        b = (b & ~1) | int(binary_message[message_index])
                    message_index += 1

                    pixels[x, y] = (r, g, b)
                else:
                    break

        new_filename = f"{filename.split('.')[0]}_task.png"
        image.save(new_filename)

        print(texts['message_hidden_successfully'])
        print(texts['Picture_saved'].format(new_filename=new_filename))

    except FileNotFoundError:
        print(texts['file_not_found'])
    except Exception as e:
        print(f"{texts['Error']}: {str(e)}")


def process_repeating_characters_steganography(texts, hidden_string, filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            texty = f.read()
    else:
        print(texts["file_not_found"])
        texty = TEST_TEXT

    replacable_indexes = {}
    for el in range(len(texty)):
        if texty[el].lower() in "укехорасмибтetyopkaxcm":
            if texty[el] in replacable_indexes:
                replacable_indexes[texty[el]] += [el]
            else:
                replacable_indexes[texty[el]] = [el]

    required_capacity = len(hidden_string) * 8
    max_len = 0
    for el in list(replacable_indexes.values()):
        if len(el) > max_len:
            max_len = len(el)
            to_replace = el
    if max_len < required_capacity:
        print(texts["insufficient_capacity"])
        return

    binary_message = "".join([format(ord(c), "08b") for c in hidden_string])

    texty_list = list(texty)
    bit_index = 0
    for idx in to_replace:
        if bit_index >= len(binary_message):
            break
        if binary_message[bit_index] == '1':
            if texty_list[idx].islower():
                texty_list[idx] = texty_list[idx].upper()
            elif texty_list[idx].isupper():
                texty_list[idx] = texty_list[idx].lower()
        bit_index += 1

    stego_text = "".join(texty_list)

    with open(f"{filename}_task", "w", encoding="utf-8") as f:
        f.write(stego_text)
        f.close()

    print(texts["message_hidden_successfully"])


def process_double_spaces_steganography(texts, hidden_string, filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            texty = f.read()
    else:
        print(texts["file_not_found"])
        texty = TEST_TEXT
    binary_message = "".join([format(ord(c), "08b") for c in hidden_string])

    if texty.count(" ") < len(binary_message):
        print(texts["insufficient_capacity"])
        return

    stego_text = ""
    message_index = 0

    for char in texty:
        if char == " " and message_index < len(binary_message):
            if binary_message[message_index] == "1":
                stego_text += "  "  # Двойной пробел для бита "1"
            else:
                stego_text += " "   # Одинарный пробел для бита "0"
            message_index += 1
        else:
            stego_text += char

    with open(f"{filename}_task", "w", encoding="utf-8") as f:
        f.write(stego_text)
        f.close()

    print(texts["message_hidden_successfully"])


def process_text_steganography(texts):
    print(texts["ask_for_string"])
    hidden_string = input(texts["prompt"]).strip()

    print(texts["ask_for_filename"])
    filename = input(texts["prompt"]).strip()

    if platform.system() == "Windows":
        filename = filename.replace("/", "\\")
    else:
        filename = filename.replace("\\", "/")

    if not filename:
        print(texts["invalid_filename"])
        return

    print(texts["hiding_info"].format(hidden_string=hidden_string, filename=f"{filename}_task"))
    print(texts["gen_text_options"])
    choice = input(texts["prompt"]).strip()

    if choice == "1":
        print(texts["gen_text_task_1"])
        process_double_spaces_steganography(texts, hidden_string, filename)
    elif choice == "2":
        print(texts["gen_text_task_2"])
    elif choice == "3":
        print(texts["gen_text_task_3"])
    elif choice == "4":
        print(texts["gen_text_task_4"])
        process_repeating_characters_steganography(texts, hidden_string, filename)
    elif choice == "random":
        task = random.choice([
            texts["gen_text_task_1"],
            texts["gen_text_task_2"],
            texts["gen_text_task_3"]
        ])
        print(task)
    else:
        print(texts["gen_invalid_choice"])


def process_image_steganography(texts):
    print(texts['ask_for_string'])
    hidden_string = input(texts['prompt']).strip()

    print(texts['ask_for_filename'])
    filename = input(texts['prompt']).strip()

    if not filename:
        print(texts['invalid_filename'])
        return

    print(texts['hiding_info'].format(hidden_string=hidden_string, filename=filename))
    print("Выберите метод стеганографии для изображения:")
    print(" 1. LSB (Least Significant Bit)")
    print(" 2. Скрытие в метаданных")

    choice = input(texts['prompt']).strip()

    if choice == "1":
        process_image_lsb_steganography(texts, hidden_string, filename)
    elif choice == "2":
        process_metadata_steganography(texts, hidden_string, filename)
    else:
        print(texts['gen_invalid_choice'])



def generate(texts):
    print(texts["gen_menu_header"])
    print(texts["gen_option_1"])
    print(texts["gen_option_2"])
    print(texts["gen_option_3"])
    print(texts["gen_option_4"])

    choice = input(texts["prompt"]).strip()
    if choice == "1":
        print(texts["gen_audio_in_dev"])
    elif choice == "2":
        process_image_steganography(texts)
    elif choice == "3":
        print(texts["gen_video_in_dev"])
    elif choice == "4":
        process_text_steganography(texts)
    else:
        print(texts["gen_invalid_choice"])


def main():
    if any(arg in ("-h", "--help") for arg in sys.argv[1:]):
        display_help(TEXTS["en"])
        sys.exit(0)

    lang = get_language()
    texts = TEXTS[lang]
    display_intro(texts)

    while True:
        try:
            command = input(texts["prompt"]).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(texts["exit"])
            break

        if command == "help":
            display_help(texts)
        elif command in ("gen", "generate"):
            generate(texts)
        elif command in ("quit", "q", "exit"):
            sys.exit(0)
        elif command == "":
            continue
        else:
            print(texts["unknown"].format(command))


if __name__ == "__main__":
    main()
