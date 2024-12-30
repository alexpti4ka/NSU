;; Задание 3
(ns task-3)

(defn simple-filter
  "Обычная функция фильтрации, которая возвращает элементы, удовлетворяющие предикату."
  [pred coll]
  (reduce
   (fn [acc item]
     (if (pred item)
       (conj acc item)  ; Добавляем элемент в аккумулятор, если он удовлетворяет предикату
       acc))            ; Иначе просто возвращаем аккумулятор
   []                  ; Начальное значение - пустой вектор
   coll))              ; Коллекция для фильтрации

;; Определяем предикат
(defn is-even? [n]
  (even? n))

;; Исходная коллекция
(def numbers (range 10))  ; [0 1 2 3 4 5 6 7 8 9]

;; Фильтрация с использованием обычной функции
(def even-numbers (simple-filter is-even? numbers))

;; Выводим результат
(println "Четные числа:" even-numbers)


;; Задание 3.1 параллельный вариант filter 

(defn parallel-filter
  [pred coll block-size] ;; берем на вход предикат для фильтра, коллекцию, размер блока д обработки
  (let [v (vec coll) ;; создаем вектор д коллекции
        n (count v) ;; считаем кол-во элементов
        num-threads (.. Runtime getRuntime availableProcessors) ;; смотрим доступные процессоры
        chunk-size (max (quot n num-threads) block-size) ;; считаем оптим размер блока
        chunks (partition-all chunk-size (range 0 n)) ;; последоваиельность индексов 0-n
        process-chunk (fn [indices]
                        (into [] ;; собираем обработанные данные в новый вектор
                              (filter pred) ;; фильтруем
                              (map #(nth v %) indices)))  ; изменили порядок операций
        futures (doall ;; создаем потоки и выполняем все
                 (for [chunk chunks] ;; для каждой последовательности
                   (future (process-chunk chunk))))]
    (reduce into [] (map deref futures)))) ;; из всех потоков собираем один вектор


;; Тестирование производительности
(defn performance-comparison []
  (let [pred even?  ; Предикат для фильтрации
        numbers (range 1000000)]  ; Исходная коллекция с 1 миллионом элементов

    ;; Замеряем время обычной фильтрации
    (println "Тестирование обычной фильтрации...")
    (let [simple-time (time (simple-filter pred numbers))]
      (println "Обычная фильтрация завершена."))

    ;; Замеряем время параллельной фильтрации
    (println "Тестирование параллельной фильтрации...")
    (let [parallel-time (time (parallel-filter pred numbers 10000))]
      (println "Параллельная фильтрация завершена."))

    ;; Выводим результаты
    (println "Тест завершен.")))

;; Запуск теста
(performance-comparison)
;; Если количество элементов в коллекции не очень велико, расходы 
;; на создание потоков могут превышать преимущества от параллельной обработки


;; Задание 3.2 ленивый параллельный вариант filter 

(defn lazy-parallel-filter
  "Ленивая параллельная версия filter, работающая с бесконечными последовательностями"
  [pred coll block-size] ;; на вход берет аналогичный набор
  (let [process-block (fn [block] ;; обрабатываем блоки по одному
                        (into []
                              (filter pred)
                              block))

        next-chunk (fn [s] ;; разбивает входящую последовательность на блоки
                     (when (seq s)
                       [(take block-size s)
                        (drop block-size s)]))]

    ((fn step [s] ;; ленивая рекурсия
       (lazy-seq ;; возвращаеь элементы по мере необходимости
        (when-let [[block rest-seq] (next-chunk s)] ;; есть ли след блок?
          (let [future-result (future (process-block block))] ;; обрабатываем соседа отдельным потоком
            (concat @future-result ;; склеивает потоки обратно
                    (step rest-seq))))))
     coll)))

;; Тест производительности
(defn performance-test-lazy []
  (let [data (range 1000000)  ; Исходная коллекция с 1 миллионом элементов
        pred even?            ; Предикат для фильтрации – лучше использовать свой, сон на 10 м-сек

        ;; Замер времени для обычной фильтрации
        start1 (System/nanoTime)
        result1 (doall (take 1000 (filter pred data)))  ; Фильтрация с использованием simple-filter
        time1 (/ (- (System/nanoTime) start1) 1000000.0)

        ;; Замер времени для ленивой параллельной фильтрации
        start2 (System/nanoTime)
        result2 (doall (take 1000 (lazy-parallel-filter pred data 100)))  ; Фильтрация с использованием lazy-parallel-filter
        time2 (/ (- (System/nanoTime) start2) 1000000.0)]

    ;; Вывод результатов
    (println "Обычный filter:" time1 "мс")
    (println "Ленивый параллельный filter:" time2 "мс")
    (println "Ускорение:" (/ time1 time2) "раз")
    (println "Результаты одинаковы?" (= result1 result2))))  ; Проверка на равенство результатов

;; Запуск теста
(performance-test-lazy)

