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

typedef struct thread_data
{
	int		fd;
	char	ip[20];
} t_thread_data;

void	*ThreadMain(void *arg);

void	*get_in_addr(struct sockaddr *sa)
{
	if (sa->sa_family == AF_INET)
		return &(((struct sockaddr_in *)sa)->sin_addr);
	
	return &(((struct sockaddr_in6 *)sa)->sin6_addr);
}

int	main(void)
{
	int						sock_fd, new_fd;
	struct sockaddr_storage	client_addr;
	struct sockaddr_in		serv_addr;
	char					address[20];
	int						ret;
	int						opt = 1;
	pthread_t				t_thread_id;
	unsigned int			port = 12345;
	socklen_t 				sin_size;

	signal(SIGPIPE, SIG_IGN);
	sock_fd = socket(AF_INET, SOCK_STREAM, 0);
	
	setsockopt(sock_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

	bzero(&serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	serv_addr.sin_port = htons(port);

	ret = bind(sock_fd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
	if (ret != 0)
	{
		perror("bind");
		exit(-1);
	}

	ret = listen(sock_fd, 5);
	if (ret != 0)
	{
		perror("listen");
		exit(-1);
	}

	while (1)
	{
		printf("i am wait new client \n");
		sin_size = sizeof(client_addr);
		new_fd = accept(sock_fd, (struct sockaddr *)&client_addr, &sin_size);
		if (new_fd == -1)
		{
			perror("accept");
			continue;
		}
		inet_ntop(client_addr.ss_family, 
			get_in_addr((struct sockaddr *)&client_addr), address, sizeof(address));
		printf("server: got connection from %s\n", address);

		t_thread_data *data;
		data = (t_thread_data *)malloc(sizeof(t_thread_data));
		data->fd = new_fd;
		strcpy(data->ip, address);
		pthread_create(&t_thread_id, NULL, ThreadMain, (void *)data);
	}
	return (0);
}

void	*ThreadMain(void *arg)
{
	t_thread_data	*client_data;
	int				buf_len;
	int				fd;
	char			ip[20];

	pthread_detach(pthread_self());
	client_data = (t_thread_data *)arg;
	fd = client_data->fd;
	strcpy(ip, client_data->ip);
	while (1)
	{
		int		num;
		char	buf[1024] = {0};
		
		num = read(fd, buf, sizeof(buf));
		if (num == 0)
		{
			printf("connection end bye\n");
			break;
		}
		printf("recv %s: [%s] %dbyte\n", ip, buf, num);
		// write(fd, buf, strlen(buf));
		write(fd, buf, sizeof(buf));
	}
	printf("disconnected client ip %s \n", ip);
	free(client_data);
	close(fd); // 이거 확인 할 수 있나?
	return (0);
}