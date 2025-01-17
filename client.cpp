#include <iostream>
#include <cstring>
#include <cstdlib>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

#define PORT 65432
#define BUFFER_SIZE 1024


//NAO parts

// #include <alerror/alerror.h>
// #include <alproxies/altexttospeechproxy.h>

// #define NAO_PORT x
// #define NAO IP x

// void forwardToRobot(const std::string& text) {
//     try {
//         // Connect to the NAO robot and create a proxy to ALTextToSpeech
//         AL::ALTextToSpeechProxy tts(NAO_IP, NAO_PORT);
//         tts.say(text);
//         std::cout << "NAO said: " << text << std::endl;
//     } catch (const AL::ALError& e) {
//         std::cerr << "Error with NAO: " << e.what() << std::endl;
//     }
// }

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};

    // Create socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // set socket options
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // define address and port
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // bind socket to address
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // start listening
    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    std::cout << "Proxy server is running and listening on port " << PORT << "..." << std::endl;

    // accepting incoming connections
    while (true) {
        if ((new_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0) {
            perror("Accept failed");
            continue; 
        }

        //receive the data
        ssize_t valread = read(new_socket, buffer, BUFFER_SIZE);
        if (valread > 0) {
            buffer[valread] = '\0'; // null-terminate the received string
            std::cout << "Received: " << buffer << std::endl;
            //forwardToRobot(buffer); //nao portion
        } else {
            std::cerr << "Failed to receive data or connection closed" << std::endl;
        }

        close(new_socket); 
    }

    // clean
    close(server_fd);
    return 0;
}
