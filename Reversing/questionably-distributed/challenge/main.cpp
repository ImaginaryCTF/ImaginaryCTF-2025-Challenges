#include"stdio.h"
#include"winsock.h"
#include"windows.h"

// flag: ictf{51ngl3_4PP_mul71pl3_53rv1c35}
// key idea: when the app is ran first, it starts copies of itself containing these elements:
// 1. data memory hosted on port 5555
// it receives a memory coordinate [x,y], and sends the data that is on the memory place XORd by the memory location
// 2. AU system, hosted on port 6666
// It receives two integers followed by the operator + - * /, and sends output
// 3. LU system, hosted on port 7777
// It receives two integers followed by the operator < > =, and sends result as a bool
// 4. dispatcher, which is the root program itself
// 5. code memory hosted on port 8888, containing opcodes
// the opcodes are defined as a character, two integers, and a character, and are context dependent

SOCKET initializeFunction(int port)
{
	WSADATA ws;
	int nret;
	//Initialise stuff
	WSAStartup(0x0101,&ws);
	SOCKET Listening;
	//Create a socket
	Listening=socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
	if(Listening==INVALID_SOCKET)return 1;
	SOCKADDR_IN serverinfo;
	//Fill in some info
	serverinfo.sin_family=AF_INET;
	serverinfo.sin_addr.s_addr=inet_addr("127.0.0.1");//The localhost,meaning the computer on which this program is running
	serverinfo.sin_port=htons(port);
	//Tell the computer that this socket is a listening one
	nret=bind(Listening,(SOCKADDR*)&serverinfo,sizeof(serverinfo));
	if(nret==SOCKET_ERROR)return 2;
	//Listen on the socket,only one at a time,you can change it to multiple
	nret=listen(Listening,1);
	if(nret==SOCKET_ERROR)return 3;
	SOCKET comm;
	//Found one? accept it on another socket
	comm=accept(Listening,0,0);
	if(comm==INVALID_SOCKET)return 4;
	return comm;
}

