import io
from openpyxl import Workbook


def create_xlsx_from_queryset(queryset: list):
    """
    Утилита для обработки данных и формирования файла xlxs.
    На вход получает список объектов.
    Возвращает файл xlsx через буфер.
    """

    # Создаем множество уникальных моделей роботов,
    # произведенных за последнюю неделю
    modelset = set([robot['model'] for robot in queryset])

    # Создаем файл, удаляем пустой лист.
    workbook = Workbook()
    workbook.remove(workbook.active)

    # В файле генерируем отдельные листы для каждой модели,
    # добавляем первой строкой заголовки для таблицы.
    for sheet in modelset:
        ws = workbook.create_sheet(sheet)
        ws.append(['Модель', 'Версия', 'Количество за неделю'])

    # Для каждого робота в кверисете добавляем его статистику на лист,
    # соответствующий названию модели.
    for robot in queryset:
        for model in modelset:
            if robot['model'] == model:
                row = [robot['model'], robot['version'], robot['counting']]
                ws = workbook[model]
                ws.append(row)

    # Сохраняем файл в буфере и возвращаем.
    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer
