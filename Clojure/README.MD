# Начало работы с Clojure

1. Устанавливаем расширение Calva для VS Code
2. Создаем папку для проекта
3. Внутри папки создаем файл deps.edn
4. Внутри файла deps.edn прописываем зависимости

    {:deps {org.clojure/clojure {:mvn/version "1.11.1"}
            org.clojure/clojurescript {:mvn/version "1.11.60"}
            org.clojure/tools.cli {:mvn/version "1.0.219"}}
    :aliases
    {:dev {:extra-deps {org.clojure/tools.namespace {:mvn/version "1.4.4"}}}}}

5. Создаем файл task_1.clj и прописываем код
6. Идем сюда https://clojure.org/guides/getting_started
7. В терминале пишем: brew install clojure/tools/clojure
8. В терминале ставим JAVA: brew install openjdk
9. nano ~/.zshrc – редактируем доступы, добавляем в конец файла 2 строки:
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
export JAVA_HOME="/opt/homebrew/opt/openjdk"
10. Проверяем собственника файла ls -l ~/.zshrc, если там root, 
то делаем sudo chown ваш_юзер:staff ~/.zshrc
11. chmod u+w ~/.zshrc — передаем права на редактирование файла
12. echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zshrc
echo 'export JAVA_HOME="/opt/homebrew/opt/openjdk"' >> ~/.zshrc
13. Проверяем, что java встала: java -version

Когда все уже установлено:
14. Запускаем REPL. В командной строке пишем: clj (в папке проекта!)
15. Если ответ Clojure 1.11.1
                user=>
                То можем подавать на вход переменные, например (+ 1 2)


#Задания по Clojure

1. Базовые операции над структурами данных
Общее условие:
Задан набор символов и число n. Опишите функцию, которая возвращает список всех строк длины n,
состоящих из этих символов и не содержащих двух одинаковых символов, идущих подряд.
Пример:
Для символов 'а', 'b', 'c' и n=2 результат должен быть ("ab" "ac" "ba" "bc" "ca" "cb") с точностью до
перестановки.
1.1. Решите задачу с помощью элементарных операций над последовательностями и рекурсии
1.2. Перепишите программу 1.1. так, чтобы все рекурсивные вызовы были хвостовыми
1.3. Определить функции my-map и my-filter, аналогичные map (для одного списка) и filter, выразив
их через reduce и базовые операции над списками (cons, first, concat и т.п.)
1.4. Решите задачу с помощью элементарных операций над последовательностями и функционалов
map/reduce/filter

