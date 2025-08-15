# Password Manager

[Русский](#русский) | [English](#english)

---

## Русский

Простая и удобная программа для управления паролями с возможностью хранения данных в Excel-файлах. Программа позволяет легко копировать логины, пароли и другую информацию одним кликом.

### 📋 Основные функции
- **Таблица с паролями** - 4 основных колонки:
  - Название (название учетной записи)
  - Логин
  - Пароль
  - Дополнительная информация
- **Копирование одним кликом** - клик по любой ячейке автоматически копирует её содержимое в буфер обмена
- **Визуальное уведомление** - при копировании показывается уведомление с содержимым скопированного текста

### 📁 Работа с файлами
- **Загрузка Excel-файлов** - поддержка файлов формата `.xlsx`
- **Быстрый доступ** - кнопки для мгновенного открытия файлов `Password.xlsx` и `Работа.xlsx`
- **Автоматическое создание** - если файл `Password.xlsx` отсутствует, он создается автоматически
- **Чтение первых 4 колонок** - программа использует только первые 4 столбца Excel-файла, остальные игнорируются

### 🖥️ Интерфейс
- **Сворачивание в трей** - программа сворачивается в системный трей при нажатии крестика или кнопки "Свернуть в трей"
- **Контекстное меню** - правый клик по окну показывает меню с пунктами "Открыть" и "Выход"

## Установка

### Требования
- Python 3.6 или выше
- Windows, Linux или macOS

### Зависимости

Установите необходимые библиотеки:

```bash
pip install pandas openpyxl pyperclip pillow pystray
```

**Описание зависимостей:**
- `pandas` - для работы с Excel-файла
- `openpyxl` - для чтения/записи Excel-файлов
- `pyperclip` - для работы с буфером обмена
- `pillow` - для создания иконки в трее
- `pystray` - для работы с системным треем

## Использование

### Работа с данными
1. **Загрузка файла**:
   - Нажмите "Загрузить файл" для выбора Excel-файла
   - Используйте кнопки быстрого доступа для файлов `Password.xlsx` и `Работа.xlsx`. При желании имена файлов и путь можно поменять в коде. 
2. **Копирование данных**:
   - Кликните по любой ячейке таблицы для копирования её содержимого
   - Скопированный текст будет показан в уведомлении
3. **Сворачивание**:
   - Нажмите крестик или кнопку "Свернуть в трей" для сворачивания в системный трей
   - Правый клик по окну → "Открыть" для восстановления
   - Правый клик по окну → "Выход" для закрытия программы

### Формат Excel-файла
Файл должен содержать как минимум 4 столбца:
1. Название учетной записи
2. Логин
3. Пароль
4. Дополнительная информация
Пустые поля будут выводиться пустыми и в интерфейсе. 

Пример структуры:
| Название | Логин | Пароль | Информация |
|----------|-------|--------|------------|
| Gmail | user@gmail.com | mypassword123 | Личный email |
| VK | vkuser | vkpass456 | Социальная сеть |

## Особенности

- 🛡️ **Безопасность** - данные хранятся локально в Excel-файлах, никакой пересылки в сеть
- 🚀 **Простота** - интуитивный интерфейс без лишних функций
- 🎨 **Удобство** - контрастная таблица и визуальные разделители
- 📱 **Доступность** - быстрый доступ к часто используемым файлам
- 🖱️ **Эргономика** - копирование одним кликом

## Примечания

- При первом запуске программа автоматически создаст файл `Password.xlsx`
- Для полноценной работы иконки в трее рекомендуется установить библиотеку `pystray`
- Программа корректно работает с русскими названиями файлов и данными
- Поддерживает Excel-файлы с любым количеством строк и данными в первых 4 колонках

## Лицензия

MIT License - свободное использование, модификация и распространение.

---

## English

A simple and convenient password management program with the ability to store data in Excel files. The program allows you to easily copy logins, passwords and other information with one click.

### 📋 Main Functions
- **Password table** - 4 main columns:
  - Name (account name)
  - Login
  - Password
  - Additional information
- **One-click copying** - clicking on any cell automatically copies its contents to the clipboard
- **Visual notification** - a notification with the copied text content is displayed when copying

### 📁 File Operations
- **Excel file loading** - support for `.xlsx` format files
- **Quick access** - buttons for instant opening of `Password.xlsx` and `Работа.xlsx` files
- **Automatic creation** - if the `Password.xlsx` file is missing, it is created automatically
- **Reading first 4 columns** - the program uses only the first 4 columns of the Excel file, the rest are ignored

### 🖥️ Interface
- **System tray minimization** - the program minimizes to the system tray when clicking the close button or "Minimize to Tray" button
- **Context menu** - right-click on the window shows a menu with "Open" and "Exit" options

## Installation

### Requirements
- Python 3.6 or higher
- Windows, Linux or macOS

### Dependencies

Install the required libraries:

```bash
pip install pandas openpyxl pyperclip pillow pystray
```

**Dependencies description:**
- `pandas` - for working with Excel files
- `openpyxl` - for reading/writing Excel files
- `pyperclip` - for working with the clipboard
- `pillow` - for creating the tray icon
- `pystray` - for working with the system tray

## Usage

### Working with Data
1. **File loading**:
   - Click "Load file" to select an Excel file
   - Use quick access buttons for `Password.xlsx` and `Работа.xlsx` files. File names and paths can be changed in the code if desired.
2. **Data copying**:
   - Click on any table cell to copy its contents
   - The copied text will be shown in the notification
3. **Minimization**:
   - Click the close button or "Minimize to Tray" button to minimize to the system tray
   - Right-click on window → "Open" to restore
   - Right-click on window → "Exit" to close the program

### Excel File Format
The file must contain at least 4 columns:
1. Account name
2. Login
3. Password
4. Additional information
Empty fields will be displayed as empty in the interface.

Example structure:
| Name | Login | Password | Information |
|------|-------|----------|-------------|
| Gmail | user@gmail.com | mypassword123 | Personal email |
| VK | vkuser | vkpass456 | Social network |

## Features

- 🛡️ **Security** - data is stored locally in Excel files, no network transmission
- 🚀 **Simplicity** - intuitive interface without unnecessary functions
- 🎨 **Convenience** - high-contrast table and visual separators
- 📱 **Accessibility** - quick access to frequently used files
- 🖱️ **Ergonomics** - one-click copying

## Notes

- The program will automatically create the `Password.xlsx` file on first launch
- For full system tray icon functionality, it is recommended to install the `pystray` library
- The program works correctly with Russian file names and data
- Supports Excel files with any number of rows and data in the first 4 columns

## License

MIT License - free use, modification and distribution.
