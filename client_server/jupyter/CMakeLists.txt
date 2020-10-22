cmake_minimum_required(VERSION ${CADABRA_CMAKE_VERSION})
project(Cadabra)

print_header("Configuring Jupyter Kernel")

find_package(GLIBMM  REQUIRED)
find_package(Threads REQUIRED)
find_package(Boost 1.53.0 COMPONENTS
  system
  program_options
  date_time
  filesystem REQUIRED
)

if(ENABLE_SYSTEM_JSONCPP)
  message("-- Linking against system-provided jsoncpp")
  find_package(JSONCPP REQUIRED)
else()
  message("-- Linking against included jsoncpp")
endif()

set(CADABRA_JUPYTER_SRC
  cadabra_translator.cc
  ${CADABRA_CORE_DIR}/InstallPrefix.cc
  ${CADABRA_CORE_DIR}/DataCell.cc
  ${CADABRA_CORE_DIR}/CdbPython.cc
  ${CADABRA_LIBS_DIR}/whereami/whereami.c
  ${CADABRA_LIBS_DIR}/base64/base64.cc
)

if(NOT ENABLE_SYSTEM_JSONCPP)
  list(APPEND CADABRA_JUPYTER_SRC
	 ${CADABRA_LIBS_DIR}/jsoncpp/jsoncpp.cpp
	 )
endif()

include_directories(
	"."
	"${CADABRA_CORE_DIR}"
	#"${CADABRA_LIBS_DIR}/pybind11/include"
	#"${CADABRA_LIBS_DIR}/websocketpp"
	"${CADABRA_LIBS_DIR}/internal/include"
	"${CADABRA_LIBS_DIR}/whereami"
	"${CADABRA_LIBS_DIR}/base64"
	#${Boost_INCLUDE_DIRS}
	#${PYTHON_INCLUDE_DIRS}
	#${SQLITE3_INCLUDE_DIR}
)

if(ENABLE_SYSTEM_JSONCPP)
  include_directories(
	 ${JSONCPP_INCLUDE_DIRS}
	 )
else()
  include_directories(
	 "${CADABRA_LIBS_DIR}/jsoncpp"
	 )
endif()

add_library(cadabra-jupyter STATIC ${CADABRA_JUPYTER_SRC})
set_target_properties(cadabra-jupyter
  PROPERTIES
  PUBLIC_HEADER cadabra_translator.hh
)
target_link_libraries(cadabra-jupyter
  #${Boost_LIBRARIES}
  ${GLIBMM3_LIBRARIES}
  #${PYTHON_LIBRARIES}
)

if(ENABLE_SYSTEM_JSONCPP)
  target_link_libraries(cadabra-jupyter
	 ${JSONCPP_LIBRARIES}
	 )
endif()

# build swig
add_subdirectory(swig)
