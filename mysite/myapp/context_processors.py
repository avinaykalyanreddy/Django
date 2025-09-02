from users.models import Users


def user_info(request):

    user_id = request.session.get("user_id",1)

    user_obj = Users.objects.filter(id=user_id).first()



    return {"user_id":user_id,"user_obj":user_obj}

