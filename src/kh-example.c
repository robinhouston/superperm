// khash example for string key int payload.  And string key with string payload.
//
// javadoc style docs
//   http://samtools.sourceforge.net/samtools/khash/index.html?PDefines/PDefines.html
// https://attractivechaos.wordpress.com/2008/09/02/implementing-generic-hash-library-in-c/
// https://attractivechaos.wordpress.com/2009/09/29/khash-h/
// https://attractivechaos.wordpress.com/tag/hash/
// Wrapper code for khash which is a good start for wrapping khash for ffi access from luajit.
//   https://github.com/attractivechaos/klib/issues/44

#include <stdio.h>
#include <stdlib.h>
#include "khash.h"


// shorthand way to get the key from hashtable or defVal if not found
#define kh_get_val(kname, hash, key, defVal) ({k=kh_get(kname, hash, key);(k!=kh_end(hash)?kh_val(hash,k):defVal);})

// shorthand way to set value in hash with single line command.  Returns value
// returns 0=replaced existing item, 1=bucket empty (new key), 2-adding element previously deleted
#define kh_set(kname, hash, key, val) ({int ret; k = kh_put(kname, hash,key,&ret); kh_value(hash,k) = val; ret;})

// name part of init must be unique for the key, value types.
// in this instance 33 is arbitrary symbolic name for a hashtable
// that contains string keys and int values.
//const int khStrInt = 33;
KHASH_MAP_INIT_STR(khStrInt, int) // setup khash to handle string key with int payload
int string_key_int_body_example()
{
   printf("\n\nBegin khash test string key with int payload\n");
   int ret, is_missing;
   khiter_t k;
   khash_t(khStrInt) *h = kh_init(khStrInt); // create a hashtable

   // Add a value Key "apple" to the hashtable
   k = kh_put(khStrInt, h, "apple", &ret); // add the key
   kh_value(h, k) = 10; // set the value of the key

   // shorthand way to set a value in the
   // with a macro 
   kh_set(khStrInt, h, "jimbo", 99);
   kh_set(khStrInt, h, "john haze", 98);
   kh_set(khStrInt, h, "jaki joiner", 97);

   // Retrieve the value for key "apple"
   k = kh_get(khStrInt, h, "apple");  // first have to get ieter
   if (k == kh_end(h)) {  // k will be equal to kh_end if key not present
      printf("no key found for apple");
   } else {
      printf ("key at apple=%d\n", kh_val(h,k)); // next have to fetch  the actual value
   }

   // Retrieve the value for key "apple"
   k = kh_get(khStrInt, h, "john haze");  // first have to get ieter
   if (k == kh_end(h)) {  // k will be equal to kh_end if key not present
      printf("no key found for john haze\n");
   } else {
      printf ("key at john haze=%d\n", kh_val(h,k)); // next have to fetch  the actual value
   }

   // retreive key for the key "not_present"
   // which should print the error message
   k = kh_get(khStrInt, h, "not_present");  // first have to get ieter
   if (k == kh_end(h)) {  // k will be equal to kh_end if key not present
      printf("no key found for not_present\n");
   } else {
      printf ("key at not_present=%d\n", kh_val(h,k)); // next have to fetch  the actual value
   }

   // shorthand method to get value that returns value found
   // or specified default value if not present.
   int tval = kh_get_val(khStrInt, h, "apple", -1);
   printf ("shortcut tval for apple = %d\n", tval);

   tval = kh_get_val(khStrInt, h, "john haze", -1);
   printf ("shortcut tval for john haze = %d\n", tval);

   // missing key should return default value of -1
   tval = kh_get_val(khStrInt, h, "not_present", -1);
   printf ("shortcut tval for not_present = %d\n", tval);


   // Try to delete a key and then retrieve it
   // to see if it is really gone.
   k = kh_get(khStrInt, h, "john haze"); // get the ieterator
   if (k != kh_end(h)) {  // if it is found
      printf("deleting key john_haze\n");
      kh_del(khStrInt, h, k);  // then delete it.
   }
   // now see if it is really gone
   tval = kh_get_val(khStrInt, h, "john haze", -1);
   printf ("after delete tval for john haze = %d\n", tval);


   // Ieterate the hash table by key, value and print out
   // the values found.
   printf("\nIeterate all keys\n");
   for (k = kh_begin(h); k != kh_end(h); ++k) {
      if (kh_exist(h, k)) {
         const char *key = kh_key(h,k);
         tval = kh_value(h, k);
         printf("key=%s  val=%d\n", key, tval);
      }
   }

   // cleanup and remove our hashtable
   kh_destroy(khStrInt, h);
   return 0;
}

