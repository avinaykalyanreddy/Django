
def logged_in_user(request):

    user_id = request.session.get("user_id")

    try:

        from .models import UserDetails

        user = UserDetails.objects.filter(id=user_id).first()

        return {"logged_in_user":user}
    except:
         return {"logged_in_user":None}