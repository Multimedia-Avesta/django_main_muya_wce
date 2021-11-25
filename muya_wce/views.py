from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from celery.result import AsyncResult


def get_login_status(request):
    if request.user.is_authenticated:
        return request.user.username
    else:
        return None


def main_page(request):
    login_details = get_login_status(request)
    data = {'page_title': 'The MUYA Workspace for Collaborate Editing',
            'login_status': login_details}
    return render(request, 'index.html', data)


def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    if 'next' in request.GET:
        next_location = request.GET.get('next')
    else:
        next_location = '/'
    return HttpResponseRedirect(next_location)


def poll_state(request):
    """
    check the current state of a task
    """
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            if task.state == 'FAILURE':
                print(repr(task.result))
                print(str(task.result))
                message_string = '{}: {}'.format(task.result.__class__.__name__, ', '.join(list(task.result.args)))
                context = {'result': message_string, 'state': task.state}
            else:
                context = {'result': task.result, 'state': task.state}
        else:
            context = {'result': 'No task_id in the request', 'state': 'FAILURE'}
    else:
        context = {'result': 'This is not an ajax request', 'state': 'FAILURE'}

    return JsonResponse(context)
