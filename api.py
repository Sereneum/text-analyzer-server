import fire
from llama_cpp import Llama

SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."
# SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им. твоя задача - это проверять на корректность наименование единицы имерения. первым словом в твоем ответе должен быть ответ на вопрос в формате да/нет. вопросы начались. отвечай только на них."
SYSTEM_TOKEN = 1788
USER_TOKEN = 1404
BOT_TOKEN = 9225
LINEBREAK_TOKEN = 13
tokens = []

ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}


def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model):
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    return get_message_tokens(model, **system_message)


model = Llama(model_path='model-q4_K.gguf', n_ctx=2000, n_parts=1)
system_tokens = get_system_tokens(model)
tokens += system_tokens
model.eval(tokens)


def interact_with_bot(model, user_message):
    global tokens

    message_tokens = get_message_tokens(model, "user", user_message)
    role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
    tokens += message_tokens + role_tokens

    generator = model.generate(
        tokens,
        top_k=30,
        top_p=0.9,
        temp=0.2,
        repeat_penalty=1.1
    )

    bot_response = ""

    for token in generator:
        token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
        tokens.append(token)
        if token == model.token_eos():
            break
        bot_response += token_str

    return bot_response


def ask_question(user_question):
    response = interact_with_bot(model, user_question)
    return response


# user_question = "твоя задача - это проверять на корректность наименование единицы имерения. первым словом в твоем ответе должен быть ответ на вопрос в формате да/нет. вопросы начались. отвечай только на них. может ли наименование единицы измерения быть: тысяча штук?"
# bot_answer, tokens = interact_with_bot(model, tokens, user_question)
#
# print("User:", user_question)
# print(bot_answer)
