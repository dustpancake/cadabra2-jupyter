#include "cadabra_translator.hh"
#include "CdbPython.hh"

std::string parse_cadabra(const std::string& blk) {
  return cadabra::cdb2python_string(blk, true);
}
