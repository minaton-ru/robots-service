import json

from django.views.generic import CreateView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

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
