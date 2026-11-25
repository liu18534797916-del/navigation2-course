cmake_minimum_required(VERSION 3.8)
project(scout_navigation)

find_package(ament_cmake REQUIRED)

# Установка launch-скриптов, карт и конфигураций
install(
  DIRECTORY launch maps config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
