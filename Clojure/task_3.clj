;; Задание 3
(ns task-3)

;; Задание 3.1 параллельный вариант filter 

(defn parallel-filter
  [pred coll block-size]
  (let [v (vec coll)
        n (count v)
        num-threads (.. Runtime getRuntime availableProcessors)
        chunk-size (max (quot n num-threads) block-size)
        chunks (partition-all chunk-size (range 0 n))
        process-chunk (fn [indices]
                        (into []
                              (filter pred)
                              (map #(nth v %) indices)))  ; изменили порядок операций
        futures (doall
                 (for [chunk chunks]
                   (future (process-chunk chunk))))]
    (reduce into [] (map deref futures))))

;; Тест производительности
(defn performance-test []
  (let [data (range 1000000)
        pred even?

        ;; Тест обычного filter
        start1 (System/nanoTime)
        result1 (doall (filter pred data))
        time1 (/ (- (System/nanoTime) start1) 1000000.0)

        ;; Тест parallel-filter
        start2 (System/nanoTime)
        result2 (doall (parallel-filter pred data 10000))
        time2 (/ (- (System/nanoTime) start2) 1000000.0)]

    (println "Обычный filter:" time1 "мс")
    (println "Параллельный filter:" time2 "мс")
    (println "Ускорение:" (/ time1 time2) "раз")
    (println "Результаты одинаковы?" (= (vec result1) (vec result2)))))

;; Пример использования:
;; (parallel-filter even? (range 100) 10)
;; (performance-test)


;; Задание 3.2 ленивый параллельный вариант filter 

(defn lazy-parallel-filter
  "Ленивая параллельная версия filter, работающая с бесконечными последовательностями"
  [pred coll block-size]
  (let [process-block (fn [block]
                        (into []
                              (filter pred)
                              block))

        next-chunk (fn [s]
                     (when (seq s)
                       [(take block-size s)
                        (drop block-size s)]))]

    ((fn step [s]
       (lazy-seq
        (when-let [[block rest-seq] (next-chunk s)]
          (let [future-result (future (process-block block))]
            (concat @future-result
                    (step rest-seq))))))
     coll)))

;; Тест производительности
(defn performance-test-lazy []
  (let [data (range 1000000)
        pred even?

        start1 (System/nanoTime)
        result1 (doall (take 1000 (filter pred data)))
        time1 (/ (- (System/nanoTime) start1) 1000000.0)

        start2 (System/nanoTime)
        result2 (doall (take 1000 (lazy-parallel-filter pred data 100)))
        time2 (/ (- (System/nanoTime) start2) 1000000.0)]

    (println "Обычный filter:" time1 "мс")
    (println "Ленивый параллельный filter:" time2 "мс")
    (println "Ускорение:" (/ time1 time2) "раз")
    (println "Результаты одинаковы?" (= result1 result2))))

;; Пример использования с бесконечной последовательностью:
;; (take 10 (lazy-parallel-filter even? (iterate inc 0)))