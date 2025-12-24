cmake_minimum_required(VERSION 3.16)
project(inertial_body_py LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)
find_package(inertial_body CONFIG REQUIRED)

pybind11_add_module(${PROJECT_NAME}
    inertial_body_py/bindings.cpp
)

target_link_libraries(${PROJECT_NAME}
    PRIVATE
    inertial_body::inertial_body
)

set_target_properties(${PROJECT_NAME} PROPERTIES
    OUTPUT_NAME "inertial_body_py"
    CXX_STANDARD 17
)

install(
  TARGETS inertial_body_py
  LIBRARY DESTINATION inertial_body_py
)