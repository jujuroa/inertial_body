cmake_minimum_required(VERSION 3.16)

project(inertial_body
    VERSION 0.1
    DESCRIPTION "Inertial Body Core Library"
    LANGUAGES CXX)

include(CMakePackageConfigHelpers)

# -----------------------------
# Library target
# -----------------------------
add_library(${PROJECT_NAME} SHARED
    src/InertialBody.cpp
)

target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_17)

configure_file(
    config.h.in
    ${PROJECT_BINARY_DIR}/config.h
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}>
        $<INSTALL_INTERFACE:include>
)

set_target_properties(${PROJECT_NAME} PROPERTIES
    OUTPUT_NAME inertial_body
    POSITION_INDEPENDENT_CODE ON
)

# -----------------------------
# Install headers
# -----------------------------
install(
    DIRECTORY include/inertial_body
    DESTINATION include
)

# -----------------------------
# Install library + export
# -----------------------------
install(
    TARGETS ${PROJECT_NAME}
    EXPORT inertial_bodyTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

install(
    EXPORT inertial_bodyTargets
    NAMESPACE inertial_body::
    DESTINATION lib/cmake/inertial_body
)

# -----------------------------
# Generate Config files
# -----------------------------
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/inertial_bodyConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/inertial_bodyConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/inertial_bodyConfig.cmake"
    INSTALL_DESTINATION lib/cmake/inertial_body
)

install(
    FILES
        "${CMAKE_CURRENT_BINARY_DIR}/inertial_bodyConfig.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/inertial_bodyConfigVersion.cmake"
    DESTINATION lib/cmake/inertial_body
)
