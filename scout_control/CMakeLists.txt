cmake_minimum_required(VERSION 3.8)
project(scout_control)

find_package(ament_cmake REQUIRED)

# Установка launch-скриптов и конфигураций контроллеров
install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
