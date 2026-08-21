cmake_minimum_required(VERSION 3.20)
project(toolbox_api C)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_ROOT}/bin")
add_executable(toolbox_api src/main.c)
set_target_properties(toolbox_api PROPERTIES OUTPUT_NAME "pizzahen-api.elf")
target_compile_options(toolbox_api PRIVATE --target=x86_64-sie-ps5 -DPPR -DPS5 -DPS5_FW_VERSION=${V_FW} -fPIC -fPIE -march=znver2 -Wall -Werror -O2)
target_link_directories(toolbox_api PUBLIC "${PROJECT_ROOT}/lib")
target_link_libraries(toolbox_api PUBLIC kernel_sys)
add_custom_command(TARGET toolbox_api POST_BUILD
    COMMAND ${PIZZA_HEN_OBJCOPY} --strip-unneeded $<TARGET_FILE:toolbox_api>
    COMMENT "Stripping PIZZA HEN API action")
