/********************************************
 * HTTP main.c - Connor Rogers (controge)
 * CREATED: 8/25/2023
 *
 * This program takes user input via arguments
 * and passes it through to the send_http function
 * This function creates an HTTP request to the given
 * host, and the program then prints the first 4096
 * characters of the response out
 ********************************************/

#include <stdio.h>
#include <string.h>

void send_http(char* host, char* msg, char* resp, size_t len);

/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
int main(int argc, char* argv[]) {
    //checks that user provided proper number of arguments
    if (argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }
  //initializes variables for use later in the program
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];

  //initializes msg variable for the message sent through send_http
  char msg[1024];
  //initializes string variable for response from send_http to be saved in
  char response[4096];
  //checks if verb is either POST or GET
  if(strcmp(verb, "POST") == 0){
    //if verb is POST, provides content-length for POST method
    sprintf(msg, "POST %s HTTP/1.1\r\nHost: %s\r\nContent-Length: 0\r\n\r\n", path, host);
  }else if(strcmp(verb, "GET") == 0){
    //if verb is GET, provides only host
    sprintf(msg, "GET %s HTTP/1.1\r\nHost: %s\r\n\r\n", path, host);
  }
  //sends http respons to host with message from msg variable
  send_http(host, msg, response, 4096);
  
  //prints response from about http request
  printf("%s\n", response); 
  return 0;
}