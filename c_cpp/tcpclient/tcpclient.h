#ifndef TCPCLIENT_H
#define TCPCLEINT_H

// if we are compiling this agains c++
#ifdef __cplusplus
extern "C"
{
#endif

#include <stdio.h>
#include <stdlib.h>

#include <sys/socket.h>
#include <sys/types.h>

#include <netinet/in.h>

#define PRELUDE_L 4
#define BUFFER_L 10000
#define USER_NAME_L 30
#define IP_ADDR_L 16

    enum Status
    {
        SUCCESS,
        ERROR,
        INVALID_IP,
        CONNECTION_ERROR,
        ERROR_RECEIVING,
        MESSAGE_TO_LONG,
        MAX_STATUS_COUNT,
    };

    typedef struct UserConfig UserConfig;
    struct UserConfig
    {
        char server_ip[IP_ADDR_L];
        char username[USER_NAME_L];
        int server_port;
        int user_id;
    };

    typedef struct GameUser GameUser;
    struct GameUser
    {
        char user_name[USER_NAME_L];
        int user_id;
    };

    typedef struct TCPClient TCPClient;
    struct TCPClient
    {
        int network_socket;
        struct sockaddr_in server_address;
        int connection_status;
        GameUser user;
        unsigned int message_length;
        char buffer[BUFFER_L];
    };

    enum Status connect_to_server(TCPClient *client, const char *server_ip, const int server_port);
    enum Status register_user(TCPClient *client, const char *name, int user_id, int big_endian);
    enum Status send_message(TCPClient *client, const char *message, int message_length);
    enum Status recv_message(TCPClient *client);
    const char *get_message(TCPClient *client);
    void close_connection(TCPClient *client);

// if we are compiling this agains c++
#ifdef __cplusplus
}
#endif

#endif