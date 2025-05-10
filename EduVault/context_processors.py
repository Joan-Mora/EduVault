from .models import Profile

def profile_avatar(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(autor=request.user)
        return {'profile': profile}
    return {}
