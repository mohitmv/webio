#include <iostream>
#include <string>
#include <stdexcept>
#include <stdio.h>
#include <sys/socket.h>

using namespace std;
#define WM_SOCKET 0x10000

class Socket 
{
private:
    HWND WindowHandle;
    SOCKET  hSocket;
    short   port;//port number 
    string  addr; //address
    WSADATA wsaData;
    bool vlisten;
    bool init;
    bool async;



public:

    Socket() {}
    Socket(short port, std::string addr, bool vlisten , HWND WindowHandle, bool async);
    ~Socket() { Close(); }
    int RecvData(void* buff, int bufferSize){
        return recv(hSocket, reinterpret_cast<char*>(buff), bufferSize, 0);
    }
    int RecvData(SOCKET S,void* buff,int bufferSize){
        return recv(S, reinterpret_cast<char*>(buff), bufferSize, 0);
    }
    int SendData(void* buff, int bufferSize){
        return send(hSocket,0);
    }


    int SendData(SOCKET S,void* buff,int bufferSize)
    {
        return send(S, reinterpret_cast<char*>(buff), bufferSize, 0);
    }

    bool Connect(short port,std::string addr,bool vlisten,HWND WindowHandle,bool async);
    //SOCKET Accept(sockaddr* clientInfo,int* clientInfoSize)
    SOCKET Accept()
    {
        static int size = sizeof(sockaddr);
        return accept(this->hSocket, 0,0);
    }
    SOCKET GetSocket() const{return this->hSocket;}
    void Close()
    {
        if (hSocket)
        {
            shutdown(hSocket,SD_BOTH);
            closesocket(hSocket);
            hSocket = 0;
        }
        if(init)
        {
            WSACleanup();
        }
    }

    bool Connect(short port,std::string addr,bool vlisten,HWND WindowHandle,WSADATA& wsaData,bool async)
    {
        if(!hSocket)
        {
            this->port = port;
            t
            this->wsaData =wsaData;
            this->init = true;


            struct sockaddr_in* sockaddr_ipv4;

            if(WSAStartup(MAKEWORD(2,2),&wsaData) !=0)
            {
                throw runtime_error("Error WSAStartup:" + WSAGetLastError());
            }

            if((this->hSocket = ::socket(AF_INET,SOCK_STREAM,IPPROTO_TCP))== INVALID_SOCKET)
            {
                Close();
                throw runtime_error("Error init sockect:" + WSAGetLastError());
            }

            if(addr != "INADDR_ANY")
            {
                struct addrinfo *result = nullptr;

                struct addrinfo *it;
                for (it = result; it != nullptr; it = it->ai_next)
                {
                    struct addrinfo *result = nullptr;
                    getaddrinfo(addr.c_str(), nullptr, nullptr, &result);
                    struct addrinfo* it;
                    for (it = result; it != nullptr; it = it->ai_next)
                    {
                        sockaddr_ipv4 = reinterpret_cast<sockaddr_in*>(it->ai_addr);
                        addr = inet_ntoa(sockaddr_ipv4->sin_addr);
                        if (addr != "0.0.0.0") break;
                    }
                    freeaddrinfo(result);
                }
            }
            SOCKADDR_IN sockAddrIn;
            memset(&sockAddrIn,0,sizeof(sockAddrIn));
            sockAddrIn.sin_port = htons(port);
            sockAddrIn.sin_family =  AF_INET;
            sockAddrIn.sin_addr.s_addr = (addr == "INADDR_ANY" ? htonl(INADDR_ANY) : inet_addr(addr.c_str()));

            if(vlisten && (bind(hSocket,reinterpret_cast<SOCKADDR*>(&sockAddrIn),sizeof(sockAddrIn))== SOCKET_ERROR))
            {
                Close();
                throw runtime_error("Error vlisten & bind: " + WSAGetLastError());
            }

            if(async && WindowHandle)
            {
                if(WSAAsyncSelect(hSocket,WindowHandle,WM_SOCKET,FD_READ|FD_WRITE|FD_CONNECT|FD_CLOSE|FD_ACCEPT) !=0)
                {
                    Close();
                    throw runtime_error("Error async & WindowHandle: " + WSAGetLastError());
                }

            }

            if(vlisten && (listen(hSocket,SOMAXCONN)== SOCKET_ERROR))
            {
                Close();
                throw runtime_error("Error async & WindowHandle: " + WSAGetLastError());
            }

            if(!vlisten && (connect(hSocket, reinterpret_cast<SOCKADDR*>(&sockAddrIn), sizeof(sockAddrIn)) == SOCKET_ERROR))
            {
                if(async && WindowHandle && (WSAGetLastError() != WSAEWOULDBLOCK))
                {
                    Close();
                    throw runtime_error("Error async & WindowHandle: " + WSAGetLastError());
                }
            }
        }
    }
    void SendLine(string str)
    {
        SendData(str,str.size());
    }

};