char *missing = "MISSING";
// const int khStrStr = 32;
KHASH_MAP_INIT_STR(khStrStr, char*); // setup khash to handle string key with string body
int str_key_str_body_example()
{
   printf("\n\nBegin khash test string key with string payload\n");
   int ret, is_missing;
   khiter_t k;
   khash_t(khStrStr) *h = kh_init(khStrStr); // create a hashtable

   // Add a value Key "apple" to the hashtable
   k = kh_put(khStrStr, h, "apple", &ret); // add the key
   kh_value(h, k) = "fruit"; // set the value of the key

   // shorthand way to set a value in hash with single line. 
   kh_set(khStrStr, h, "jimbo", "artist");
   kh_set(khStrStr, h, "john haze", "engineer");
   kh_set(khStrStr, h, "jaki joiner", "architect");

   // Retrieve the value for key "apple"
   k = kh_get(khStrStr, h, "apple");  // first have to get ieter
   if (k == kh_end(h)) {  // k will be equal to kh_end if key not present
      printf("no key found for apple");
   } else {
      printf ("key at apple=%s\n", kh_val(h,k)); // next have to fetch  the actual value
   }

   // Retrieve the value for key "apple"
   k = kh_get(khStrStr, h, "john haze");  // first have to get ieter
   if (k == kh_end(h)) {  // k will be equal to kh_end if key not present
      printf("no key found for john haze\n");
   } else {
      printf ("key at john haze=%s\n", kh_val(h,k)); // next have to fetch  the actual value
   }

   // retreive key for the key "not_present"
   // which should print the error message
   k = kh_get(khStrStr, h, "not_present");  // first have to get ieter
   if (k == kh_end(h)) {  // k will be equal to kh_end if key not present
      printf("no key found for not_present\n");
   } else {
      printf ("key at not_present=%s\n", kh_val(h,k)); // next have to fetch  the actual value
   }

   // shorthand method to get value that returns value found
   // or specified default value if not present.   Would normally
   // use NULL default if key is not present but easier to printf
   // a real value.
   char *tval = kh_get_val(khStrStr, h, "apple", missing);
   printf ("shortcut tval for apple = %s\n", tval);

   tval = kh_get_val(khStrStr, h, "john haze", missing);
   printf ("shortcut tval for john haze = %s\n", tval);

   // missing key should return default value of -1
   tval = kh_get_val(khStrStr, h, "not_present", missing);
   printf ("shortcut tval for not_present = %s\n", tval);


   // Try to delete a key and then retrieve it
   // to see if it is really gone.
   k = kh_get(khStrStr, h, "john haze"); // get the ieterator
   if (k != kh_end(h)) {  // if it is found
      printf("deleting key john_haze\n");
      kh_del(khStrStr, h, k);  // then delete it.
   }
   // now see if it is really gone
   tval = kh_get_val(khStrStr, h, "john haze", missing);
   printf ("after delete tval for john haze = %s\n", tval);


   // Ieterate the hash table by key, value and print out
   // the values found.
   printf("\nIeterate all keys\n");
   for (k = kh_begin(h); k != kh_end(h); ++k) {
      if (kh_exist(h, k)) {
         const char *key = kh_key(h,k);
         tval = kh_value(h, k);
         printf("key=%s  val=%s\n", key, tval);
      }
   }

   // cleanup and remove our hashtable
   kh_destroy(khStrStr, h);
   return 0;
}


int main()
{
   string_key_int_body_example();
   str_key_str_body_example();
}

