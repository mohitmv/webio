
namespace webio {

struct Json {
  enum Type {INT_TYPE, STRING_TYPE, NULL_TYPE, BOOL_TYPE, LIST, MAP};
  Type type;
  boost::varient<>;
};


} // namespace webio
