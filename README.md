# Ridley
Maestro Of Robots

# Запуск модуля
1. Запускаем flask-cервер из папки src/py_srvcli/py_srvcli/:
   ```
   flask --app flask_server run
   ```
2. Запускам ROS2-клиент:
   
    2.1. `source install/setup.bash`

    2.2  `ros2 run py_srvcli client`

3. Запускаем проигрываение rosbag2(мы использовали rosbag2_2023_09_09-18_26_09 (отличный)):
  ```
  ros2 bag play .
  ```

4. Открываем src/py_srvcli/py_srvcli/index.html в браузере
