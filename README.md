# template

`example.txt` - хранится анализируемая статья

`template.docx` - файл-шаблон. лежит где и запускаемый файл. в нем должно быть пять тегов: `#text1#`, `#text2#`, `#text3#`, `#text4#`, `#text5#`. Они заменяются на сгенерированные LLM сообщения

`clear template.docx` - исходный файл-шаблон. Для очередного запуска template.docx нужно удалить и создать из копии `clear template.docx`.
