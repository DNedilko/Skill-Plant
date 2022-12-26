# Skill-Plant
 Презентація проєкту - [link](https://docs.google.com/presentation/d/1RVYhiMTWDP2VtgzYNJEAJ8LeId5X-8dsszX8_cL5Yd0/edit#slide=id.p)
 
 GitHub репозиторій - [link](https://github.com/ViktoriiaHudym/Skill-Plant)

## Простими словами про важливі речі 🙌
    
**Парсинг даних**

Є загальна логіка, за якою відбувається парсинг даних. Виконуються http методи (post або get) вони отримують код веб сторінки (html дерево), і потім за цим деревом відбувається пошук потрібних тегів (тег з датою, назвою вакансії, регіон вакансії і тд).
Для кожного сайту реалізовано свій лоадер, його задача полягає у парсингу даних. Використано технології багатопотоку, щоб пришвидшити збір даних.
В мультипотоці запускається дві функції. Перша - яка, збирає усі посилання на вакансії. Друга - яка, збирає дані з самої сторінки вакансії.
Після ідентифікації, створюється словник та повертається кінцевою функцією. На виході отримуємо Json файл.

**Передаємо дані в Kafka**

Передаємо дані в Kafka Producer, який в свою чергу надсилає дані в Topic. Одночасно декілька Kafka Producer можуть надсилати дані в Topic. Після цього дані передаються в Consumer, з якого той в починає забирати дані по черзі.

**А якщо у нас вже є така вакансія?**

Отримавши дані з Consumer, перевіряємо чи є вакансія дублікатом. Якщо за параметрами назва, локація, роботодавець, країна, посада подібна вакансія вже є в БД, ми не запишемо її.

**Запис даних в БД**

Запис даних в БД реалізований за допомогою psycopg2. Реалізовується черга, яка записує дані з Json. Детaльнiше можна глянути у ***Database/DatabaseProxy.py***

**Препроцесінг даних**

Окрім того, що ми парсимо багато полів напряму з сайту. Description  слугує джерелом для виділення Hard&Soft Skills, що у подальшому записуються у БД. Дані зберігаються у таблицю з назвою skillplant_data.

Kafka працює як черга. (Поки одна вакансія не перевіриться на дублікат, пройде препроцесінг, та не запишеться у БД, робота з наступною вакансією не розпочнеться).

**Докер**

Щоб запустити докер та розгорнути контейнери з сервісами, використай команду:
  ```python
# to build app
docker-compose up -d
# or - shows all the information in terminal
docker-compose up
  ```
основні команди роботи з докером та пояснення їхньої роботи можна знайти у файлі ***commands.txt***

**Jupyter Notebook**

	Для отримання доступу у ноутбук є два сценарії:
+ якщо у вас є десктопна версія docker, то після запуску команди docker-compose up -d(у терміналі) у додатку docker з'являться контейнери з кожним з сервісів, що було передзавантажено. В самому низу контейнер файлу “datascience-notebook-container” можна знайти посилання на ноутбук. 
+ якщо ж у вас немає додатку, то перший раз розгортати систему треба командою docker-compose up, тоді у вас в терміналі буде відображено увесь процес розгортання системи. Посилання на ноутбук буде знаходитися серед цих повідомлень.

	Щоб під'єднатися треба лише вставити посилання у ваш пошуковик або просто клікнути на нього.
	В ноутбуці вже встановлений pip, тож проблем з завантаженням потрібних вам для подальшої роботи бібліотек бути не повинною

**Крони**
Реалізовані для автоматизованого запуску відпрацювання скриптів скрапінгу даних та їхньої обробки. 





## Покрокова інструкція 🤌

**Крок 1.** Git clone репозиторію

**Крок 2.** Розгони систему за допомогою команд docker-compose up або docker-compose up -d

**Крок 3.** Встанови requirements командою pip install -r requirements.txt 
Перед тим як запускати проєкт, варто встановити усі requirements, вони є у файлі ***requirements.txt. 

**Крок 4.** Запуск лоадерів та проксі з терміналу:
```python
python ./scripts/djinni.co/djinni.co.py
python ./scripts/rabota.ua/rabota.ua.py
python ./scripts/work.ua/work.ua.py
python ./Database/DatabaseProxy.py

```
**Крок 5.** Щоб переглядати завантажені дані здійсність підключення до БД - пароль, користувача та назву можна знайти у файлі docker-compose.yml. 
Якщо ви усе зробили правильно, то побачите підключення до БД та табличку, у яку вже почали запсуватися дані.

**Крок 6.** Щоб відкрити Jupyter, скопіюйте посилання у вашому Docker додатку або у терміналі, якщо ви запускали систему командою docker-compose up

**Крок 7.** Підключайся до БД з jupyter notebook та працюй з даними!

Щоб почитати цей гайд з картинками перейдіть за [посиланням](https://docs.google.com/document/d/13UaltWiAEUJr98ad9ps3Upz_JQrmOdPwzY3piguUzCA/edit)


