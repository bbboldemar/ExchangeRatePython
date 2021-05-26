# ExchangeRatePython
Crypto to USD via api.twelvedata.com with tkinter GUI

Программа на python с GUI, выполненном при помощи модуля tkinter. Раз в минуту выводит данные о курсе Bitcoin и Siacoin к USD через api от twelvedata.com 
и позволяет настроить email рассылку при превышении задаваемого значения.

'send_email' function:
Must work with 'yandex.ru' with another address and port and doesn't work with 'mail.ru' at all.
For 'google.com' 2-step verification must be disabled, less secure apps must be enabled.

This is my own "Hello World!" to you.

  to do list:
      - api key switcher (def api_request():)
    subscription_settings_window:
      - through cycle
      - email address validation
      - add min price limit function
      - min/max price validation (float)
      - last saved settings button/info
