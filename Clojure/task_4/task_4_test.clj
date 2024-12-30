;; Тесты
(ns task-4-test
  (:require [clojure.test :refer :all]
            [task-4]))  ; Импортируйте пространство имен, которое вы тестируете

(deftest test-constant
  (let [true-const (task-4/TRUE)
        false-const (task-4/FALSE)]
    (is (= (task-4/evaluate true-const nil) true))
    (is (= (task-4/evaluate false-const nil) false))))

(deftest test-variable
  (let [var (task-4/variable :x)]
    (is (= (task-4/evaluate var {:x true}) true))
    (is (= (task-4/evaluate var {:x false}) false))))

(deftest test-not
  (let [var (task-4/variable :x)
        not-var (task-4/not* var)]
    (is (= (task-4/evaluate not-var {:x true}) false))
    (is (= (task-4/evaluate not-var {:x false}) true))))

(deftest test-and
  (let [a (task-4/variable :a)
        b (task-4/variable :b)
        and-expr (task-4/and* a b)]
    (is (= (task-4/evaluate and-expr {:a true :b true}) true))
    (is (= (task-4/evaluate and-expr {:a true :b false}) false))
    (is (= (task-4/evaluate and-expr {:a false :b true}) false))
    (is (= (task-4/evaluate and-expr {:a false :b false}) false))))

(deftest test-or
  (let [a (task-4/variable :a)
        b (task-4/variable :b)
        or-expr (task-4/or* a b)]
    (is (= (task-4/evaluate or-expr {:a true :b true}) true))
    (is (= (task-4/evaluate or-expr {:a true :b false}) true))
    (is (= (task-4/evaluate or-expr {:a false :b true}) true))
    (is (= (task-4/evaluate or-expr {:a false :b false}) false))))

(deftest test-implies
  (let [a (task-4/variable :a)
        b (task-4/variable :b)
        implies-expr (task-4/implies* a b)]
    (is (= (task-4/evaluate implies-expr {:a true :b true}) true))
    (is (= (task-4/evaluate implies-expr {:a true :b false}) false))
    (is (= (task-4/evaluate implies-expr {:a false :b true}) true))
    (is (= (task-4/evaluate implies-expr {:a false :b false}) true))))

(deftest test-substitution
  (let [expr (task-4/implies* (task-4/variable :p) (task-4/and* (task-4/variable :q) (task-4/variable :r)))]
    (is (= (task-4/evaluate (task-4/substitute expr :p false) {:p false :q true :r true}) true))
    (is (= (task-4/evaluate (task-4/substitute expr :q false) {:p true :q false :r true}) false))))

;; Запуск тестов
(run-tests)