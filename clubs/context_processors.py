def get_current_user(request):
    current_user = request.user
    return {'current_user': current_user}