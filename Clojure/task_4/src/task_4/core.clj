;; Задание 4
(ns core
  (:require [clojure.test :refer :all]))

;; 1. Сначала определяем протокол
(defprotocol BooleanExpression ;; for bool 
  (evaluate [this vars]) ;; оценка логич выражения на основе входных переменных
  (to-dnf [this]) ;; преобразвоание в ДНФ (дизъюнк. норм. форму) И / ИЛИ
  (substitute [this var value])) ;; возвращает новое логич выражение (преобразованное)

;; 2. Затем определяем все records с реализацией протокола
(defrecord Constant [value] ;; новый тип данных «константа» 
  BooleanExpression
  (evaluate [_ _] value)
  (to-dnf [this] this)
  (substitute [this _ _] this))

(defrecord Variable [name]  ;; новый тип данных «переменная» 
  BooleanExpression
  (evaluate [_ vars] (get vars name))
  (to-dnf [this] this)
  (substitute [this var value]
    (if (= name var)
      (->Constant value)
      this)))

(defrecord Not [expr]  ;; новый тип данных «НЕ»  ++ двойное отрицания, ноль -- что тогда?? ЛЮБОЕ лог выражение (закон деморгана)
  BooleanExpression
  (evaluate [_ vars] (not (evaluate expr vars)))
  (to-dnf [_]
    (let [dnf-expr (to-dnf expr)]
      (if (instance? Constant dnf-expr)
        (->Constant (not (:value dnf-expr)))
        (->Not dnf-expr))))
  (substitute [_ var value]
    (->Not (substitute expr var value))))

(defrecord And [left right]  ;; новый тип данных «И»
  BooleanExpression
  (evaluate [_ vars]
    (and (evaluate left vars) (evaluate right vars)))
  (to-dnf [_]
    (let [l (to-dnf left)
          r (to-dnf right)]
      (if (and (instance? Constant l) (instance? Constant r))
        (->Constant (and (:value l) (:value r)))
        (->And l r))))
  (substitute [_ var value]
    (->And (substitute left var value)
           (substitute right var value))))

(defrecord Or [left right] ;; новый тип данных «ИЛИ»
  BooleanExpression
  (evaluate [_ vars]
    (or (evaluate left vars) (evaluate right vars)))
  (to-dnf [_]
    (let [l (to-dnf left)
          r (to-dnf right)]
      (if (and (instance? Constant l) (instance? Constant r))
        (->Constant (or (:value l) (:value r)))
        (->Or l r))))
  (substitute [_ var value]
    (->Or (substitute left var value)
          (substitute right var value))))

(defrecord Implies [left right] ;; новый тип данных «если L то R» 
  BooleanExpression
  (evaluate [_ vars]
    (or (not (evaluate left vars)) (evaluate right vars)))
  (to-dnf [_]
    (to-dnf (->Or (->Not left) right)))
  (substitute [_ var value]
    (->Implies (substitute left var value)
               (substitute right var value))))

;; 3. Затем определяем вспомогательные функции
(def TRUE (->Constant true))
(def FALSE (->Constant false))
(defn variable [name] (->Variable name))
(defn not* [expr] (->Not expr))
(defn and* [& exprs] (reduce ->And TRUE exprs))
(defn or* [& exprs] (reduce ->Or FALSE exprs))
(defn implies* [a b] (->Implies a b))

;; Пример использования:
(comment
  ;; Создание выражения (p → (q ∧ r))
  (def example (implies* (variable :p) (and* (variable :q) (variable :r))))

  ;; Вычисление
  (evaluate example {:p true :q true :r false})

  ;; ДНФ
  (to-dnf example)

  ;; Подстановка
  (substitute example :p true))

