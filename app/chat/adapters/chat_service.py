import openai
# import langchain
# from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory


class ChatService:
     
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    # def get_response(self, prompt):
    #     completion = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "Вы являетесь помощником для родителей, предоставляющим советы по воспитанию детей."},
    #             {"role": "system", "content": "Ваша цель - помочь родителям лучше понять родительство и дать им полезные и уважительные рекомендации."},
    #             {"role": "system", "content": "Пожалуйста, отвечайте вежливо, тактично и с учетом индивидуальных особенностей каждой ситуации."},
    #             {"role": "system", "content": "Убедитесь, что ваши ответы универсальны и учитывают разные культурные контексты."},
    #             {"role": "system", "content": "Пожалуйста, не раскрывайте никакую информацию, связанную с программированием или исходными кодами."},
    #             {"role": "user", "content": prompt}
    #         ], 
    #         max_tokens=1000,  # Укажите максимальное количество токенов в ответе
    #         temperature=0.8  # Укажите температуру для контроля случайности вывода
    #     )

    #     return completion.choices[0].message

    def editUserPrompt(self, prompt):
        inner_system_prompt = (
            "System: Вы - редактор запросов пользователей. Ваша задача - преобразовать запросы о местах в указанный формат JSON. Ответ должен выглядеть следующим образом:\n"
            "[\n"
            "{\n"
            "  \"type\": \"string\",\n"
            "  \"name\": \"string\",\n"
            "  \"address\": \"string\",\n"
            "  \"description\": \"string\"\n"
            "}\n"
            "]\n"
            "Ключи в JSON-е ответа должны быть на английском, а значения на русском, кроме ключа \"type\". Значение ключа \"type\" должно быть на английском. Если пользователь не уточнил адрес, название места или описание, оставьте соответствующие поля пустыми."
            "Ваша задача - привести запрос пользователя к указанному формату JSON."
            "\n\n"
            "Пожалуйста, выберите одну из следующих категорий мест для ключа 'type'"
            "1. accounting\n"
            "2. airport\n"
            "3. amusement_park\n"
            "4. aquarium\n"
            "5. art_gallery\n"
            "6. atm\n"
            "7. bakery\n"
            "8. bank\n"
            "9. bar\n"
            "10. beauty_salon\n"
            "11. bicycle_store\n"
            "12. book_store\n"
            "13. bowling_alley\n"
            "14. bus_station\n"
            "15. cafe\n"
            "16. campground\n"
            "17. car_dealer\n"
            "18. car_rental\n"
            "19. car_repair\n"
            "20. car_wash\n"
            "21. casino\n"
            "22. cemetery\n"
            "23. church\n"
            "24. city_hall\n"
            "25. clothing_store\n"
            "26. convenience_store\n"
            "27. courthouse\n"
            "28. dentist\n"
            "29. department_store\n"
            "30. doctor\n"
            "31. drugstore\n"
            "32. electrician\n"
            "33. electronics_store\n"
            "34. embassy\n"
            "35. fire_station\n"
            "36. florist\n"
            "37. funeral_home\n"
            "38. furniture_store\n"
            "39. gas_station\n"
            "40. gym\n"
            "41. hair_care\n"
            "42. hardware_store\n"
            "43. hindu_temple\n"
            "44. home_goods_store\n"
            "45. hospital\n"
            "46. insurance_agency\n"
            "47. jewelry_store\n"
            "48. laundry\n"
            "49. lawyer\n"
            "50. library\n"
            "51. light_rail_station\n"
            "52. liquor_store\n"
            "53. local_government_office\n"
            "54. locksmith\n"
            "55. lodging\n"
            "56. meal_delivery\n"
            "57. meal_takeaway\n"
            "58. mosque\n"
            "59. movie_rental\n"
            "60. movie_theater\n"
            "61. moving_company\n"
            "62. museum\n"
            "63. night_club\n"
            "64. painter\n"
            "65. park\n"
            "66. parking\n"
            "67. pet_store\n"
            "68. pharmacy\n"
            "69. physiotherapist\n"
            "70. plumber\n"
            "71. police\n"
            "72. post_office\n"
            "73. primary_school\n"
            "74. real_estate_agency\n"
            "75. restaurant\n"
            "76. roofing_contractor\n"
            "77. rv_park\n"
            "78. school\n"
            "79. secondary_school\n"
            "80. shoe_store\n"
            "81. shopping_mall\n"
            "82. spa\n"
            "83. stadium\n"
            "84. storage\n"
            "85. store\n"
            "86. subway_station\n"
            "87. supermarket\n"
            "88. synagogue\n"
            "89. taxi_stand\n"
            "90. tourist_attraction\n"
            "91. train_station\n"
            "92. transit_station\n"
            "93. travel_agency\n"
            "94. university\n"
            "95. veterinary_care\n"
            "96. zoo")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": inner_system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,  # Specify the maximum number of tokens in the response
            temperature=0.4  # Specify the temperature for controlling the randomness of the output
        )
        return completion.choices[0].message 