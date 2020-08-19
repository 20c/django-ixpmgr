# Mostly ripped from jea.api.v2.errors.problem_factory.py in ix-api-sandbox-v2

import inspect
import json

from django.core import exceptions as django_exceptions
from django.http import Http404, HttpResponseNotFound
from django.http import response as http_response

from rest_framework import status, exceptions as rest_exceptions
from rest_framework.views import exception_handler as rest_exception_handler

from ixapi_schema.v2.entities import problems


DJANGO_EXCEPTIONS =  (
    Http404,
) + tuple(
    cls for (_, cls) in inspect.getmembers(django_exceptions, inspect.isclass)
)


def handle_exception(exc, context):
    problem = make_problem(exc)
    serializer = problems.ProblemResponse(problem)
    return http_response.JsonResponse(
        serializer.data, status=problem.response_status)

def generic404(request, exception):
    return handle_exception(exception, None)


def make_problem(obj):
    "Convert an exception to an IX-API problem"

    if isinstance(obj, rest_exceptions.APIException):
        return _make_problem_from_api_exception(obj)
    if isinstance(obj, DJANGO_EXCEPTIONS):
        return _make_problem_from_django_exception(obj)
    if isinstance(obj, Exception):
        return _make_problem_from_exception(obj)

    return problems.ServerErrorProblem()


def _get_problem_class(exception):
    """
    Get the problem class for a given exception.
    If no such class could be found, fall back to
    an empty problem.

    :param exception: The exception object
    """
    if isinstance(exception, rest_exceptions.AuthenticationFailed):
        return problems.AuthenticationProblem

    # Try to derive problem class from name
    if inspect.isclass(exception):
        cls = exception
    else:
        cls = exception.__class__

    if cls == object: # We are all the way down
        return problems.ServerErrorProblem

    name = cls.__name__
    problem_name = f"{name}Problem"

    # Try to get the corresponding problem class
    problem_class = getattr(problems, problem_name, None)
    if not problem_class:
        problem_class = _get_problem_class(cls.__base__)

    return problem_class


def _make_problem_from_api_exception(api_exception):
    """
    We have a rest framework api exception.
    Let's make a problem out of it.
    """
    problem_class = _get_problem_class(api_exception)

    # if api_exception.detail and isinstance(api_exception.detail, list):
    #     detail = str(api_exception.detail[0])
    # elif api_exception.detail:
    #     detail = str(api_exception.detail)
    # else:
    #     detail = None

    detail = None
    if api_exception.detail:
        detail = api_exception.detail

    # Fill in the details from the original object
    problem = problem_class(
        detail=detail,
        response_status=api_exception.status_code)

    return problem


def _make_problem_from_django_exception(exception):
    """
    Make problem from django exception
    """
    problem_class = _get_problem_class(exception)
    if isinstance(exception, (Http404, django_exceptions.ObjectDoesNotExist)):
        problem_class = problems.NotFoundProblem

    # Get the detail, if there is any. Otherwise make explicit none.
    # detail = str(exception)
    # if not detail:
    #     detail = None
    detail = exception

    problem = problem_class(detail=detail)
    return problem


def _make_problem_from_exception(obj):
    """
    Try to make an exception from any object
    """
    problem_class = _get_problem_class(obj)
    try:
        title = problem_class.default_title
        if problem_class == problems.Problem:
            title = obj.__class__.__name__

        detail = str(obj)
        if not detail:
            detail = None
        return problem_class(title=title, detail=detail)
    except:
        return problems.ServerErrorProblem()
