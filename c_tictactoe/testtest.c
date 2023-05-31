#include <stdio.h>
#include <stdlib.h>

typedef struct thread_data
{
	int		fd;
	char	ip[20];
} t_thread_data;

int	main(void)
{
	t_thread_data *temp;
	temp = (t_thread_data *)malloc(sizeof(t_thread_data));

	temp->fd = 3;
	int fd = temp->fd;

	fd = 2;
	printf("fd : %d, temp->fd : %d\n",fd, temp->fd);

	return (0);
}
