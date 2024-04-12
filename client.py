import requests

## POST-запросы: 

response = requests.post("http://127.0.0.1:5000/user",
                        json={
                            "name": "user_1",
                            "password": "1212"
                        })

# response = requests.post("http://127.0.0.1:5000/user",
#                         json={
#                             "name": "user_2",
#                             "password": "2345"
#                         })

# response = requests.post("http://127.0.0.1:5000/advertisement",
#                         json={
#                             "title": "Куплю автомобиль",
#                             "description": "Нужен автомобиль с небольшим пробегом",
#                             "owner_id": 1
#                         })

# response = requests.post("http://127.0.0.1:5000/advertisement",
#                         json={
#                             "title": "Продам гараж",
#                             "description": "Подходит для хранения велосипедов",
#                             "owner_id": 1
#                         })

# response = requests.post("http://127.0.0.1:5000/advertisement",
#                         json={
#                             "title": "Маникюр",
#                             "description": "Запишитесь на маникюр",
#                             "owner_id": 2
#                         })


## GET-запросы:

# response = requests.get("http://127.0.0.1:5000/user")

# response = requests.get("http://127.0.0.1:5000/user/1")

# response = requests.get("http://127.0.0.1:5000/advertisement/3")


## PATCH-запросы:

# response = requests.patch("http://127.0.0.1:5000/advertisement/3",
#                         json={
#                             "title": "Маникюр и педикюр"
#                         })

# response = requests.patch("http://127.0.0.1:5000/user/2",
#                         json={
#                             "name": "nails_art"
#                         })


## DELETE-запросы:

# response = requests.delete("http://127.0.0.1:5000/advertisement/1")

# response = requests.delete("http://127.0.0.1:5000/user/2")


print(response.status_code)
print(response.text)