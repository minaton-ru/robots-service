import json
import io
from datetime import timedelta
from openpyxl import Workbook

from django.utils import timezone
from django.db.models import Count
from django.views.generic import CreateView, ListView
from django.http import HttpResponse, FileResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, RequestAborted
from django.core.exceptions import EmptyResultSet

from .models import Robot


@method_decorator(csrf_exempt, name="dispatch")
class RobotCreateView(CreateView):
    """
    API endpoint принимает POST-запрос, клиент должен быть авторизован.
    При успешной валидации данных создает новую запись в базе данных
    и возвращает 201 CREATED.
    При ошибке в полученных данных возвращает 400 Bad Request.
    При получении GET-запроса возращает 403 Forbidden.
    """

    def get(self, request):
        return HttpResponse("GET request is not supported",
                            status=403, headers={"Allow": "POST"})

    def post(self, request) -> HttpResponse:
        data = json.loads(request.body)

        # Проверяем, что в запросе есть все необходимые данные.
        # Если нет, возвращаем ошибку.
        if data.get("model") and data.get("version") and data.get("created"):
            robot_model = data.get("model")
            robot_version = data.get("version")
            robot_created = data.get("created")
        else:
            return HttpResponse("Missing requirement data in request",
                                status=400)

        robot_data = {
            'serial': "-".join((robot_model, robot_version)),
            'model': robot_model,
            'version': robot_version,
            'created': robot_created,
        }

        # Создаем инстанс и валидируем данные модели методом full_clean.
        # Если валидация не прошла, возращаем ошибку.
        new_robot = Robot(**robot_data)
        try:
            new_robot.full_clean()
            new_robot.save()
            return HttpResponse("New robot successfully created", status=201)
        except ValidationError:
            return HttpResponse("Validation error", status=400)


class LastWeekExportView(ListView):
    """
    Генерирует и возвращает xlsx-файл с отчетом
    о производстве роботов за последнюю неделю.

    """
    def get(self, request):

        # Создаем кверисет: объекты сгруппированы по модели и версии,
        # добавлено количество,
        # отфильтрованы по дате создания семи дней (включая сегодняшний).
        week_ago = timezone.now() - timedelta(days=6)
        queryset = (
            Robot.objects.filter(created__gte=week_ago)
            .values("model", "version")
            .annotate(counting=Count("id"))
            .order_by("model")
        )

        if not queryset:
            raise EmptyResultSet("No new robots")

        # Создаем множество уникальных моделей роботов,
        # произведенных за последнюю неделю
        modelset = set([robot['model'] for robot in queryset])

        # Создаем пустой файл, удаляем пустой лист.
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

        # Если ошибок нет, сохраняем файл в буфер и возвращаем.
        try:
            buffer = io.BytesIO()
            workbook.save(buffer)
            buffer.seek(0)
            filename = f'week-report-{timezone.now().strftime("%Y-%m-%d")}.xlsx'  # noqa: E501
            return FileResponse(buffer, as_attachment=True, filename=filename)
        except RequestAborted:
            return HttpResponse("Error during creating XLSX file", status=500)
