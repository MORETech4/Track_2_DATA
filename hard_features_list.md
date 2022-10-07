### Сложные features
- Полезная новость — Это вероятно как раз то что мы и должны найти, т.е. скорее целевая функция. Т.е. полезность это реальное соответствие клиента новостям которые он читает, можно получить только из обучающей выборки именно это и должна научиться считать наша модель
- Интересная новость — Один из вариантов можно попробовать по схожести тематик клиента и схожести тематик новости. т.е. создаем 10/50/100 тематик и соотносим каждого клиента с какой-то вероятностью и то же самое делаем для каждой новости. В итоге получается 10/50/100 тематических признаков по новостям + 10/50/100 признаков по клиентам. На основе этого можно еще будет добавить "тематическую популярность": частота появления новости по каждой тематики у клиентов.
- Важная новость — ?? непонятно как считать.
- Локализация: можно схожесть по ключевым словам, например если упоминается название регионов РФ/городов и прочее нижний уровень, если упоминаются федеральные органы или просто Россия то средний уровень, если упоминаются ключевые слова мирового значения (Европа, США, страны, мировая экономика и прочее), тогда верхний уровень.
- Популярность новости - сходу два варианта приходит на ум: 1. это кол-во клиентов которые читают эту новость. 2. Кол-во синонимов этой новости, в случае если несколько источников новостей
- Возрастная принадлежность новости - разбить клиентов на возрастные группы и соответствено определять процентное рапределение возрастных групп для каждой новости.
  Такой же аналог по полу делать не имеет смысл т.к. клиент и так бьется на бинарный м/ж
- Потенциальный размер целевой аудитории: Можно попробовать посчитать потенциал охвата новости, например: "В России вводятся несколько новых дорожных знаков" берем количество водителей в стране и получаем прямой охват в цифрах. Ну т.е. так:  "Потенциальный размер целевой аудитории" ? сколько возможного потенциала у этой новости в принципе? Норм тема, надо подумать как такое посчитать. Там можно подумать над пороговыми значениями, если охват больше какой-то цифры, значит эту новость надо рекомендовать, что-то такое.
ну например есть две три новости про кадровое ведение, про новые правила ПДД и про машинное обучение. Мы понимаем головой что машинное обучение меньший охват, кадры сильно больше, а ПДД так вообще максимальный. Один из вариантов как такое подсчитать, можно ввести искусственные категории (свои, это смотря какие данные будут, может быть там будет явно ограничено кол-во категорий/тематик), т.е. просто вручную вбить веса категориям и тогда задача сведется только к тому чтобы категории новостей определить (а может они и будут даже в датасете).  Норм идея с охватом
- Эмоциональный окрас новости: 
- Информационные всплески. Еще на счет фичей такая идея крутиться. Когда идут информационные всплески по определенной тематике в каком-то  временном сроке (например когда повышают пенсионный возраст всем сразу стали интересны новости по ПФР ну и таких примеров много) . Такое считать тяжело, но в принципе можно было бы по датам новостей искать всплески заинтересованности к определенной тематике. Ну а при прогнозировании просто определять какая тематика сейчас в тренде
 