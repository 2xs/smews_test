#ifndef __DYNAMIC_TEST_H__
#define __DYNAMIC_TEST_H__

#ifndef TEST_ARRAY_SIZE
  #ifdef DEV_MTU
    #define ARRAY_SIZE ((DEV_MTU-150) < 0 ? OUTPUT_BUFFER_SIZE : (DEV_MTU-150))
  #else
    #define ARRAY_SIZE OUTPUT_BUFFER_SIZE
  #endif
#else
  #define ARRAY_SIZE TEST_ARRAY_SIZE
#endif


#endif
