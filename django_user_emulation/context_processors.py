def emulation(request):
    # inject is_emulating variable into every template
    emulating = request.session.get('is_emulating', False)

    return {'is_emulating': emulating}
