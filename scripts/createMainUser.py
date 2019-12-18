from backend.models import Users
def run(*args):
    user=Users.objects.create_user(args[0], "Admin",password=args[1])
    user.is_superuser=False
    user.is_staff=False
    user.save()
