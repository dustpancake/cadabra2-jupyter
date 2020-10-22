cmake_minimum_required(VERSION ${CADABRA_CMAKE_VERSION})
project(Cadabra)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
print_header("Configuring SWIG for cadabra_translator")

find_package(GLIBMM REQUIRED)
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})
SET(CMAKE_SWIG_FLAGS "")

set_property(SOURCE cadabra_translator.i PROPERTY CPLUSPLUS ON)
# set_property(SOURCE cadabra_translator.i PROPERTY SWIG_FLAGS "-includeall")

include_directories(
  "."
  "${PYTHON_INCLUDE_DIRS}"
  "${CADABRA_ROOT_DIR}/client_server/jupyter/"
  "${CADABRA_LIBS_DIR}/internal/include"
)

# build swig wrapper code
SET(UseSWIG_TARGET_NAME_PREFERENCE STANDARD)
SWIG_ADD_LIBRARY(cadabra_translator
  TYPE SHARED
  LANGUAGE python
  OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}
  SOURCES cadabra_translator.i
)
set_property(TARGET cadabra_translator
  PROPERTY
  SUFFIX ".so"
)

#SET_PROPERTY(TARGET example
#  APPEND PROPERTY
#  LINK_FLAGS "-flat_namespace -undefined suppress"
#)
# if not in same directory, would have to include the headers in the swig module

MESSAGE(${PYTHON_LIBRARIES})
TARGET_LINK_LIBRARIES(cadabra_translator PRIVATE cadabra-jupyter ${PYTHON_LIBRARIES})

# ---------------------  python packaging  ---------------------------------- #
SET(PYTHON_INSTALL_FILES
  ${CMAKE_CURRENT_BINARY_DIR}/cadabra_translator.py
  ${CMAKE_CURRENT_BINARY_DIR}/_cadabra_translator.so
)
# configure setup.py and copy to output dir
SET(SETUP_PY_IN ${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in)
SET(SETUP_PY_OUT ${CMAKE_CURRENT_BINARY_DIR}/setup.py)

CONFIGURE_FILE(${SETUP_PY_IN} ${SETUP_PY_OUT})
