/* Auto-generated by genmsg_cpp for file /home/oscar/ros_workspace/RelocSensorDriver/msg/Relocdata.msg */
#ifndef RELOCSENSORDRIVER_MESSAGE_RELOCDATA_H
#define RELOCSENSORDRIVER_MESSAGE_RELOCDATA_H
#include <string>
#include <vector>
#include <map>
#include <ostream>
#include "ros/serialization.h"
#include "ros/builtin_message_traits.h"
#include "ros/message_operations.h"
#include "ros/time.h"

#include "ros/macros.h"

#include "ros/assert.h"

#include "std_msgs/Header.h"

namespace RelocSensorDriver
{
template <class ContainerAllocator>
struct Relocdata_ {
  typedef Relocdata_<ContainerAllocator> Type;

  Relocdata_()
  : header()
  , US1(0.0)
  , US2(0.0)
  , US3(0.0)
  , US4(0.0)
  , USID()
  , IRx1(0.0)
  , IRy1(0.0)
  , IRx2(0.0)
  , IRy2(0.0)
  , IRx3(0.0)
  , IRy3(0.0)
  , IRx4(0.0)
  , IRy4(0.0)
  , IRID()
  {
  }

  Relocdata_(const ContainerAllocator& _alloc)
  : header(_alloc)
  , US1(0.0)
  , US2(0.0)
  , US3(0.0)
  , US4(0.0)
  , USID(_alloc)
  , IRx1(0.0)
  , IRy1(0.0)
  , IRx2(0.0)
  , IRy2(0.0)
  , IRx3(0.0)
  , IRy3(0.0)
  , IRx4(0.0)
  , IRy4(0.0)
  , IRID(_alloc)
  {
  }

  typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
   ::std_msgs::Header_<ContainerAllocator>  header;

  typedef double _US1_type;
  double US1;

  typedef double _US2_type;
  double US2;

  typedef double _US3_type;
  double US3;

  typedef double _US4_type;
  double US4;

  typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _USID_type;
  std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  USID;

  typedef double _IRx1_type;
  double IRx1;

  typedef double _IRy1_type;
  double IRy1;

  typedef double _IRx2_type;
  double IRx2;

  typedef double _IRy2_type;
  double IRy2;

  typedef double _IRx3_type;
  double IRx3;

  typedef double _IRy3_type;
  double IRy3;

  typedef double _IRx4_type;
  double IRx4;

  typedef double _IRy4_type;
  double IRy4;

  typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _IRID_type;
  std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  IRID;


  typedef boost::shared_ptr< ::RelocSensorDriver::Relocdata_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::RelocSensorDriver::Relocdata_<ContainerAllocator>  const> ConstPtr;
  boost::shared_ptr<std::map<std::string, std::string> > __connection_header;
}; // struct Relocdata
typedef  ::RelocSensorDriver::Relocdata_<std::allocator<void> > Relocdata;

typedef boost::shared_ptr< ::RelocSensorDriver::Relocdata> RelocdataPtr;
typedef boost::shared_ptr< ::RelocSensorDriver::Relocdata const> RelocdataConstPtr;


template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const  ::RelocSensorDriver::Relocdata_<ContainerAllocator> & v)
{
  ros::message_operations::Printer< ::RelocSensorDriver::Relocdata_<ContainerAllocator> >::stream(s, "", v);
  return s;}

} // namespace RelocSensorDriver

namespace ros
{
namespace message_traits
{
template<class ContainerAllocator> struct IsMessage< ::RelocSensorDriver::Relocdata_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct IsMessage< ::RelocSensorDriver::Relocdata_<ContainerAllocator>  const> : public TrueType {};
template<class ContainerAllocator>
struct MD5Sum< ::RelocSensorDriver::Relocdata_<ContainerAllocator> > {
  static const char* value() 
  {
    return "9643ee6acc38ea8170edc95077793e3a";
  }

