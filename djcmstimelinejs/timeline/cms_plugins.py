from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from models import *

class HelloPlugin(CMSPluginBase):
    model = CMSPlugin
#    model = News
    name = _("Timeline Plugin")
    render_template = "timeline_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance,
                        'categories': Category.objects.all()})
        return context


plugin_pool.register_plugin(HelloPlugin)
