"""Text constants for bot messages (Russian).

## Traceability
Component: Core / Vocabulary
"""

WELCOME = (
    "Добро пожаловать в <b>AI Presentation Builder</b>!\n"
    "Я помогу вам создать презентацию из текста или голосового сообщения."
)

CREATE_PROMPT = "Отправьте текст или голосовое сообщение для создания презентации"

STRUCTURING = "Структурирую презентацию..."

SLIDE_TEMPLATE = (
    "<b>Слайд {index}/{total}</b>\n\n"
    "<b>{title}</b>\n\n"
    "{text}\n\n"
    "<i>{visual_description}</i>"
)

EDIT_PROMPT = "Отправьте команду редактирования текстом или голосом"

CONFIRM_PROMPT = "Подтвердите создание презентации"

EXPORT_READY = "Ваша презентация готова!"

ERROR = "Произошла ошибка: {error}"

NO_PRESENTATIONS = "У вас нет презентаций"

PRESENTATION_CREATED = "Презентация создана! Отправляйте материал."

INPUT_RECEIVED = "Материал получен. Отправьте ещё или нажмите «Структурировать»"

# Button texts
BTN_CREATE = "Создать презентацию"
BTN_STRUCTURE = "Структурировать"
BTN_PREV = "◀️ Назад"
BTN_NEXT = "Вперёд ▶️"
BTN_EDIT = "Редактировать"
BTN_DELETE = "Удалить"
BTN_CONFIRM = "Подтвердить"
BTN_EXPORT_HTML = "Экспорт HTML"
BTN_EXPORT_PDF = "Экспорт PDF"
BTN_BACK = "Назад"
BTN_ADD_SLIDE = "Добавить слайд"
