#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <pthread.h>

#define BUFFSIZE 3
#define PORT 12345
#define PLAYER_X_ID "X"
#define PLAYER_O_ID "O"

/* 두 클라이언트의 소켓을 저장하는 구조체입니다. */
typedef struct s_data
{
	int	fd1, fd2;
}	t_data;

void	*thread_main(void *arg);

int	main(void)
{
	int					serv_sock;
	int					clnt_sock1, clnt_sock2;
	struct sockaddr_in	serv_addr;
	struct sockaddr_in	clnt_addr1, clnt_addr2;
	int					clnt_addr_size1, clnt_addr_size2;
	pthread_t			t_thread;
	t_data				*data;

	/* 소켓을 생성하고 주소 정보를 입력합니다. */
	serv_sock = socket(PF_INET,SOCK_STREAM,0);
	if (serv_sock == -1)
	{
		perror("socket");
		exit(EXIT_FAILURE);
	}

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(PORT);

	if (bind(serv_sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1)
	{
		perror("bind");
		exit(EXIT_FAILURE);
	}

	if (listen(serv_sock, 5) == -1)
	{
		perror("listen");
		exit(EXIT_FAILURE);
	}

	/* 두 클라이언트의 접속을 받고 새 스레드를 연 다음 소켓정보를 인자로 전달합니다. */
	while (1)
	{
		clnt_addr_size1=sizeof(clnt_addr1);
		clnt_sock1 = accept(serv_sock, (struct sockaddr *)&clnt_addr1, &clnt_addr_size1);
		if (clnt_sock1 == -1)
		{
			perror("accept");
			exit(EXIT_FAILURE);
		}
		write(clnt_sock1, PLAYER_X_ID, strlen(PLAYER_X_ID)+1);
		
		clnt_addr_size2=sizeof(clnt_addr2);
		clnt_sock2 = accept(serv_sock, (struct sockaddr *)&clnt_addr2, &clnt_addr_size2);
		if (clnt_sock2 == -1)
		{
			perror("accept");
			exit(EXIT_FAILURE);
		}
		write(clnt_sock2, PLAYER_O_ID, strlen(PLAYER_O_ID)+1);

		data = (t_data *)malloc(sizeof(t_data));
		data->fd1 = clnt_sock1;
		data->fd2 = clnt_sock2;

		pthread_create(&t_thread, NULL, thread_main, (void *)data);
	}
	close(serv_sock);
	return 0;
}

/* 새 스레드에서 동작하는 함수입니다. 두 클라이언트가 데이터를 주고받도록 합니다. */
void	*thread_main(void *arg)
{
	t_data	*data;
	int		clnt_sock1, clnt_sock2;
	char	msg[BUFFSIZE];

	pthread_detach(pthread_self());

	data = (t_data*)arg;
	clnt_sock1 = data->fd1;
	clnt_sock2 = data->fd2;
	
	/* 매칭이 이루어졌음을 두 클라이언트에게 알려줍니다. */
	strcpy(msg, "AA");
	write(clnt_sock1, msg, sizeof(msg));
	write(clnt_sock2, msg, sizeof(msg));
	
	int	i = 1;
	int len_x = 0;
	int len_o = 0;

	/* 플레이어 X, O 순서로 데이터를 받고, 상대 플레이어에게 그대로 전달합니다. */
	while (1)
	{
		if (i%2)
		{
			len_x = read(clnt_sock1, msg, sizeof(msg));
			if (strcmp(msg, "end") == 0)
				break;
			if(len_x < 1)
				break;
			write(clnt_sock2, msg, sizeof(msg));
		}
		else
		{
			len_o = read(clnt_sock2, msg, sizeof(msg));
			if (strcmp(msg, "end") == 0)
				break;
			if(len_o < 1)
				break;
			write(clnt_sock1, msg, sizeof(msg));
		}
		i++;
	}
	free(data);
	printf("game over\n");
	return	NULL;
}