char arr[28][28]={
{100,66,-97,-127,-61,125,60,7,118,16,-15,-97,104,-32,11,-121,-123,-126,12,-57,-108,-92,-124,-65,52,-105,-63,26},
{9,96,122,0,-70,26,-127,125,-105,-67,-124,14,-51,117,-83,54,86,-72,-67,-37,59,-54,-94,-49,110,39,-113,-94},
{-66,80,29,-57,-56,55,-57,-126,81,72,0,-23,6,-124,-9,-45,-6,-92,9,80,92,-57,43,-105,-111,-51,103,-1},
{-12,-10,-95,26,70,94,122,14,-106,65,-112,-25,-118,-112,-48,-112,21,-57,99,15,107,109,95,-56,52,-118,95,-59},
{87,-58,-60,76,31,101,-2,2,-60,120,16,90,-70,-95,65,68,49,18,-44,70,-39,55,85,69,-92,-76,13,-40},
{62,108,-99,-106,51,102,-30,-17,-57,-32,-14,-117,89,2,-27,19,-93,38,87,-43,56,43,27,18,98,113,87,7},
{37,100,-33,100,-48,125,18,3,-34,-36,-13,-91,-68,-27,48,21,-25,21,40,-117,60,127,96,116,-86,123,-122,13},
{-20,-35,20,18,65,-13,118,103,112,112,21,79,76,8,-12,8,-19,37,30,-43,58,70,96,118,-58,-64,-21,112},
{59,113,125,40,79,-111,58,-112,3,-80,-94,-11,32,-72,68,108,-64,57,116,-82,94,-110,-125,-104,-39,-29,15,-97},
{-93,-6,15,-34,107,-115,6,-70,30,3,75,-93,-16,-19,-103,16,-91,-35,124,102,22,-15,20,116,-125,-105,13,92},
{122,28,-5,29,22,11,-5,-127,-104,2,18,-74,66,-121,90,51,116,-13,67,26,-48,-64,-128,-25,-79,-108,91,52},
{43,104,-111,-91,-124,-116,-62,-102,-105,-67,28,28,-65,88,-26,2,-33,64,53,83,51,120,109,3,56,-19,-22,-23},
{-127,70,30,-84,-82,-81,81,51,59,19,-51,-45,36,-23,2,-112,65,-24,-110,32,40,-57,116,91,64,-31,95,120},
{-49,73,98,80,-113,-128,-3,62,47,78,113,106,98,31,61,51,40,64,-61,105,40,86,-118,81,29,-2,-84,93},
{-33,11,-42,-82,85,56,-1,-28,-72,-4,34,-25,74,-109,106,-84,-46,-113,-33,-6,-49,-93,99,-9,-7,-19,72,22},
{-21,-11,116,-53,0,74,121,85,-126,120,58,58,116,92,33,96,-16,114,107,-62,1,75,-68,-48,-18,31,-56,-25},
{13,16,-3,-8,5,113,-61,6,-69,61,91,61,-75,-107,119,42,35,-104,-23,-30,11,84,-92,12,-97,96,-35,-115},
{127,-91,116,-116,-75,114,-123,-69,-29,72,-63,-97,-123,28,-36,59,-78,31,101,-92,-20,78,-122,-9,-94,42,4,66},
{-118,-31,-49,9,-122,68,-106,59,-74,27,-10,-103,99,-73,56,-23,-44,21,102,-122,105,-119,42,85,-41,-80,77,121},
{-38,81,-69,100,50,-117,109,-72,-49,3,-13,-123,30,-22,30,-126,-95,87,107,18,108,-113,-5,-43,24,37,42,-17},
{-43,119,104,-81,-56,36,19,-6,-81,-127,-78,126,-124,-90,3,-93,-112,33,37,49,100,-112,-89,-28,31,-94,-71,55},
{-56,-28,38,-99,91,-114,77,36,-78,96,30,97,-31,-47,-33,102,119,-30,9,7,4,102,56,124,-66,-33,97,-35},
{-126,26,20,74,-2,58,-25,90,-56,52,126,123,-107,-100,-36,118,109,-68,-36,-28,-98,-27,33,-94,19,36,31,-47},
{3,-128,-82,-123,-102,-62,-49,-103,-4,-73,-13,-59,-21,113,64,-128,13,28,-9,123,-40,-45,95,37,-71,75,25,-52},
{111,56,-98,114,-72,76,-8,83,15,-57,-20,11,126,-33,-48,106,80,16,-22,93,45,-31,-40,5,96,56,124,110},
{-125,-106,58,-14,-50,-40,100,-121,37,92,-38,52,36,-58,63,-94,-91,16,12,-11,32,-9,82,77,-40,22,83,-115},
{99,-49,-5,-26,101,54,-40,52,14,60,-69,51,-103,-107,103,-67,91,-89,95,0,-73,108,-11,-41,99,71,102,59},
{114,120,-55,-43,71,-60,-69,-83,-6,-109,-31,9,-48,-100,60,105,49,-92,38,-116,75,-123,-116,2,-15,-127,-39,100},
};

void MemoryFunction(int port)
{
	SOCKET sock=initializeFunction(port);
	if(sock==1)return;
	if(sock==2)return;
	if(sock==3)return;
	if(sock==4)return;
	char recvbuff[256]={0};
	//recv(sock,recvbuff,256,0);
	//printf("Memory function at port %d\n",port);
	while(1)
	{
		int x,y;
		char sendbuff[256]={0};
		int nret;
		nret=recv(sock,recvbuff,256,0);
		sscanf(recvbuff,"%d %d",&x,&y);
		sprintf(sendbuff,"%d",arr[x][y]);
		//sprintf(sendbuff,"hi\n");
		nret=send(sock,sendbuff,strlen(sendbuff)+1,0);
	}
}

void AUFunction(int port)
{
        SOCKET sock=initializeFunction(port);
	if(sock==1)return;
	if(sock==2)return;
	if(sock==3)return;
	if(sock==4)return;
	//printf("AU function at port %d\n",port);
	while(1)
	{
		int x,y;
		char op;
		int nret;
		char recvbuff[256]={0};
		char sendbuff[256]={0};
		nret = recv(sock, recvbuff,256,0);
		sscanf(recvbuff, "%d %d %c", &x, &y, &op);
		//printf("%d %d %c\n",x,y,op);
		int res;
		switch(op)
		{
			case '+':
				res = x+y;
				break;
			case '-':
				res = x-y;
				break;
			case '^':
				res = x^y;
				break;
		}
		sprintf(sendbuff,"%d",res);
		nret = send(sock, sendbuff, strlen(sendbuff)+1,0);
	}
}

