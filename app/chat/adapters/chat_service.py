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
            "Ваша задача - привести запрос пользователя к указанному формату JSON.")
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