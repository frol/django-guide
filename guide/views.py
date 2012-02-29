from misc.json_encode import json_response

from guide import settings
from .models import UserGuide


def toggle_guides(request, status):
    if request.user.is_authenticated():
        if status == 'disable':
            UserGuide.objects.filter(user=request.user,
                    guide__in=request.GET.getlist('guide_list[]'))\
                .update(views_count=(settings.GUIDE_MIN_VIEWS_COUNT + 1))
        else:
            UserGuide.objects.filter(user=request.user,
                    guide__in=request.GET.getlist('guide_list[]'))\
                .update(views_count=1)
    request.session['guide_disabled'] = (status == 'disable')
    return json_response({'status': 'ok'})
