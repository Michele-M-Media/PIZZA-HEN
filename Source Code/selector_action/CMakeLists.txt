cmake_minimum_required(VERSION 3.20)
project(selector_action C)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_ROOT}/bin")
add_executable(selector_action src/main.c)
set_target_properties(selector_action PROPERTIES OUTPUT_NAME "pizzahen-kstuff-select.elf")
target_compile_options(selector_action PRIVATE --target=x86_64-sie-ps5 -DPPR -DPS5 -DPS5_FW_VERSION=${V_FW} -fPIC -fPIE -march=znver2 -Wall -Werror -O2)
target_link_directories(selector_action PUBLIC "${PROJECT_ROOT}/lib")
target_link_libraries(selector_action PUBLIC kernel_sys)
add_custom_command(TARGET selector_action POST_BUILD
    COMMAND ${PIZZA_HEN_OBJCOPY} --strip-unneeded $<TARGET_FILE:selector_action>
    COMMENT "Stripping PIZZA HEN KStuff selector action")
