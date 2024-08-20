from loan.models import SystemParameters


def get_system_parameter(name):
    return SystemParameters.objects.get(name=name)
