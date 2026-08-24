cmake_minimum_required(VERSION 3.20)
project(shadow_selector_action C)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_ROOT}/bin")

add_executable(shadow_selector_action src/main.c)
set_target_properties(shadow_selector_action PROPERTIES OUTPUT_NAME "pizzahen-shadowmount-select.elf")
target_compile_options(shadow_selector_action PRIVATE --target=x86_64-sie-ps5 -DPPR -DPS5 -DPS5_FW_VERSION=${V_FW} -fPIC -fPIE -march=znver2 -Wall -Werror -O2)
target_link_directories(shadow_selector_action PUBLIC "${PROJECT_ROOT}/lib")
target_link_libraries(shadow_selector_action PUBLIC kernel_sys SceSystemService)
add_custom_command(TARGET shadow_selector_action POST_BUILD
    COMMAND ${PIZZA_HEN_OBJCOPY} --strip-unneeded $<TARGET_FILE:shadow_selector_action>
    COMMENT "Stripping ShadowMount selector action"
)
