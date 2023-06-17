#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <pthread.h>
#include <signal.h>

#define BUFFSIZE 3
#define PORT 12347

typedef struct s_data
{
	int	fd1, fd2;
}	t_data;

typedef struct s_coord
{
	int	x, y;
}	t_coord;

void	*ThreadMain(void *arg);

int	main(void)
{
	int					serv_sock;
	int					clnt_sock1, clnt_sock2;
	struct sockaddr_in	serv_addr;
	struct sockaddr_in	clnt_addr1, clnt_addr2;
	int					clnt_addr_size1, clnt_addr_size2;
	pthread_t			t_thread;
	t_data				*data;

	serv_sock = socket(PF_INET,SOCK_STREAM,0);
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(PORT);

	if (bind(serv_sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1)
		printf("bind error\n");

	if (listen(serv_sock, 5) == -1)
		printf("listen error");

	while (1)
	{
		char	*ID1 = "X";
		char	*ID2 = "O";

		printf("1\n");
		clnt_addr_size1=sizeof(clnt_addr1);
		clnt_sock1 = accept(serv_sock, (struct sockaddr *)&clnt_addr1, &clnt_addr_size1);
		write(clnt_sock1, ID1, strlen(ID1)+1);
		
		printf("2\n");
		clnt_addr_size2=sizeof(clnt_addr2);
		clnt_sock2 = accept(serv_sock, (struct sockaddr *)&clnt_addr2, &clnt_addr_size2);
		write(clnt_sock2, ID2, strlen(ID2)+1);

		printf("3\n");
		data = (t_data *)malloc(sizeof(t_data));
		data->fd1 = clnt_sock1;
		data->fd2 = clnt_sock2;

		pthread_create(&t_thread, NULL, ThreadMain, (void *)data);
		printf("4\n");
	}
	return 0;
}

void	*ThreadMain(void *arg)
{
	t_data	*data;
	int		clnt_sock1, clnt_sock2;
	char	msg[BUFFSIZE];

	pthread_detach(pthread_self());

	//printf("Thread Main!!!\n");
	data = (t_data*)arg;
	clnt_sock1 = data->fd1;
	clnt_sock2 = data->fd2;
	
	strcpy(msg, "ma");
	write(clnt_sock1, msg, sizeof(msg));
	write(clnt_sock2, msg, sizeof(msg));
	int	i = 1;
	int a = 0;
	int b = 0;
	while (1)
	{
		printf("thread inside! %d\n", i);
		if (i%2)
		{
			printf("X : %d\n", a);
			a = read(clnt_sock1, msg, sizeof(msg));
			printf("read %s\n", msg);
			if(a < 1)
				break;
			write(clnt_sock2, msg, sizeof(msg));
			printf("send to O\n");
		}
		else
		{
			printf("O : %d\n", b);
			b = read(clnt_sock2, msg, sizeof(msg));
			printf("read %s\n", msg);
			if(b < 1)
				break;
			write(clnt_sock1, msg, sizeof(msg));
			printf("send to X\n");
		}
		i++;
	}
	free(data);
	printf("game over\n");
	//send_finish_msg(clnt_sock1, clnt_sock2);
	return	NULL;
}

//void send_finish_msg(int fd1, int fd2)
//{
	
//}