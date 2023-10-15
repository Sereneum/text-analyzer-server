Загрузите модель в корень проекта  `model-q4_K.gguf`.

```
wget https://huggingface.co/IlyaGusev/saiga2_13b_gguf/resolve/main/model-q4_K.gguf
```

Установите зависимости:
```
pip install llama-cpp-python fire openpyxl flask flask_cors openpyxl git+https://github.com/pdftables/python-pdftables-api.git
```

Запустите проект:

```
python server.py
```
