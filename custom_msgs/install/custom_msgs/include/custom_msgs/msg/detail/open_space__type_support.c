// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from custom_msgs:msg/OpenSpace.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "custom_msgs/msg/detail/open_space__rosidl_typesupport_introspection_c.h"
#include "custom_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "custom_msgs/msg/detail/open_space__functions.h"
#include "custom_msgs/msg/detail/open_space__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  custom_msgs__msg__OpenSpace__init(message_memory);
}

void OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_fini_function(void * message_memory)
{
  custom_msgs__msg__OpenSpace__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_message_member_array[2] = {
  {
    "angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_msgs__msg__OpenSpace, angle),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "distance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_msgs__msg__OpenSpace, distance),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_message_members = {
  "custom_msgs__msg",  // message namespace
  "OpenSpace",  // message name
  2,  // number of fields
  sizeof(custom_msgs__msg__OpenSpace),
  OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_message_member_array,  // message members
  OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_init_function,  // function to initialize message memory (memory has to be allocated)
  OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_message_type_support_handle = {
  0,
  &OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_custom_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msgs, msg, OpenSpace)() {
  if (!OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_message_type_support_handle.typesupport_identifier) {
    OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &OpenSpace__rosidl_typesupport_introspection_c__OpenSpace_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
