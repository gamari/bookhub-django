from django.shortcuts import render


class BaseViewMixin(object):
    def render_error(self, message, template_name, **context):
        context['error_message'] = message
        return render(self.request, template_name, context)

    def _get_context_for_error(self, **kwargs):
        raise NotImplementedError("実装してください")

