cmake_minimum_required(VERSION 3.8)
project(scout_gazebo)

find_package(ament_cmake REQUIRED)

# Установка launch-скриптов, миров и конфигураций
install(
  DIRECTORY launch worlds config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
