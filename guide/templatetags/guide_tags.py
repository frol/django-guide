from django import template

from guide import settings
from guide.models import Guide, UserGuide


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
    request = context['request']
    if request.user.is_authenticated():
        guide_list = Guide.objects.exclude(visibility_mode=Guide.VM_FOR_ANONYMOUS)
    else:
        guide_list = Guide.objects.exclude(visibility_mode=Guide.VM_FOR_AUTHENTICATED)
    guide_list = guide_list.filter(name__in=request.current_guide_name_list)
    rendered_guide = []
    for guide in guide_list:
        guide_is_visible = False
        if request.user.is_authenticated():
            guide_views = guide.saw_user_list.filter(user=request.user)
            if not guide_views:
                UserGuide.objects.create(guide=guide, user=request.user)
                guide_is_visible = True
            else:
                guide_view = guide_views[0]
                if guide_view.views_count <= settings.GUIDE_MIN_VIEWS_COUNT:
                    guide_view.views_count += 1
                    guide_view.save()
                    guide_is_visible = True
        else:
            if not request.session.get('guide_disabled'):
                guide_is_visible = True
        rendered_guide.append({
            'id': guide.id,
            'js': guide.render(request, visible=guide_is_visible)
        })
    if not rendered_guide:
        return u''
    return u"guide_list = new Array(%s); $(function(){%s $(document).trigger('guide.all_loaded')});" % (
            ','.join(["'%s'" % rg['id'] for rg in rendered_guide]),
            ''.join([rg['js'] for rg in rendered_guide])
        )
