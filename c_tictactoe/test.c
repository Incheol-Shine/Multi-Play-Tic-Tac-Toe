#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 12345
/* 아마도 한번에 보내는 데이터 크기. 채팅 프로그램으로 글자 수 1024 제한을 둔 것 같다.
틱택토 게임에서는 더 작게 해도 상관 없을 듯 */
#define BUF_SIZE 1024

int	main(void)
{
	int	socket_fd, accepted_fd; // socket_fd는 소켓 반환값일거고, accepted_fd 는 뭐지?
	struct sockaddr_in	host_addr, client_addr; // ipv4 주소를 저장하는 객체인듯?
	socklen_t	size; // 뭘까?
	int	recv_length; // 뭘까?2
	char	buffer[BUF_SIZE];
	
	/* PF? AF? , SOCK_STREAM 이 TCP 통신이라함, 마지막 PROTOCOL 인자가 0 이면 자동으로 골라준다함 */
	socket_fd = socket(PF_INET, SOCK_STREAM, 0);

	host_addr.sin_family = AF_INET; // ????? 객체에 필요한 정보를 넣는데 AF_INET 은 ipv4 를 의미하는 것 같고 AF? PF?
	host_addr.sin_port = htons(PORT); // host, net 사이의 byte order (endian) 를 변환하는 함수라는데 s 는 uint16 이고 l 은 uint32 래
	host_addr.sin_addr.s_addr = htonl(INADDR_ANY); // ????????
	memset(&(host_addr.sin_zero), 0, 8); // ???????????? 뭔데 왜 8바이트만큼 0 으로 초기화한걸까?

	/* bind 는 대체 뭘까? */
	bind(socket_fd, (struct sockaddr *)&host_addr, sizeof(struct sockaddr));

	listen(socket_fd, 3); // 이 옵션을 결정하는 기준이 뭘까?
	size = sizeof(struct sockaddr);
	while (1)
	{
		accepted_fd = accept(socket_fd, (struct sockaddr *)&client_addr, &size); // 프로그램이 여기서 대기
		write(accepted_fd, "Connected", 10); // client 에 데이터 전송 ("Connected"), flag = 0 이건 뭔지 몰?루
		printf("Client Info : IP %s, Port %d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
		printf("socket port: %d\n", ntohs(host_addr.sin_port));
		recv_length = read(accepted_fd, &buffer, BUF_SIZE); //ojtube 에서는 read, write 를 썼는데 이런 함수도 제공하고 있다~
		// eof 에서 0을 반환하므로, client 가 종료되면 while 을 탈출한다.
		while (recv_length > 0)
		{
			printf("From client : %s\n", buffer);
			recv_length = read(accepted_fd, &buffer, BUF_SIZE); // 프로그램이 여기서 멈춰서 대기하네?
		}
		close(accepted_fd);
	}
	return (0);
}
