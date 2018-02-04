def current_user(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    return {'user': user}