# Fork of [OOTDiffusion](https://github.com/levihsu/OOTDiffusion) with REST API for web app [find-your-style](https://github.com/lruns/find-your-style)
Все про OOTDiffusion можете почитать в их [репозитории](https://github.com/levihsu/OOTDiffusion)
А ради чего этот форк был создан можно посмотреть здесь [find-your-style](https://github.com/lruns/find-your-style).

Самое главное: добавил с помощью библиотеки FastAPI возможность интегрировать веб приложение.

ВАЖНО: ML модели очень большие (занимают как минимум около 30 Гб), нужно учитывать это при установке сервера!
Также при первом запуске будет "прогревка", необходимо будет подождать 10 и более минут (в зависимости от мощности устройства).
И также требуется огромные вычислительные ресурсы...

## Как установить, запустить и как пользоваться

Устанавливаем

```
git clone https://github.com/lruns/OOTDiffusion
cd OOTDiffusion
conda create -n ootd python==3.10
conda activate ootd
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
pip install "uvicorn[standard]"
pip install -r requirements.txt
```

Потом нужно загрузить модели (внимание, они большие!)
```
cd ..
git clone https://huggingface.co/levihsu/OOTDiffusion OOTDiffusionModels
mv ./OOTDiffusionModels/checkpoints ./OOTDiffusion/checkpoints
cd ./OOTDiffusion/checkpoints
git clone https://huggingface.co/openai/clip-vit-large-patch14
cd ..
```

Проверяем что работает (из-за того что в первый раз, будет долго отрабатываться)
```
cd run
python run_ootd.py --model_path ./examples/model/01008_00.jpg --cloth_path ./examples/garment/00055_00.jpg --scale 2.0 --sample 1
```

Запускаем веб сервер (по умолчанию порт 8000)
```
uvicorn web_server:app
```

API состоит из 5 команд: 
- две GET `/api/model/` и `/api/cloth/`, которые выдают список всех названий файлов моделей и одежды
- две GET `/api/model/{filename}` и `/api/cloth/{filename}`, которые позволяют получить изображение модели или одежды
- один POST `/api/try_on/`, который позволяет примерить на определенной модели определенную одежду

Можно API протестировать по ссылке http://127.0.0.1:8000/docs
