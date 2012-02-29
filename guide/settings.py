from django.conf import settings

GUIDE_IMAGES_URL = getattr(settings, 'GUIDE_IMAGES_URL', settings.STATIC_URL + 'img/guide/')
GUIDE_ARROW_IMAGE_NAME = getattr(settings, 'GUIDE_ARROW_IMAGE_NAME', 'arrow')
GUIDE_HIGHLIGHT_IMAGE_NAME = getattr(settings, 'GUIDE_HIGHLIGHT_IMAGE_NAME', 'circle')
GUIDE_MIN_VIEWS_COUNT = getattr(settings, 'GUIDE_MIN_VIEWS_COUNT', 3)
GUIDE_SHOW_ONLY_REGISTERED_GUIDES = getattr(settings, 'GUIDE_SHOW_ONLY_REGISTERED_GUIDES', False)
