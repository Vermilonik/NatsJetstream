# NatsJetStream

в этом репозитории примеры работы с NATSJetStream. используется библиотека nats-py

в каждой директории есть свой main.py, requirements.txt и свой server.conf . тебе остается только подставить токен своего бота и можешь запускать код

чтоб скачать все библиотеки, что используются в коде, и потом его запустить, нужно написать:
```
pip install -r requirements.txt
python main.py
```

чтоб запустить натс сервер нужно написать:
```
nats-server -c server.conf 
```

мануал по скачиванию nats, и настройке: https://github.com/Vermilonik/HowCreateStreamAndConsumerNats

наш чат по nats: https://t.me/nats_py
