;; Задание 2

(ns task-2  ; Замените на ваш актуальный неймспейс
  (:require [clojure.test :refer [deftest is testing]]))

(defn simple-trapezoid-integral
   "Вычисляет интеграл функции f от x до 0 методом трапеций (разбиение подграфика на элементы)"
  [f]
  (fn [x]
    (let [steps 1000
          dx (/ (Math/abs x) steps)
          points (if (pos? x)
                   (range x (- dx) (- dx))
                   (range x dx dx))
          result (* (/ dx 2)
                    (+ (f 0)
                       (f x)
                       (* 2 (reduce + (map f (rest (butlast points)))))))]
      result)))

;; Пример использования:
(def F (simple-trapezoid-integral #(* % %))) ; интеграл x^2
;; (F 1)   ; вычисляет интеграл x^2 dx от 1 до 0
;; (F -1)  ; вычисляет интеграл x^2 dx от -1 до 0

;; Задание 2.1 оптимизация  мемоизацией
(defn trapezoid-integral
  "Оптимизация мемоизацией (кеширование)"
  [f]
  (let [steps 1000  ; количество шагов
        cache (atom {})]  ; кэш для мемоизации
    (fn [x]
      (if-let [cached-result (get @cache x)]
        cached-result  ; возвращаем кэшированный результат, если есть
        (let [dx (/ (Math/abs x) steps)  ; шаг интегрирования
              points (if (pos? x)
                       (range x (- dx) (- dx))  ; интегрирование от x до 0
                       (range x dx dx))         ; интегрирование от x до 0
              result (* (/ dx 2)  ; множитель dx/2 для метода трапеций
                        (+ (f 0)    ; первая точка
                           (f x)    ; последняя точка
                           (* 2 (reduce + (map f (rest (butlast points)))))))] ; удвоенная сумма промежуточных точек
          (swap! cache assoc x result)  ; сохраняем результат в кэш
          result)))))

;; Пример использования:
;; (def F (trapezoid-integral #(* % %))) ; интеграл x^2
;; (F 1)   ; вычисляет интеграл x^2 dx от 1 до 0
;; (F -1)  ; вычисляет интеграл x^2 dx от -1 до 0


;; Тест для сравнения производительности до и после оптимизации
(defn performance-comparison-test
  "Сравнение производительности оптимизированной и простой версий"
  []
  (testing "Сравнение производительности оптимизированной и простой версий"
    (let [optimized-f (trapezoid-integral #(* % %))
          simple-f (simple-trapezoid-integral #(* % %))
          x 1.0
          iterations 100

          ;; Замеряем время оптимизированной версии
          optimized-time (time
                          (dotimes [_ iterations]
                            (optimized-f x)))

          ;; Замеряем время простой версии
          simple-time (time
                       (dotimes [_ iterations]
                         (simple-f x)))

          ;; Проверяем, что результаты совпадают
          optimized-result (optimized-f x)
          simple-result (simple-f x)]

      ;; Проверяем точность  
      (is (< (Math/abs (- optimized-result simple-result)) 0.0001)
          "Результаты оптимизированной и простой версий должны совпадать")

      ;; Выводим результаты замеров
      (println "Результаты теста производительности:")
      (println "Оптимизированная версия время:" optimized-time)
      (println "Простая версия время:" simple-time))))

;; Запуск теста
;;(performance-comparison-test)

;; Тест на одиночных вызовах
(let [optimized-f (trapezoid-integral #(* % %))
      simple-f (simple-trapezoid-integral #(* % %))]
  
  (println "Первый вызов оптимизированной версии:")
  (time (optimized-f 1.0))
  
  (println "\nВторой вызов оптимизированной версии (должен быть быстрее):")
  (time (optimized-f 1.0))
  
  (println "\nПервый вызов простой версии:")
  (time (simple-f 1.0))
  
  (println "\nВторой вызов простой версии (такой же медленный):")
  (time (simple-f 1.0))
  )


;;"Первый вызов оптимизированной версии:
;;"Elapsed time: 0.469833 msecs"

;;Второй вызов оптимизированной версии (должен быть быстрее):
;;"Elapsed time: 0.0115 msecs"

;;Первый вызов простой версии:
;;"Elapsed time: 0.230709 msecs"

;;Второй вызов простой версии (такой же медленный):
;;"Elapsed time: 0.159666 msecs"
;;0.33333349999999934"



;; Задание 2.2 оптимизация бесконечной последовательности частичных решений

(defn trapezoid-integral-seq
  "Вычисляет интеграл функции f от x до 0 с бесконечной последовательностью частичных решений"
  [f]
  (let [make-partial-sums (fn [x steps] ;; чем больше на вход подадим шагов, чем точнее
                            (let [dx (/ (Math/abs x) steps)
                                  points (if (pos? x)
                                           (range x (- dx) (- dx))
                                           (range x dx dx))
                                  result (* (/ dx 2)
                                            (+ (f 0)
                                               (f x)
                                               (* 2 (reduce + (map f (rest (butlast points)))))))]
                              result))
        cache (atom {})]  ; кэш для хранения последовательностей
    (fn [x]
      (if-let [cached-seq (get @cache x)]
        (first cached-seq)  ; возвращаем первый элемент кэшированной последовательности
        (let [steps-seq (iterate #(* 2 %) 100)  ; последовательность количества шагов: 100, 200, 400, ...
              results-seq (lazy-seq ;; не вычисляем все сразу, только если нужно
                           (map #(make-partial-sums x %) steps-seq))]
          (swap! cache assoc x results-seq)
          (first results-seq))))))

;; Пример использования:
;; (def F (trapezoid-integral-seq #(* % %)))
;; (F 1)  ; вычисляет интеграл x^2 dx от 1 до 0
;; (F -1) ; вычисляет интеграл x^2 dx от -1 до 0

;; Тест для сравнения производительности трех версий
(deftest performance-comparison-test-2
  (testing "Сравнение производительности трех версий: простой, с мемоизацией и с бесконечной последовательностью"
    (let [simple-f (simple-trapezoid-integral #(* % %))  ; Простая версия
          optimized-f (trapezoid-integral #(* % %))       ; Версия с мемоизацией
          seq-f (trapezoid-integral-seq #(* % %))    ; Версия с бесконечной последовательностью
          x 1.0
          iterations 100
          
          ;; Замеряем время простой версии
          simple-time (time
                        (dotimes [_ iterations]
                          (simple-f x)))
          
          ;; Замеряем время оптимизированной версии
          optimized-time (time
                          (dotimes [_ iterations]
                            (optimized-f x)))
          
          ;; Замеряем время версии с бесконечной последовательностью
          seq-time (time
                     (dotimes [_ iterations]
                       (seq-f x)))
          
          ;; Проверяем, что результаты совпадают
          simple-result (simple-f x)
          optimized-result (optimized-f x)
          seq-result (seq-f x)]
      
      ;; Проверяем точность
      (is (< (Math/abs (- optimized-result simple-result)) 0.0001)
          "Результаты простой и оптимизированной версий должны совпадать")
      (is (< (Math/abs (- seq-result simple-result)) 0.0001)
          "Результаты простой и версии с бесконечной последовательностью должны совпадать")
      
      ;; Выводим результаты замеров
      (println "Результаты теста производительности:")
      (println "Простая версия время:" simple-time)
      (println "Оптимизированная версия время:" optimized-time)
      (println "Версия с бесконечной последовательностью время:" seq-time))))

;; Запуск теста
;; (performance-comparison-test-2)