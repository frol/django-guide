from django import template
from django.db.models import F

from guide import settings
from guide.models import Guide, UserGuide
from guide.settings import GUIDE_SHOW_ONLY_REGISTERED_GUIDES


register = template.Library()

@register.tag
def add_guide(parser, token):
    return AddGuide(token.split_contents()[1:])


class AddGuide(template.Node):
    def __init__(self, names):
        self.names = [template.Variable(name) for name in names]

    def render(self, context):
        if not hasattr(context['request'], 'current_guide_name_list'):
            context['request'].current_guide_name_list = list()
        for name_key in self.names:
            name = name_key.resolve(context)
            context['request'].current_guide_name_list.append(name)
        return u''


@register.simple_tag(takes_context=True)
def render_guides(context):
    """
    Render JS code of guides.
    """
    request = context['request']
    if request.user.is_authenticated():
        guide_list = Guide.objects.exclude(visibility_mode=Guide.VM_FOR_ANONYMOUS)
    else:
        guide_list = Guide.objects.exclude(visibility_mode=Guide.VM_FOR_AUTHENTICATED)
    if GUIDE_SHOW_ONLY_REGISTERED_GUIDES:
        guide_list = guide_list.filter(name__in=request.current_guide_name_list)
    else:
        guide_list = guide_list.all()

    if not guide_list:
        return u''

    # If user is authenticated need update views_count for visible guides
    if request.user.is_authenticated():
        guide_views = UserGuide.objects.filter(user=request.user,
                guide__in=[item.pk for item in guide_list]
            ).values_list('id', 'guide_id', 'views_count')
        guide_views_visible_pk = [pk for pk, guide_id, views_count in guide_views
                if views_count < settings.GUIDE_MIN_VIEWS_COUNT
            ]
        # Update only if any visible guide
        if guide_views_visible_pk:
            UserGuide.objects.filter(id__in=guide_views_visible_pk)\
                .update(views_count=F('views_count') + 1)
        guide_views = {guide_id: views_count for pk, guide_id, views_count in guide_views}

    # Render JS blocks
    rendered_guide = []
    for guide in guide_list:
        # Decide which guides will be visible
        guide_is_visible = False
        if request.user.is_authenticated():
            if guide.pk not in guide_views:
                UserGuide.objects.create(guide=guide, user=request.user)
                guide_is_visible = True
            elif guide_views[guide.pk] < settings.GUIDE_MIN_VIEWS_COUNT:
                guide_is_visible = True
        elif not request.session.get('guide_disabled'):
            guide_is_visible = True
        rendered_guide.append({
            'id': guide.pk,
            'js': guide.render(request, visible=guide_is_visible)
        })

    # Render final js
    return u"guide_list = new Array(%s); $(function(){%s $(document).trigger('guide.all_loaded')});" % (
            ','.join(["'%s'" % rg['id'] for rg in rendered_guide]),
            ''.join([rg['js'] for rg in rendered_guide])
        )