  static const char* value(const  ::RelocSensorDriver::Relocdata_<ContainerAllocator> &) { return value(); } 
  static const uint64_t static_value1 = 0x9643ee6acc38ea81ULL;
  static const uint64_t static_value2 = 0x70edc95077793e3aULL;
};

template<class ContainerAllocator>
struct DataType< ::RelocSensorDriver::Relocdata_<ContainerAllocator> > {
  static const char* value() 
  {
    return "RelocSensorDriver/Relocdata";
  }

  static const char* value(const  ::RelocSensorDriver::Relocdata_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct Definition< ::RelocSensorDriver::Relocdata_<ContainerAllocator> > {
  static const char* value() 
  {
    return "\n\
# this packs the sequence the robot identity an the time stamp\n\
Header header\n\
\n\
\n\
#Range info:\n\
float64  US1\n\
float64  US2\n\
float64  US3\n\
float64  US4\n\
string	 USID\n\
\n\
#Bearing info:\n\
float64  IRx1\n\
float64  IRy1\n\
float64  IRx2\n\
float64  IRy2\n\
float64  IRx3\n\
float64  IRy3\n\
float64  IRx4\n\
float64  IRy4\n\
string	 IRID\n\
\n\
\n\
#add localization score information\n\
\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.secs: seconds (stamp_secs) since epoch\n\
# * stamp.nsecs: nanoseconds since stamp_secs\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
\n\
";
  }

  static const char* value(const  ::RelocSensorDriver::Relocdata_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator> struct HasHeader< ::RelocSensorDriver::Relocdata_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct HasHeader< const ::RelocSensorDriver::Relocdata_<ContainerAllocator> > : public TrueType {};
} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

template<class ContainerAllocator> struct Serializer< ::RelocSensorDriver::Relocdata_<ContainerAllocator> >
{
  template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
  {
    stream.next(m.header);
    stream.next(m.US1);
    stream.next(m.US2);
    stream.next(m.US3);
    stream.next(m.US4);
    stream.next(m.USID);
    stream.next(m.IRx1);
    stream.next(m.IRy1);
    stream.next(m.IRx2);
    stream.next(m.IRy2);
    stream.next(m.IRx3);
    stream.next(m.IRy3);
    stream.next(m.IRx4);
    stream.next(m.IRy4);
    stream.next(m.IRID);
  }

  ROS_DECLARE_ALLINONE_SERIALIZER;
}; // struct Relocdata_
} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::RelocSensorDriver::Relocdata_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const  ::RelocSensorDriver::Relocdata_<ContainerAllocator> & v) 
  {
    s << indent << "header: ";
s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "US1: ";
    Printer<double>::stream(s, indent + "  ", v.US1);
    s << indent << "US2: ";
    Printer<double>::stream(s, indent + "  ", v.US2);
    s << indent << "US3: ";
    Printer<double>::stream(s, indent + "  ", v.US3);
    s << indent << "US4: ";
    Printer<double>::stream(s, indent + "  ", v.US4);
    s << indent << "USID: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.USID);
    s << indent << "IRx1: ";
    Printer<double>::stream(s, indent + "  ", v.IRx1);
    s << indent << "IRy1: ";
    Printer<double>::stream(s, indent + "  ", v.IRy1);
    s << indent << "IRx2: ";
    Printer<double>::stream(s, indent + "  ", v.IRx2);
    s << indent << "IRy2: ";
    Printer<double>::stream(s, indent + "  ", v.IRy2);
    s << indent << "IRx3: ";
    Printer<double>::stream(s, indent + "  ", v.IRx3);
    s << indent << "IRy3: ";
    Printer<double>::stream(s, indent + "  ", v.IRy3);
    s << indent << "IRx4: ";
    Printer<double>::stream(s, indent + "  ", v.IRx4);
    s << indent << "IRy4: ";
    Printer<double>::stream(s, indent + "  ", v.IRy4);
    s << indent << "IRID: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.IRID);
  }
};


} // namespace message_operations
} // namespace ros

#endif // RELOCSENSORDRIVER_MESSAGE_RELOCDATA_H

