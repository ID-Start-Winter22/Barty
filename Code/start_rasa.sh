# rasa run --cors "*" --enable-api & rasa run actions &
screen -S rasa -d -m rasa run --cors "*" --enable-api --debug
screen -S rasa-actions -d -m rasa run actions
