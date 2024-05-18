/* Implementation of a tcp client used to connect to the game server.
This client is meant to be used in both the c and c++ client. */
#include <arpa/inet.h>
#include <string.h>

#include "tcpclient.h"

unsigned int _get_message_length(const char *buffer_l);

/*******************************************************************************
 * @brief This function sets up the client and esablishes a connection to the server
 *
 * @param client A pointer to the TCPClient to be setup
 * @param server_ip The ip address of the server to connect to as a string.
 *                  Should be on the format "123.123.123.123"
 * @param server_port The port on the server to connect to
 * @return int, if -2 = invalid ip address, if -1 could not connect to server, 0 no error.
 ******************************************************************************/
enum Status connect_to_server(TCPClient *client, const char *server_ip, const int server_port)
{
    // create a socket
    client->network_socket = socket(AF_INET, SOCK_STREAM, 0);

    // specify an address for the socket
    client->server_address.sin_family = AF_INET;
    client->server_address.sin_port = htons(server_port);
    int valid_ip = inet_pton(AF_INET, server_ip, &client->server_address.sin_addr.s_addr);
    if (valid_ip == 0)
    {
        printf("Invalid ip address was provided! %s\n", server_ip);
        return INVALID_IP;
    }

    // connect to server
    client->connection_status = connect(
        client->network_socket,
        (struct sockaddr *)&(client->server_address),
        sizeof(client->server_address));
    if (client->connection_status == -1)
    {
        printf("There was an error connecting to the server!\n");
        return CONNECTION_ERROR;
    }
    return SUCCESS;
}

/*******************************************************************************
 * @brief Using prelude message, calculate the message length
 *
 * @param buffer_l
 * @return int message length
 ******************************************************************************/
unsigned int _get_message_length(const char *buffer_l)
{
    unsigned int message_length = 0;
    int offset = 24;
    for (int index = 0; index < PRELUDE_L; ++index)
    {
        message_length += (unsigned int)buffer_l[index] << offset;
        offset -= 8;
    }
    return message_length;
}

/*******************************************************************************
 * @brief Get a message from the server
 *
 * @param client A pointer to the TCPClient used for sending the message
 * @return enum Status
 ******************************************************************************/
enum Status recv_message(TCPClient *client)
{
    // recive the prelude containing message length
    char buffer_l[PRELUDE_L];
    int res_pre = recv(client->network_socket, &buffer_l, sizeof(buffer_l), 0);
    if (res_pre == -1)
    {
        printf("Error while reading prelude!\n");
        return ERROR_RECEIVING;
    }

    // calculate message length and validate against buffer
    client->message_length = _get_message_length(buffer_l);
    if (client->message_length >= BUFFER_L)
    {
        printf("Incoming message too large! msg_len=[%d] >= %d", client->message_length, BUFFER_L);
        return MESSAGE_TO_LONG;
    }

    // recive message from server
    int res_msg = recv(client->network_socket, client->buffer, client->message_length, 0);
    if (res_msg == -1)
    {
        printf("Error while reading receiving message!\n");
        return ERROR_RECEIVING;
    }

    // add null character
    client->buffer[client->message_length] = '\0';

    return SUCCESS;
}

/*******************************************************************************
 * @brief Get the message object
 *
 * @param client
 * @return const char*
 ******************************************************************************/
const char *get_message(TCPClient *client)
{
    return client->buffer;
}

/*******************************************************************************
 * @brief Sends a message to the server using a configured client.
 *
 * @param client A pointer to the TCPClient used for sending the message
 * @param message Pointer to the char array containing the message
 * @param message_length The length of the message
 * @return int
 ******************************************************************************/
enum Status send_message(TCPClient *client, const char *message, int message_length)
{
    int sent_bytes = send(client->network_socket, message, message_length, 0);
    if (sent_bytes == -1)
    {
        printf("Error while sending data to the server!");
        return ERROR;
    }
    return SUCCESS;
}

enum Status register_user(TCPClient *client, const char *name, int user_id, int big_endian)
{
}

void close_connection(TCPClient *client)
{
    close(client->network_socket);
}

int _parse_command_line_args(UserConfig *config, int argc, char *argv[])
{
    /// ./tcpclient -a 0.0.0.0 -p 9002 -n 4G -u 666
    char server_ip[16] = "0.0.0.0";
    char username[USER_NAME_L] = "4G";
    int server_port = 9002;
    int user_id = 123;

    for (int arg_index = 1; arg_index < argc; ++arg_index)
    {
        if (strcmp(argv[arg_index], "-a") == 0)
        {
            if (strlen(argv[arg_index + 1]) >= sizeof(server_ip))
            {
                printf("Provided server ip address is too long!\n");
                return -1;
            }
            strcpy(server_ip, argv[arg_index + 1]);
            ++arg_index;
        }
        else if (strcmp(argv[arg_index], "-p") == 0)
        {
            server_port = atoi(argv[arg_index + 1]);
            ++arg_index;
        }
        else if (strcmp(argv[arg_index], "-n") == 0)
        {
            if (strlen(argv[arg_index + 1]) >= sizeof(username))
            {
                printf("Username provided is too long! A maximum of %d character are allowed\n", USER_NAME_L);
                return -1;
            }
            strcpy(username, argv[arg_index + 1]);
            ++arg_index;
        }
        else if (strcmp(argv[arg_index], "-u") == 0)
        {
            user_id = atoi(argv[arg_index + 1]);
            ++arg_index;
        }
        else
        {
            printf("Unknown flag found [%s]!\n", argv[arg_index]);
        }
    }

    strcpy(config->server_ip, server_ip);
    strcpy(config->username, username);
    config->server_port = server_port;
    config->user_id = user_id;

    printf("\nClient configuration:\n");
    printf("|-Server ip: %s\n|-Server port: %d\n|-Username: %s\n|-User id: %d\n",
           config->server_ip, config->server_port, config->username, config->user_id);
    return 0;
}

int _TEST(int argc, char *argv[])
{

    // parse user input from command line
    UserConfig config;
    int parse_result = _parse_command_line_args(&config, argc, argv);
    if (parse_result != 0)
    {
        return -1;
    }
    return 0;

    // setup and establish connection with server
    TCPClient tcpClient;
    int connection_established = connect_to_server(&tcpClient, "0.0.0.0", 9002);
    if (connection_established != 0)
    {
        printf("Errors while setting up a connection to the server!\n");
        printf("Terminating program!\n\n");
        return -1;
    }

    //
    register_user(&tcpClient, "4G", 666, 0);
}

int main(int argc, char *argv[])
{

    // char buffer_l[4] = {0, 0, 1, 7};

    // unsigned int msg_len = _get_message_length(buffer_l);
    // printf("msg_len: %d\n", msg_len);

    // parse user input from command line
    UserConfig config;
    int parse_result = _parse_command_line_args(&config, argc, argv);
    if (parse_result != 0)
    {
        return -1;
    }

    // setup and establish connection with server
    TCPClient tcpClient;
    int connection_established = connect_to_server(&tcpClient, config.server_ip, config.server_port);
    if (connection_established != SUCCESS)
    {
        printf("Errors while setting up a connection to the server!\n");
        printf("Terminating program!\n\n");
        close_connection(&tcpClient);
        return -1;
    }

    int res_msg = recv_message(&tcpClient);
    if (res_msg != SUCCESS)
    {
        printf("Error reciving message!\n");
        close_connection(&tcpClient);
        return -1;
    }
    printf("Recived message: [%s]\n", tcpClient.buffer);

    close_connection(&tcpClient);
    return 0;
}