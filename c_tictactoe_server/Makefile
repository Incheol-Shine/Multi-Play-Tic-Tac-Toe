NAME	= tictactoe_server
RM 		= rm -f

# src / obj files
SRC		= tictactoe_server.c 
OBJ		= $(SRC:.c=.o)

# compiler
CC = cc

all : $(NAME)

$(NAME): $(OBJ)
	$(CC) $(OBJ) -lpthread -o $(NAME)

%.o: %.c
	$(CC) -c $< -o $@

clean :
	$(RM) $(OBJ)

fclean : clean
	@$(RM) $(NAME)

re : fclean
	@make all

.PHONY : all clean fclean re