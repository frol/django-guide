from django.conf import settings

if 'coffin' in settings.INSTALLED_APPS:
    from jinja2 import nodes, Markup
    from jinja2.ext import Extension
    from coffin.template import Library
    
    from guide.templatetags.guide_tags import AddGuide, render_guides as origin_render_guides

    register = Library()

    class AddGuideExtension(Extension):
        """
        Jinja2-version of the ``render_guides`` tag.
        """

        tags = set(['add_guide'])

        def parse(self, parser):
            lineno = parser.stream.next().lineno
            args = []
            while not parser.stream.current.test('block_end'):
                args.append(parser.parse_expression())
                parser.stream.skip_if('comma')
            return nodes.Output([
                self.call_method('_render', [nodes.Name('request', 'load'), nodes.List(args)]),
            ]).set_lineno(lineno)

        def _render(self, request, args):
            if not hasattr(request, 'current_guide_name_list'):
                request.current_guide_name_list = list()
            for name in args:
                request.current_guide_name_list.append(name)
            return ''


    @register.object
    def render_guides(request):
        return Markup(origin_render_guides({'request': request}))

    register.tag(AddGuideExtension)
