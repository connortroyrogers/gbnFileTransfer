/********************************************
 * SMTP main.c - Connor Rogers (controge)
 * CREATED: 8/31/2023
 *
 * This program takes user input via arguments
 * that provide the recipient and filepath for 
 * an email. It starts a socket connection to smtp
 * with connect_smtp then interacts with the email
 * server using send_smtp
 ********************************************/

#include <stdio.h>
#include <string.h>
int PORT = 25;
int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);

/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];
  char response[4096];
  char recipient[256];
  char to[256];
  char contents[4096];
  char message[8000];
  char from[256];
  FILE *fptr;
  fptr = fopen(filepath,"r");

  if(fptr == NULL){
    printf("Error: No file at filepath");
    return -1;
  }
  //
  size_t read_size = fread(contents, 1, sizeof(contents) -1, fptr);
  contents[read_size] = '\0';
  if(read_size > 4096){
    printf("Error: Email contents too large");
    return -1;
  }
  
  fclose(fptr);

  strcat(contents, "\r\n");
  //print address of recipient to 'to' and 'recipient' variables with formatting.
  sprintf(to, "To: %s\r\n", rcpt);
  sprintf(recipient, "RCPT TO:%s\r\n", rcpt);
  //format DATA of the email
  sprintf(message, "From: %s\r\nSubject: Test Email\r\n%s\r\n%s\r\n.\r\n", rcpt, to, contents);
  sprintf(from, "MAIL FROM: %s\r\n", rcpt);
  //initialize socket for smtp
  int socket = connect_smtp("lunar.open.sice.indiana.edu", PORT);

  //say hello to mail server
  send_smtp(socket, "HELO iu.edu\r\n", response, 4096);
  printf("%s", response);
  //tell server who the mail is coming from
  send_smtp(socket, from, response, 4096);
  printf("%s", response);
  //tell the server who the recipient is
  send_smtp(socket, recipient, response, 4096);
  printf("%s", response);
  //provide server with DATA for message
  send_smtp(socket, "DATA\r\n", response, 4096);
  printf("%s", response);
  //provide contents of email to lunar
  send_smtp(socket, message, response, 4096);
  printf("%s", response);

  return 0;
}