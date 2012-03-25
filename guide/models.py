from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from guide import settings

GUIDE_JS_TEMPLATE = """$('%(html_selector)s').guide({text:%(text)s,
imagesPath:'%(images_path)s',%(images_settings)s visible:%(visible)d,extra_id:%(id)d,
verticalPosition:'%(vertical_position)s',horizontalPosition:'%(horizontal_position)s'
});"""


class Guide(models.Model):
    VP_TOP, VP_BOTTOM = 0, 1
    VERTICAL_POSITION_CHOICES = (
        (VP_TOP, _("top")),
        (VP_BOTTOM, _("bottom")),
    )
    HP_LEFT, HP_RIGHT = 0, 1
    HORIZONTAL_POSITION_CHOICES = (
        (HP_LEFT, _("left")),
        (HP_RIGHT, _("right"))
    )
    TM_ARROW_AND_CIRCLE, TM_ARROW_ONLY, TM_CIRCLE_ONLY, TM_NO_IMAGES = range(4)
    TIP_MODE_CHOICES = (
        (TM_ARROW_AND_CIRCLE, _("Arrow and circle")),
        (TM_ARROW_ONLY, _("Arrow only")),
        (TM_CIRCLE_ONLY, _("Circle only")),
        (TM_NO_IMAGES, _("No images yet")),
    )
    VM_FOR_ALL, VM_FOR_ANONYMOUS, VM_FOR_AUTHENTICATED = range(3)
    VISIBILITY_MODE_CHOICES = (
        (VM_FOR_ALL, _("For all")),
        (VM_FOR_ANONYMOUS, _("For anonymous users only")),
        (VM_FOR_AUTHENTICATED, _("For authenticated users only")),
    )
    name = models.CharField(_("Name"), max_length=255)
    html_selector = models.CharField(_("HTML selector"), max_length=255)
    guide_text = models.CharField(_("Guide text"), max_length=255, default='', blank=True,
        help_text=_("If the field not set than will be used text from title attribute of HTML object"))
    vertical_position = models.IntegerField(_("Vertical position"),
        choices=VERTICAL_POSITION_CHOICES, default=VP_TOP)
    horizontal_position = models.IntegerField(_("Horizontal position"),
        choices=HORIZONTAL_POSITION_CHOICES, default=HP_LEFT)
    tip_mode = models.IntegerField(_("Tip mode"), choices=TIP_MODE_CHOICES,
        default=TM_ARROW_AND_CIRCLE)
    visibility_mode = models.PositiveSmallIntegerField(_("Visibility mode"),
        choices=VISIBILITY_MODE_CHOICES, default=VM_FOR_ALL)
    who_saw = models.ManyToManyField(User, verbose_name=_("Who saw"), related_name='guide_list',
        help_text=_("Users whom already saw this guide"), blank=True, through='UserGuide')

    GUIDE_IMAGES_SETTINGS_TEMPLATES = {
        TM_ARROW_AND_CIRCLE: "arrowImageName:'%(arrow_image_name)s',highlightImageName:'%(highlight_image_name)s',",
        TM_ARROW_ONLY: "arrowImageName:'%(arrow_image_name)s',highlightImageName:null,",
        TM_CIRCLE_ONLY: "arrowImageName:null,highlightImageName:'%(highlight_image_name)s',",
        TM_NO_IMAGES: "arrowImageName:null,highlightImageName:null,",
    }

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.html_selector)
    
    @property
    def str_vertical_position(self):
        return ['top', 'bottom'][self.vertical_position]

    @property
    def str_horizontal_position(self):
        return ['left', 'right'][self.horizontal_position]

    def render(self, request=None, visible=True):
        images_settings = self.GUIDE_IMAGES_SETTINGS_TEMPLATES[self.tip_mode] % {
                'arrow_image_name': settings.GUIDE_ARROW_IMAGE_NAME,
                'highlight_image_name': settings.GUIDE_HIGHLIGHT_IMAGE_NAME,
                'vertical_position': self.str_vertical_position,
                'horizontal_position': self.str_horizontal_position,
            }
        if callable(settings.GUIDE_IMAGES_URL):
            guide_images_url = settings.GUIDE_IMAGES_URL(request)
        else:
            guide_images_url = settings.GUIDE_IMAGES_URL
        return GUIDE_JS_TEMPLATE % {
            'id': self.pk,
            'html_selector': self.html_selector,
            'text': ("'%s'" % self.guide_text) if self.guide_text else 'null',
            'images_path': guide_images_url,
            'images_settings': images_settings,
            'vertical_position': self.str_vertical_position,
            'horizontal_position': self.str_horizontal_position,
            'visible': 1 if visible else 0,
        }


class UserGuide(models.Model):
    user = models.ForeignKey(User, related_name='saw_guide_list')
    guide = models.ForeignKey(Guide, related_name='saw_user_list')
    views_count = models.PositiveSmallIntegerField(default=1)
