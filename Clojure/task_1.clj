;; Задание 1

(ns task-1) ;; namespace для группировки объектов

;; Задание 1.2 (последовательности + рекурсия)
(defn generate-strings
  "Возвращает список всех строк длины n,
состоящих из этих символов и не содержащих двух одинаковых символов, идущих подряд"
  [chars n] ;; ф-я принимает последовательность символов и число n
  (letfn [(generate [current-str remaining-len] ;; рекурсивная генерация строк
            (if (zero? remaining-len) ;; если осталось 0 символов, то возвращаем текущую строку
              [current-str] ;; возвращаем список с текущей строкой
              (mapcat ;; применяем ф-ю ко всем элементам
               (fn [c] ;; для каждого символа
                 (when (not= c (last current-str)) ;; если символ не равен последнему символу текущей строки
                   (generate (str current-str c) (dec remaining-len)))) ;; рекурсивно вызываем ф-ю с новой строкой и уменьшенным количеством символов
               chars)))] ;; последовательность символов
    (generate "" n))) ;; вызываем рекурсивную ф-ю с пустой строкой и числом n

;; Пример использования
;; clj
;; (load-file "/Users/alexpti4ka/Documents/Cursor_projects/Clojure/task_1.clj")
;; (task-1/generate-strings [\a \b \c] 2)

;; (ns task-1)  – переключение на верный namespace
;; (def result (generate-strings [\a \b \c] 2)) 
;; генерируем строки длины 2 из символов 'a', 'b', 'c'
;; (println "Result:" result) ;; выводим результат

;; для выхода из ошибки Ctrl + D


(ns task-1)
;; Задание 1.2 (хвостовая рекурсия)
;; не переполняет стек, выполняется быстрее
(defn generate-strings-tail
  "Та же функция, но с хвостовой рекурсией"
  [chars n]
  (letfn [(generate [current-str remaining-len acc] 
            (if (zero? remaining-len)
              (conj acc current-str) ;; аккумулятор для сбора результатов
              (reduce
               (fn [new-acc c]
                 (if (not= c (last current-str))
                   (generate (str current-str c)
                             (dec remaining-len)
                             new-acc) 
                   new-acc))
               acc
               chars)))]
    (generate "" n #{}))) ;; Результаты собираются в множество (#{}) вместо списка

;; Для проверки может понадобится еще раз перегрузить файл и обозначить пространство имен
;; Перезагрузим файл
;;(load-file "/Users/alexpti4ka/Documents/Cursor_projects/Clojure/task_1.clj")

;; Переключимся в пространство имен
;;(ns task-1)

;; Для сравнения результатов
;;(= (set (generate-strings [\a \b \c] 2))
;;   (generate-strings-tail [\a \b \c] 2))


;; Задание 1.3 — reduce и базовые операции над списками (cons, first, concat)
(ns task-1)

;; my-map: применяет функцию f к каждому элементу списка
(defn my-map ;; «разметка», те хотим применять ф-ю ко всем элементам
  [f coll] ;; на вход ф-я и коллекция (параметры)
  (reduce ;; применяет ф-ю из аргумента ко всем эл. кол.
   (fn [acc item] ;; храним промежут результаты
     (concat acc [(f item)])) ; добавляем результат применения функции f к текущему элементу
   [] ; начальное значение - пустой вектор
   coll))

;; my-filter: оставляет только элементы, удовлетворяющие предикату pred
(defn my-filter
  [pred coll] ;; pred - это ф-я предикат (bool) 
  (reduce
   (fn [acc item]
     (if (pred item)
       (concat acc [item]) ; если элемент удовлетворяет предикату, добавляем его
       acc)) ; иначе пропускаем
   [] ; начальное значение - пустой вектор
   coll))

;; Примеры использования:
;; (my-map inc [1 2 3 4 5])  ; => [2 3 4 5 6]
;; (my-filter even? [1 2 3 4 5])  ; => [2 4]

;; Задание 1.4 — операции над последовательностями + map/reduce/filter
(ns task-1)


(defn generate-strings-functional 
    "Возвращает список всех строк длины n, состоящих из заданных символов 
     и не содержащих двух одинаковых символов подряд, используя map/reduce/filter"
  [chars n]
  (reduce
   (fn [acc _]
     (vec
      (mapcat (fn [s]
                (map #(str s %)
                     (filter #(not= % (last s)) chars)))
              acc)))
   [""]
   (range n)))


;; Пример использования:
;; (generate-strings-functional [\a \b \c] 2)
;; => ["ab" "ac" "ba" "bc" "ca" "cb"]

