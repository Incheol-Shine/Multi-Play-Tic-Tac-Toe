#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>

pthread_mutex_t	g_mutex;
int				g_cnt;

void	*count(void *arg)
{
	char	*name;
	int		i = 0;

	name = (char *)arg;
	pthread_mutex_lock(&g_mutex);
	g_cnt = 0;
	while (i < 10)
	{
		printf("%s cnt: %d, i: %d\n", name, g_cnt, i);
		g_cnt++;
		usleep(1);
		i++;
	}
	pthread_mutex_unlock(&g_mutex);
	return (NULL);
}

int	main()
{
	pthread_t	pth1;
	pthread_t	pth2;
	pthread_t	pth3;

	pthread_mutex_init(&g_mutex, NULL);
	pthread_create(&pth1, NULL, count, (void *)"new thread1");
	pthread_create(&pth2, NULL, count, (void *)"new thread2");
	pthread_create(&pth3, NULL, count, (void *)"new thread3");
	pthread_join(pth1, NULL);
	pthread_join(pth2, NULL);
	pthread_join(pth3, NULL);
	pthread_mutex_destroy(&g_mutex);
	return (0);
}

