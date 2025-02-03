from .models import Module

def active_modules(request):
    """Add active modules to template context"""
    modules = Module.objects.filter(active=True).order_by('order')
    return {'active_modules': modules} 