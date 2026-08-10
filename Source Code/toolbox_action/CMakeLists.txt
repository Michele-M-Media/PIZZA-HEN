cmake_minimum_required(VERSION 3.20)
project(toolbox_action C)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_ROOT}/bin")
add_executable(toolbox_action src/main.c)
set_target_properties(toolbox_action PROPERTIES OUTPUT_NAME "pizzahen-toolbox-open.elf")
target_compile_options(toolbox_action PRIVATE --target=x86_64-sie-ps5 -DPPR -DPS5 -DPS5_FW_VERSION=${V_FW} -fPIC -fPIE -march=znver2 -Wall -Werror -O2)
target_link_directories(toolbox_action PUBLIC "${PROJECT_ROOT}/lib")
target_link_libraries(toolbox_action PUBLIC kernel_sys)
add_custom_command(TARGET toolbox_action POST_BUILD
    COMMAND ${PIZZA_HEN_OBJCOPY} --strip-unneeded $<TARGET_FILE:toolbox_action>
    COMMENT "Stripping PIZZA HEN Toolbox action")
