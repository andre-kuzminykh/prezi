"""Text constants for bot messages (Russian).

## Traceability
Component: Core / Vocabulary
"""

WELCOME = (
    "Добро пожаловать в <b>AI Presentation Builder</b>!\n"
    "Я помогу вам создать презентацию из текста или голосового сообщения."
)

CREATE_PROMPT = "Отправьте текст или голосовое сообщение с описанием презентации."

STRUCTURING = "⏳ Структурирую презентацию..."

SLIDE_TEMPLATE = (
    "📑 <b>Слайд {index}/{total}</b>\n\n"
    "<b>{title}</b>\n\n"
    "{text}\n\n"
    "🎨 <i>Визуал: {visual_description}</i>"
)

EDIT_PROMPT = "✏️ Отправьте команду редактирования текстом или голосом"

EXPORT_READY = "Ваша презентация готова! 🎉"

ERROR = "❌ Произошла ошибка: {error}"

NO_SLIDES = "Нет слайдов для отображения."

PRESENTATION_CREATED = "Презентация создана! Отправляйте материал текстом или голосом."

INPUT_RECEIVED = "✅ Материал получен. Отправьте ещё или нажмите «Структурировать»"

GENERATING_PDF = "⏳ Генерирую PDF..."

# Button texts
BTN_CREATE = "🎯 Создать презентацию"
BTN_STRUCTURE = "🔮 Структурировать"
BTN_PREV = "◀️"
BTN_NEXT = "▶️"
BTN_INACTIVE = "·"
BTN_EDIT = "✏️ Редактировать"
BTN_DONE = "✅ Далее"
