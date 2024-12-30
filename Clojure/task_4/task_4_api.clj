(ns task_4_api
  (:require [compojure.core :refer [defroutes GET POST]]
            [compojure.route :as route]
            [ring.middleware.json :refer [wrap-json-body wrap-json-response]]
            [ring.adapter.jetty :refer [run-jetty]]
            [task_4.core :as logic]))  ; Импорт пространства имен с логикой

;; Определите маршруты
(defroutes app-routes
  (GET "/evaluate" [expr vars]
    (let [parsed-expr (read-string expr)  ; Преобразуем строку в выражение
          parsed-vars (read-string vars)]  ; Преобразуем строку в переменные
      {:status 200
       :body {:result (logic/evaluate parsed-expr parsed-vars)}}))

  (POST "/substitute" [expr var value]
    (let [parsed-expr (read-string expr)
          substituted-expr (logic/substitute parsed-expr (keyword var) value)]
      {:status 200
       :body {:result substituted-expr}}))

  (route/not-found "Not Found"))

;; Запуск сервера
(defn -main []
  (run-jetty (wrap-json-response (wrap-json-body app-routes)) {:port 3000}))

