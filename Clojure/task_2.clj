;; Задание 2

(ns task-2) ;; namespace для группировки объектов


;; Задание 2.1 оптимизация  мемоизацией
(defn trapezoid-integral
  "Вычисляет интеграл функции f от x до 0 методом трапеций"
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
;; (def F (trapezoid-integral #(* % %)))  ; интеграл x^2
;; (F 1)   ; вычисляет интеграл x^2 dx от 1 до 0
;; (F -1)  ; вычисляет интеграл x^2 dx от -1 до 0



;; Задание 2.2 оптимизация бесконечной последовательности частичных решений
(ns task-2)

(defn trapezoid-integral-seq
  "Вычисляет интеграл функции f от x до 0 используя бесконечную последовательность частичных решений"
  [f]
  (let [make-partial-sums (fn [x steps]
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
              results-seq (lazy-seq
                           (map #(make-partial-sums x %) steps-seq))]
          (swap! cache assoc x results-seq)
          (first results-seq))))))

;; Пример использования:
;; (def F (trapezoid-integral-seq #(* % %)))
;; (F 1)  ; вычисляет интеграл x^2 dx от 1 до 0
;; (F -1) ; вычисляет интеграл x^2 dx от -1 до 0