void LUFunction(int port)
{
        SOCKET sock=initializeFunction(port);
	if(sock==1)return;
	if(sock==2)return;
	if(sock==3)return;
	if(sock==4)return;
	//printf("LU function at port %d\n",port);
	while(1)
	{
		char x,y;
		char op;
		char nret;
		char recvbuff[256]={0};
		char sendbuff[256]={0};
		nret = recv(sock, recvbuff,256,0);
		sscanf(recvbuff, "%d %d %c", &x, &y, &op);
		bool res;
		switch(op)
		{
			case '=':
				res = x==y;
				break;
			case '>':
				res = x>y;
				break;
			case '<':
				res = x<y;
				break;
		}
		sprintf(sendbuff,"%d",res);
		nret = send(sock, sendbuff, strlen(sendbuff)+1,0);
	}
}

int main(int argc, char* argv[])
{
	int list[]={5555,6666,7777};
	if(argc==1) //default case
	{
		//start the services
		for(int i=0; i<3;i++)
		{
			char s[100];
			sprintf(s,"start chal.exe %d\n",list[i]);
			system(s);
		}
		Sleep(500);
		// create sockets
		SOCKET sockets[3];
		for(int i=0;i<3;i++)
		{
			WSADATA ws;
			int nret;
			//Initialise stuff
			WSAStartup(0x0101,&ws);
			//Create a socket
			sockets[i]=socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
			if(sockets[i]==INVALID_SOCKET)return 1;
			SOCKADDR_IN serverinfo;
			//Fill in some info
			serverinfo.sin_family=AF_INET;
			serverinfo.sin_addr.s_addr=inet_addr("127.0.0.1");//The localhost,meaning the computer on which this program is running
			serverinfo.sin_port=htons(list[i]);
			//Tell the computer that this socket is a listening one
			nret = connect(sockets[i],(struct sockaddr*)&serverinfo,sizeof(serverinfo));
		}
		// test sockets
		char sendbuff[256]={0};
		char recvbuff[256]={0};
		//send(sockets[1],arr,strlen(arr)+1,0);
		//recv(sockets[1],recvbuff,256,0);
		//printf("%s",recvbuff);
		// dispatcher
		
		for(int i=0;i<28;i++)
		{
			for(int j=0;j<28;j++)
			{
				// take input
				sprintf(sendbuff,"%d %d",i,j);
				send(sockets[0],sendbuff,strlen(sendbuff)+1,0);
				//Sleep(100);
				recv(sockets[0],recvbuff,256,0);
				//printf("input done\n");
				int res;
				sscanf(recvbuff,"%d",&res);
				// apply xor
				sprintf(sendbuff,"%d %d ^",res,0x42);
				send(sockets[1],sendbuff,strlen(sendbuff)+1,0);
				//Sleep(100);
				recv(sockets[1],recvbuff,256,0);
				//printf("xor done\n");
				sscanf(recvbuff,"%d",&res);
				// add 15
				sprintf(sendbuff,"%d %d +",res,15);
				send(sockets[1],sendbuff,strlen(sendbuff)+1,0);
				//Sleep(100);
				recv(sockets[1],recvbuff,256,0);
				//printf("add done\n");
				sscanf(recvbuff,"%d",&res);
				//if(i==j)printf("%u ",(unsigned char)res);
			}
		}
	}
	else if(argc==2)
	{
		int req=0;
		sscanf(argv[1],"%d",&req);
		switch(req)
		{
			case 5555:
				//printf("memory");
				MemoryFunction(req);
				break;
			case 6666:
				AUFunction(req);
				break;
			case 7777:
				LUFunction(req);
				break;
			default:
				return -1;
		}
	}
	else return -1;
	return 0;
}
