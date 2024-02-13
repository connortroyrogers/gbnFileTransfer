/********************************************
 * DNS main.c - Connor Rogers (controge)
 * CREATED: 9/8/2023
 * This program prints the IPv4 and v6 information
 * from a provided host using DNS information servers
 * given a proper host and port is provided by the
 * user
 ********************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <arpa/inet.h>
/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }

  //get host and port from user arguments
  char* host = argv[1];
  long port = atoi(argv[2]);
  
  //initialize strings
  char charport[32];
  char ipAddr[64];
  char str[64];
  //initialize addrinfo structures for future use
  struct addrinfo hints, *i, *res;
  //hints to gather distinct addresses via TCP
  memset(&hints, 0, sizeof(struct addrinfo));
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  
  //convert given long port to string
  sprintf(charport, "%ld", port);
  //request info using host and port, sending info to res (result) addrinfo structure
  getaddrinfo(host, charport, &hints, &res);

  //iterate through results from getaddrinfo
  for(i = res; i!=NULL; i=i->ai_next){
    //initialize raw address variable
    void* raw_addr;
    //if current ip address type is IPv4
    if(i -> ai_family == AF_INET){
      //create temporary variable to store socket address in ipv4 format
      struct sockaddr_in* tmp = (struct sockaddr_in*)i->ai_addr;
      //get ipv4 address from temp variable
      raw_addr = &(tmp->sin_addr);
      //print to string the ipv4 address that was converted from raw address to string
      snprintf(ipAddr, INET6_ADDRSTRLEN, "IPv4 %s", inet_ntop(AF_INET, raw_addr, str, sizeof(str)));
    //if current ip address type is IPv6
    }else if(i -> ai_family == AF_INET6){
      //create temp variable for socket ipv6 address
      struct sockaddr_in6* tmp = (struct sockaddr_in6*)i->ai_addr;
      //get ipv6 address from temp variable
      raw_addr = &(tmp->sin6_addr);
      //print to string the ipv6 address that was converted from raw address to string
      snprintf(ipAddr, INET6_ADDRSTRLEN, "IPv6 %s", inet_ntop(AF_INET6, raw_addr, str, sizeof(str)));
    }
    //print current address to console
    printf("%s\n", ipAddr);
  }
  return 0;
}
