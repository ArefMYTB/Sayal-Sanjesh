from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result
from SayalSanjesh.models import Cities
from Authorization.Serializers.AdminsSerializer import AdminsSerializer


class citiesSerializer:

    @staticmethod
    def admin_create_city_serializer(token, city_name, city_state):
        """
            param : [token, city_name, city_state]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """

        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Base'):
                try:
                    Cities.objects.create(admin_id=admin_id, city_name=city_name, city_state=city_state)
                except:
                    wrong_data_result["farsi_message"] = "نام شهر باید منحصر به فرد باشد"
                    wrong_data_result["english_message"] = "city name must be unique"
                    return False, wrong_data_result

                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_city_serializer(token, city_id, city_name, city_state):
        """
            param : [token, city_id, city_name, city_state]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Base'):
                try:
                    city = Cities.objects.get(city_id=city_id)
                    city.admin.admin_id = admin_id
                    city.city_name = city_name
                    city.city_state = city_state
                    city.save()
                except:
                    wrong_data_result["farsi_message"] = "city_id اشتباه است"
                    wrong_data_result["english_message"] = "city_id is incorrect"
                    return False, wrong_data_result

                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_delete_city_serializer(token, city_id):
        """
            param : [token, city_id]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Base'):
                try:
                    city = Cities.objects.get(city_id=city_id)
                    city.delete()
                except:
                    wrong_data_result["farsi_message"] = "city_id اشتباه است"
                    wrong_data_result["english_message"] = "city_id is incorrect"
                    return False, wrong_data_result

                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_cities_serializer(token, page, count, city_name, city_state):
        """
            param : [token, page, count, city_name, city_state]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Base'):
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "city_name": city_name,
                    "city_state": city_state
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                try:
                    cities = Cities.objects.filter(**filters)
                    cities_pagination = cities.order_by('city_create_date')[offset:offset + limit]
                except:
                    wrong_data_result["farsi_message"] = "داده های ورودی را چک کنید"
                    wrong_data_result["english_message"] = "Check the input data"
                    return False, wrong_data_result
                all_cities_count = cities.count()
                cities_list = []
                for city in cities_pagination:
                    city = city.as_dict()
                    city['all_cities_count'] = all_cities_count
                    cities_list.append(city)
                return True, cities_list
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_city_serializer(token, city_id):
        """
            param : [token, city_id]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Base'):

                try:
                    city = Cities.objects.get(city_id=city_id)
                except:
                    wrong_data_result["farsi_message"] = "city_id اشتباه است"
                    wrong_data_result["english_message"] = "city_id is incorrect"
                    return False, wrong_data_result
                city = city.as_dict()
                return True, city
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
