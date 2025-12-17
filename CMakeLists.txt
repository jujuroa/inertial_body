cmake_minimum_required(VERSION 3.10)

# Set some basic project attributes
project (InertialBody
	VERSION 0.1
	DESCRIPTION "A Hello World Project")
	
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# This project will output an executable file
add_library(${PROJECT_NAME} 
			SHARED
			InertialBody.cpp)

# Create a simple configuration header
configure_file(config.h.in config.h)

# Include the configuration header in the build
target_include_directories(${PROJECT_NAME} PUBLIC "${PROJECT_BINARY_DIR}")
